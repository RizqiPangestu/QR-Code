import cv2
from QR import QR
from control import Control

video_path = "sample3.mp4"
cap = cv2.VideoCapture(video_path)
fps = 20 # An assumption
img_width = 640 # An assumption
img_height = 480
img_size = ((img_height,img_width))
QR = QR()

videoWriter = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'),fps, img_size)

while (cap.isOpened()):
    ret, frame = cap.read()
    try:
        frame = cv2.resize(frame,img_size,interpolation=cv2.INTER_AREA)
        image = QR.processQR(frame)
        cv2.imshow("capture",image)
        # videoWriter.write(image)
        ret, frame = cap.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print("[EXCEPTION]",e)
        break

print("[INFO] Video ended")
cap.release()

cv2.destroyAllWindows()