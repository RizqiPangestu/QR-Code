import cv2
from pyzbar import pyzbar
from control import Control

GREEN = (0,255,0)
RED = (0,0,255)

#Focal Length
F = 546.4285714285714


class QR():
	def __init__(self):
		self.data = list()
		self.control = Control(1500,1500,1500)

	def distance(self,F,pixel_width,real_width = 2.8):
		return abs(F * real_width / pixel_width)

	def center_status(self,image,coordinates,size,distance):
		'''
		return green color if offset < 0.1, otherwise red
		'''
		if self.control.centering(image,coordinates,size) and self.control.approaching(distance):
			return GREEN
		else:
			return RED

	def processQR(self,image):
		barcodes = pyzbar.decode(image)
		for barcode in barcodes:
			(x,y,w,h) = barcode.rect
			coordinates = (x,y)
			size = (w,h)
			d = self.distance(F,w)
			color = self.center_status(image,coordinates,size,d)
			self.data.append(barcode.data.decode("utf-8"))
			text_log = "Distance : {:.2f}cm".format(d)
			cv2.putText(image,text_log,(0,35),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
			cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
		return image,self.data
		

if __name__== "__main__" :
	print("QR Class")