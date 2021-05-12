import cv2
import numpy as np

from QR import QR
from drop import Drop

'''
1. Localization to QR area
2. Centering and Scan QR
3. Localization and Centering dropping zone
4. Dropping
'''

GREEN = (0,255,0)
RED   = (0,0,255)
status_qr = RED

video_path = "data/video_QR/sample3.mp4"
cap = cv2.VideoCapture(video_path)  # Cam 1
cap2 = cv2.VideoCapture(video_path) # Cam 2
fps = 20 # An assumption
img_width = 640 # An assumption
img_height = 480
img_size = ((img_height,img_width))
QR = QR()
drop = Drop()

# videoWriter = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'),fps, img_size)

while (cap.isOpened() and cap2.isOpened()):
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
    try:
        frame = cv2.resize(frame,img_size,interpolation=cv2.INTER_AREA)
        frame2 = cv2.resize(frame,img_size,interpolation=cv2.INTER_AREA)

        if status_qr == RED:
            image, status_qr = QR.processQR(frame) # Frame from Cam 1
            cv2.imshow("capture",image)
        elif status_qr == GREEN:
            xyz_now = np.array([0,0,0]) # Dapet dari FC (ini data dummy)
            xyz_setpoint = xyz_now + 20 # sesuain sendiri mau naik berapa cm
            print(xyz_setpoint)
            offset = xyz_now - xyz_setpoint
            status_drop = drop.centering_drop(frame2,img_size,offset) # Frame from Cam 2
            if status_drop:
                drop.drop(QR.get_data())
                status_qr = RED
        
        # videoWriter.write(image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print("[EXCEPTION]",e)
        break

print("[INFO] Video ended")
cap.release()

cv2.destroyAllWindows()