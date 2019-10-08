import cv2
import numpy as np
import time


def getthresholdedimg(hsv):
    threshImg = cv2.inRange(hsv,(145,50,20),(155,100,255))
    return threshImg

def getTrackValue(value):
    return value


c = cv2.VideoCapture("./sololink.sdp")
#c = cv2.VideoCapture(0)
width,height = c.get(3),c.get(4)
print "frame width and height : ", width, height


ROIwidth = width/3
print("ROIwidth = ",+ROIwidth)
ROIwidth2 = ROIwidth*2
print("ROIwidth2 = ",+ROIwidth2)
ROIheight = height/3
print("ROIheight = ", +ROIheight)
ROIheight2 = ROIheight*2
print("Roiheight2 = ", +ROIheight2)


cv2.namedWindow('Output', cv2.WINDOW_NORMAL)



print("..::Presione La Letra q Para Salir::..")

while(1):
	_,f = c.read()
	f = cv2.flip(f,1)
	blur = cv2.medianBlur(f,5)
	hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
	thrImg = getthresholdedimg(hsv)
	erode = cv2.erode(thrImg,None,iterations = 3)
	dilate = cv2.dilate(erode,None,iterations = 10)

	image,contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	
	#Lineas de cuadrantes para 3DR solo
	cv2.line(img=f, pt1=(426, 0), pt2=(426, 720), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	cv2.line(img=f, pt1=(853, 0), pt2=(853, 720), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	cv2.line(img=f, pt1=(0, 240), pt2=(1280, 240), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	cv2.line(img=f, pt1=(0, 480), pt2=(1280, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	"""
	#Lineas de cuadrantes para WebCam
	cv2.line(img=f, pt1=(213, 0), pt2=(213, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	cv2.line(img=f, pt1=(426, 0), pt2=(426, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	cv2.line(img=f, pt1=(0, 160), pt2=(640, 160), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	cv2.line(img=f, pt1=(0, 320), pt2=(640, 320), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	"""
	for cnt in contours:
		x,y,w,h = cv2.boundingRect(cnt)
		cx,cy = x+w/2, y+h/2
		cv2.rectangle(f,(x,y),(x+w,y+h),[0,0,255],2)

		
		#En que cuadrante estoy para 3DR       
		if((cx < 426)and(cy<240)):
		    print("Cuadrante   (1,1)")
		elif((cx < 426)and(cy > 240) and (cy<480)):
		    print("Cuadrante   (2,1)")
		elif((cx < 426)and(cy > 480) and (cy<720)):
		    print("Cuadrante   (3,1)")
		elif((cx>426)and(cx<853)and(cy<240)):
		    print("Cuadrante   (1,2)")
		elif((cx>426)and(cx<853)and(cy>240)and(cy<480)):
		    print("Cuadrante   (2,2)")
		elif((cx>426)and(cx<853)and(cy>480)and(cy<720)):
		    print("Cuadrante   (3,2)")
		elif((cx>853)and(cy<240)):
		    print("Cuadrante   (1,3)")
		elif((cx>853)and(cy>240)and(cy<480)):
		    print("Cuadrante   (2,3)")
		elif((cx>853)and(cy>480)):
		    print("Cuadrante   (3,3)")
		"""

		#En que cuadrante estoy para WebCam
		if((cx < 213)and(cy<160)):
			print("Cuadrante   (1,1)")
						
		elif((cx < 213)and(cy > 160) and (cy<320)):
			print("Cuadrante   (2,1)")
		elif((cx < 213)and(cy > 230) and (cy<480)):
			print("Cuadrante   (3,1)")
		elif((cx>213)and(cx<426)and(cy<160)):
			print("Cuadrante   (1,2)")
		elif((cx>213)and(cx<426)and(cy>160)and(cy<320)):
			print("Cuadrante   (2,2)")
		elif((cx>213)and(cx<426)and(cy>320)and(cy<480)):
			print("Cuadrante   (3,2)")
		elif((cx>426)and(cy<160)):
			print("Cuadrante   (1,3)")
		elif((cx>426)and(cy>160)and(cy<320)):
			print("Cuadrante   (2,3)")
		elif((cx>426)and(cy>320)):
			print("Cuadrante   (3,3)")
		"""
	
		"""
		if(cv2.getTrackbarPos('Caliberate','Trackbars') == 1):        
		cv2.imshow('Output',thrImg)
		else:
		cv2.imshow('Output',f)
		"""
	cv2.imshow('Output',f)
		#cv2.waitKey(50)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		print "salida"
		break

cv2.destroyAllWindows()
c.release()
