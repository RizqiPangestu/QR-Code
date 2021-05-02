
from time import time
from QR import QR
import cv2

class Drop():
    def __init__(self,image):
        super().__init__()
        img_width = 640 # An assumption
        img_height = 480
        img_size = ((img_height,img_width))
        self.image = cv2.resize(image,img_size,interpolation=cv2.INTER_AREA)
        self.QR = QR()

    def wait(self,sec):
        '''
        wait for some sec then decode
        '''
        t0 = time()
        t1 = time()
        print("[INFO] Waiting...")
        while((t1 - t0) < sec):
            t1 = time()

    def drop(self):
        '''
        Dropping Mechanism
        1. Wait 3 second for confirmation (should be thread)
        TODO make thread for timer
        '''
        # self.wait(3)
        
        '''
        2. Get color code
        '''
        self.QR.processQR(self.image)
        data = self.QR.get_data()
        for code in data:
            print(code)
            print(type(code))
            if data == 'RED':
                pass
            elif data == 'GREEN':
                pass
            elif data == 'BLUE':
                pass

    def reset(self):
        pass


if __name__=="__main__":
    image = cv2.imread("18cm.jpg")
    obj = Drop(image)
    obj.drop()
    print("Hello")