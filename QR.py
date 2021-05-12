import cv2
from pyzbar import pyzbar
from control import Control

BLUE  = (255,0,0)
GREEN = (0,255,0)
RED   = (0,0,255)

#Focal Length in cm
F = 546.4285714285714


class QR(Control):
	def __init__(self):
		self.data = list()
		self.distance = 0
		self.status = RED

	def calc_distance(self,F,pixel_width,real_width = 2.8):
		return F * real_width / pixel_width

	def center_status(self,image,coordinates,size,distance):
		'''
		Centering and approaching control to QR code
		return green color if offset < 0.1, otherwise red
		'''
		if self.centering_QR(image,coordinates,size) and self.approaching_QR(distance):
			return GREEN
		else:
			return RED

	def processQR(self,image):
		barcodes = pyzbar.decode(image)
		for barcode in barcodes:
			(x,y,w,h) = barcode.rect
			coordinates_QR = (x,y)
			size_QR = (w,h)
			self.distance = self.calc_distance(F,w)
			self.status = self.center_status(image,coordinates_QR,size_QR,self.distance)
			self.data.append(barcode.data.decode("utf-8"))
			cv2.rectangle(image, (x, y), (x + w, y + h), self.status, 2)

		# Put text for data log
		text_log = "QR count : {}".format(len(barcodes))
		cv2.putText(image,text_log,(0,10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, GREEN, 2)
		text_log = "Distance : {:.2f}cm".format(self.distance)
		cv2.putText(image,text_log,(0,35),cv2.FONT_HERSHEY_SIMPLEX, 0.5, GREEN, 2)
		return image,self.status

	def get_data(self):
		'''
		return list of string type data
		'''
		return self.data
	
	def get_status(self):
		return self.status
		

if __name__== "__main__" :
	print("QR Class")