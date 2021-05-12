
from time import time
from control import Control
import cv2

class Drop(Control):
    def __init__(self):
        super().__init__()
        self.pwm_servo = 1500

    def wait(self,sec):
        '''
        wait for some sec then decode
        '''
        t0 = time()
        t1 = time()
        print("[INFO] Waiting...")
        while((t1 - t0) < sec):
            t1 = time()

    def drop(self,data):
        '''
        Dropping Mechanism
        1. Wait 3 second for confirmation (should be thread)
        TODO make thread for timer (keknya gaperlu lagi)
        '''
        # self.wait(3)
        
        '''
        2. Get color code
        '''
        print(type(data))
        print(data)

        if data == 'VTOL 1': # RED
            self.pwm_servo = 1000
        elif data == 'VTOL 2': # GREEN
            pass
            self.pwm_servo = 1500
        elif data == 'VTOL 3': # BLUE
            self.pwm_servo = 2000

    def set_data(self,data):
        self.data = data

    def reset(self):
        pass


if __name__=="__main__":
    print("Drop Class")