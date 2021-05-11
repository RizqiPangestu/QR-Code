import cv2
import numpy as np

video_path = "../data/ORB/orb_vid.mp4"
cap = cv2.VideoCapture(video_path)
fps = 20 # An assumption
img_width = 640 # An assumption
img_height = 480
img_size = ((img_height,img_width))

# Initiate ORB detector
orb = cv2.ORB_create(nfeatures=1000,scaleFactor=1.2)

# create BFMatcher object
bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=True)

# videoWriter = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'),fps, img_size)

# Intrinsic Camera
'''
SHOULD BE CALIBRATED!!
'''
kinect_intrinsic_param = np.array([[514.04093664, 0., 320], [0., 514.87476583, 240], [0., 0., 1.]])
kinect_distortion_param = np.array([2.68661165e-01, -1.31720458e+00, -3.22098653e-03, -1.11578383e-03, 2.44470018e+00])

# applying homography matrix as inference of perpective transformation
def output_perspective_transform(img_object, M):
    print(img_object.shape)
    h,w,_ = img_object.shape
    corner_pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    center_pts = np.float32([ [w/2,h/2] ]).reshape(-1,1,2)
    corner_pts_3d = np.float32([ [-w/2,-h/2,0],[-w/2,(h-1)/2,0],[(w-1)/2,(h-1)/2,0],[(w-1)/2,-h/2,0] ])###
    corner_camera_coord = cv2.perspectiveTransform(corner_pts,M)###
    center_camera_coord = cv2.perspectiveTransform(center_pts,M)
    return corner_camera_coord, center_camera_coord, corner_pts_3d, center_pts

# solving pnp using iterative LMA algorithm
def iterative_solve_pnp(object_points, image_points):
    image_points = image_points.reshape(-1,2)
    retval, rotation, translation = cv2.solvePnP(object_points, image_points, kinect_intrinsic_param, kinect_distortion_param)
    return rotation, translation

firstFrame = True
while (cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.resize(frame,img_size,interpolation=cv2.INTER_AREA)

    if firstFrame:
        # Save first frame as init frame
        frame_last = frame
        kp_last, des_last = orb.detectAndCompute(frame,None)
        firstFrame = False
        continue
    
    try:
        kp_new, des_new = orb.detectAndCompute(frame,None)

        image = cv2.drawKeypoints(frame, kp_new, None, color=(0,255,0), flags=0) 
        cv2.imshow("Frame Points",image)

        matches = bf.match(des_last,des_new)
        matches = sorted(matches, key = lambda x:x.distance)
        # Init list of points to save points coordinates
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)
        for i, match in enumerate(matches):
            points1[i, :] = kp_last[match.queryIdx].pt    #gives index of the descriptor in the list of query descriptors
            points2[i, :] = kp_new[match.trainIdx].pt    #gives index of the descriptor in the list of train descriptors

        img_match = cv2.drawMatches(frame_last,kp_last,frame,kp_new,matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow("Matches",img_match)

        idx = list()
        for i in range(len(matches)):
            idx.append(matches[i].trainIdx)

        kp_fix = list()

        for i in range(len(kp_new)):
            if i in idx:
                kp_fix.append(kp_new[i])

        img_fix = cv2.drawKeypoints(frame, kp_fix, None, color=(255,255,0), flags=0)
        text_log = "Fix points count : {}".format(len(kp_fix))
        cv2.putText(img_fix,text_log,(0,10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        cv2.imshow("Fixed Points",img_fix)

        '''
        Find Homography using RANSAC
        Output = matrix Homography
        '''
        h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

        # apply homography matrix using perspective transformation
        corner_camera_coord, center_camera_coord, object_points_3d, center_pts = output_perspective_transform(img_fix, h)
                
        # solve pnp using iterative LMA algorithm
        rotation, translation = iterative_solve_pnp(object_points_3d, corner_camera_coord)

        print(f"[INFO] ROTATION =\n{rotation}\nTRANSLATION =\n{translation}")          

        
         # videoWriter.write(image)

        frame_last = frame
        kp_last, des_last = kp_new, des_new

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print("[WARNING] Tracking is lost!!!!!!!!!!!!!")
        print("[EXCEPTION]",e)
        print("[TODO] Save this frame to Bag of Words")

print("[INFO] Video ended")
cap.release()

cv2.destroyAllWindows()