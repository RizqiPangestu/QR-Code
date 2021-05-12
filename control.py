
import cv2
import math

BLUE  = (255,0,0)
GREEN = (0,255,0)
RED   = (0,0,255)

class Control():
    def __init__(self):
        super().__init__()
        self.pwm_roll = 1500
        self.pwm_pitch = 1500
        self.pwm_thr = 1500
        self.center_status = RED
        self.drop_status = "wait"

    def off2pwm(self,offset):
        '''
        TODO PID control optimization
        '''
        pwm = 1500 + (500 * offset)
        return pwm

    def distance2pwm(self,distance):
        '''
        TODO PID control optimization
        '''
        if distance > 10:
            return 1600
        else:
            return 1500

    def centering_QR(self,image,coordinates_QR,size_QR):
        '''
        Control the attitude roll and throttle of vehicle by calculating offset value by pixel position using front camera
        param:
        image(list2D)
        coordinates(x,y)
        size((height,width))
        return True if center, False otherwise
        '''
        img_width = image.shape[1]
        img_height = image.shape[0]

        # Get midpoint of image and QR
        x = coordinates_QR[0] + size_QR[0]/2
        y = coordinates_QR[1] + size_QR[1]/2
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
        cv2.putText(image,text_log,(0,60),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        # TODO Set offset tolerance param (assumption is 0.3)
        if offset < 0.3: 
            return True
        else:
            return False

    def approaching_QR(self,distance):
        '''
        Control the attitude pitch of vehicle by calculating distance(cm) from QR
        return True if QR close, False otherwise
        '''
        self.pwm_pitch = self.distance2pwm(distance)
        if distance <= 40:
            return True
        else:
            return False

    def centering_drop(self,image,size,offset):
        '''
        Control the position of vehicle to centering the dropping zone using bottom camera
        param:
        image(list2D)
        size((height,width))
        '''
        img_width = image.shape[1]
        img_height = image.shape[0]
        # up(keatas)-> crush(maju) -> centering -> drop
        # up
        if self.drop_status == "up":
            offsetz = offset[2]
            self.pwm_thr = self.off2pwm(offsetz)
            if offset[2] < 1.0:
                self.drop_status = "crush"
        # up done, go crush
        elif self.drop_status == "crush":
            offsety = offset[1]
            self.pwm_pitch = self.off2pwm(offsety)
            if offset[1] < 1.0:
                self.drop_status = "center"
        # crush done, go centering
        elif self.drop_status == "center":

            '''
            Detect red colors and get bounding box coordinates
            '''
            coordinates_red = [0,0] # dummy (dapet dari image processing)
            # Get midpoint of image and corner of red rectangle
            x = coordinates_red[0]
            y = coordinates_red[1]
            midx = img_width/2
            midy = img_height/2

            dx = x - midx
            dy = y - midy
            offsetx = (dx/midx)
            offsety = (dy/midy)
            offset = math.sqrt((offsetx**2 + offsety**2))
            
            # Control
            self.pwm_roll = self.off2pwm(offsetx)
            self.pwm_pitch = self.off2pwm(offsety)

            #Print txt to image
            text_log = "Offset : {:.2f}cm".format(offset)
            cv2.putText(image,text_log,(0,60),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

            # TODO Set offset tolerance param (assumption is 0.3)
            if offset < 0.3:
                self.drop_status = "up"
                return True
            else:
                return False

        


if __name__== "__main__" :
	print("Control Class")