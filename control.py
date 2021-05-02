
import cv2
import math

class Control():
    def __init__(self,pwm_roll,pwm_pitch,pwm_thr):
        super().__init__()
        self.pwm_roll = pwm_roll
        self.pwm_pitch = pwm_pitch
        self.pwm_thr = pwm_thr

    def off2pwm(self,offset):
        '''
        TODO control optimization
        '''
        roll = 1500 + (500 * offset)
        return roll

    def distance2pwm(self,distance):
        '''
        TODO control optimization
        '''
        if distance > 10:
            return 1600
        else:
            return 1500

    def centering(self,image,coordinates,size):
        '''
        Control the attitude roll and throttle of vehicle by calculating offset value by pixel position
        return True if center, False otherwise
        '''
        img_width = image.shape[1]
        img_height = image.shape[0]

        # Get midpoint of image and QR
        x = coordinates[0] + size[0]/2
        y = coordinates[1] + size[1]/2
        midx = img_width/2
        midy = img_height/2

        dx = x - midx
        dy = y - midy
        offsetx = (dx/midx)
        offsety = (dy/midy)
        offset = math.sqrt((offsetx**2 + offsety**2))
        
        # Control
        self.pwm_roll = self.off2pwm(offsetx)
        self.pwm_thr = self.off2pwm(offsety)

        #Print txt to image
        text_log = "Offset : {:.2f}cm".format(offset)
        cv2.putText(image,text_log,(0,10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        # TODO Set offset tolerance param (assumption is 0.3)
        if offset < 0.3: 
            return True
        else:
            return False

    def approaching(self,distance):
        '''
        Control the attitude pitch of vehicle by calculating distance from QR
        return True if QR close, False otherwise
        '''
        self.pwm_pitch = self.distance2pwm(distance)
        if distance <= 40:
            return True
        else:
            return False


    def scan(self):
        pass

    def drop(self):
        pass

if __name__== "__main__" :
	print("Control Class")