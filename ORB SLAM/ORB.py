'''
ORB Feature Extraction
TODO
1. Feature Matching
- 2 image
- ORB Feature
- Brute Force Matcher

2. KeyFrame
- Frame with matches points

3. Tracking Position (PnP)
- Matrix of intrinsic camera
- Matches points (use RANSAC to eliminate outliers point)

4. Covisibility

5. Mapping
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt

# Intrinsic Camera
'''
SHOULD BE CALIBRATED!!
'''
kinect_intrinsic_param = np.array([[514.04093664, 0., 320], [0., 514.87476583, 240], [0., 0., 1.]])
kinect_distortion_param = np.array([2.68661165e-01, -1.31720458e+00, -3.22098653e-03, -1.11578383e-03, 2.44470018e+00])


class ORB():
    def __init__(self):
        super().__init__()
        # Initiate ORB detector
        self.orb = cv2.ORB_create(nfeatures=1000,scaleFactor=1.2)
        self.bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=True)

    # applying homography matrix as inference of perpective transformation
    def output_perspective_transform(self,img_object, M):
        print(img_object.shape)
        h,w,_ = img_object.shape
        corner_pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        center_pts = np.float32([ [w/2,h/2] ]).reshape(-1,1,2)
        corner_pts_3d = np.float32([ [-w/2,-h/2,0],[-w/2,(h-1)/2,0],[(w-1)/2,(h-1)/2,0],[(w-1)/2,-h/2,0] ])
        corner_camera_coord = cv2.perspectiveTransform(corner_pts,M)
        center_camera_coord = cv2.perspectiveTransform(center_pts,M)
        return corner_camera_coord, center_camera_coord, corner_pts_3d, center_pts

    # solving pnp using iterative LMA algorithm
    def iterative_solve_pnp(self,object_points, image_points):
        image_points = image_points.reshape(-1,2)
        retval, rotation, translation = cv2.solvePnP(object_points, image_points, kinect_intrinsic_param, kinect_distortion_param)
        return rotation, translation

    def extractORB(self,img):
        return self.orb.detectAndCompute(img,None)

    def matchingPoints(self,img,img2,orb1,orb2,draw=False):
        kp1,des1 = orb1[0],orb1[1]
        kp2,des2 = orb2[0],orb2[1]

        # compute matches points between two images
        matches = self.bf.match(des1,des2)
        matches = sorted(matches, key = lambda x:x.distance)

        # deselect points that not matched
        idx = list()
        kp_connected = list()
        for i in range(len(matches)):
            idx.append(matches[i].trainIdx)

        for i in range(len(kp2)):
            if i in idx:
                kp_connected.append(kp2[i])

        self.img_fix = cv2.drawKeypoints(img2, kp_connected, None, color=(0,255,0), flags=0)

        # Init list of points to save points coordinates
        self.points1 = np.zeros((len(matches), 2), dtype=np.float32)
        self.points2 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            self.points1[i, :] = kp1[match.queryIdx].pt    #gives index of the descriptor in the list of query descriptors
            self.points2[i, :] = kp2[match.trainIdx].pt    #gives index of the descriptor in the list of train descriptors
        


        if draw:
            img2 = cv2.drawKeypoints(img2, kp2, None, color=(0,255,0), flags=0)
            cv2.imshow("Keypoints on frame",img2)

            img3 = cv2.drawMatches(img,kp1,img2,kp2,matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            text_log = "Fix points count : {}".format(len(matches))
            cv2.putText(img3,text_log,(0,10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            cv2.imshow("Matched Keypoints",img3)

            text_log = "Fix points count : {}".format(len(kp_connected))
            cv2.putText(self.img_fix,text_log,(0,10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            cv2.imshow("Fixed Connected Points",self.img_fix)



    # Find Homography using RANSAC
    # Output = matrix Homography
    def homography(self):
        h, mask = cv2.findHomography(self.points1, self.points2, cv2.RANSAC)

        # apply homography matrix using perspective transformation
        corner_camera_coord, center_camera_coord, object_points_3d, center_pts = self.output_perspective_transform(self.img_fix, h)
                
        # solve pnp using iterative LMA algorithm
        self.rotation, self.translation = self.iterative_solve_pnp(object_points_3d, corner_camera_coord)

    def get_pose(self,frame_last,frame,orb1,orb2,draw=False):
        self.matchingPoints(frame_last,frame,orb1,orb2,draw)
        self.homography()
        return self.rotation,self.translation

if __name__=="__main__":
    img = cv2.imread("../data/ORB/orb1.jpg")
    img2 = cv2.imread("../data/ORB/orb2.jpg")
    img_width = 640 # An assumption
    img_height = 480
    img_size = ((img_height,img_width))
    img = cv2.resize(img,img_size,interpolation=cv2.INTER_AREA)
    img2 = cv2.resize(img2,img_size,interpolation=cv2.INTER_AREA)


    obj = ORB()

    kp1,des1 = obj.extractORB(img)
    kp2,des2 = obj.extractORB(img2)

    rotation,translation = obj.get_pose(img,img2,(kp1,des1),(kp2,des2),draw=True)

    print(f"[INFO] ROTATION =\n{rotation}\nTRANSLATION =\n{translation}")  

    cv2.waitKey()
    cv2.destroyAllWindows()



       