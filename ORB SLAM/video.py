import cv2
import numpy as np
from ORB import ORB

video_path = "../data/ORB/orb_vid.mp4"
cap = cv2.VideoCapture(video_path)
fps = 20 # An assumption
img_width = 640 # An assumption
img_height = 480
img_size = ((img_height,img_width))
orb = ORB()

# videoWriter = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'),fps, img_size)

firstFrame = True
draw = True
while (cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.resize(frame,img_size,interpolation=cv2.INTER_AREA)

    if firstFrame:
        # Save first frame as init frame
        frame_last = frame
        kp_last, des_last = orb.extractORB(frame)
        firstFrame = False
        continue
    
    try:
        kp_new, des_new = orb.extractORB(frame)
        rotation,translation = orb.get_pose(frame_last,frame,(kp_last,des_last),(kp_new,des_new),draw)

        print(f"[INFO] ROTATION =\n{rotation}\nTRANSLATION =\n{translation}")          
     
         # videoWriter.write(image)

        frame_last = frame
        kp_last, des_last = kp_new, des_new

        if draw and cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print("[WARNING] Tracking is lost!!!!!!!!!!!!!")
        print("[EXCEPTION]",e)
        print("[TODO] Save this frame to Bag of Words")

print("[INFO] Video ended")
cap.release()

cv2.destroyAllWindows()