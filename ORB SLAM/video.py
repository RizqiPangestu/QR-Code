import cv2

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

videoWriter = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'),fps, img_size)

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

        matches = bf.match(des_last,des_new)
        matches = sorted(matches, key = lambda x:x.distance)
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

        image = cv2.drawKeypoints(frame, kp_new, None, color=(0,255,0), flags=0)
            
        cv2.imshow("Frame Points",image)
         # videoWriter.write(image)

        frame_last = frame
        kp_last, des_last = kp_new, des_new

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print("[EXCEPTION]",e)
        print("[TODO] Save this frame to Bag of Words")

print("[INFO] Video ended")
cap.release()

cv2.destroyAllWindows()