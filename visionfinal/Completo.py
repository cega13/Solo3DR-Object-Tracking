import numpy as np
import time
from dronekit import VehicleMode, connect
from pymavlink import mavutil
import cv2

quiroga=1.70

def initial(initialAlt):
	"""
	Arms vehicle an elevates to certain alt
	"""
	print "Checking Armability"
	while not vehicle.is_armable:
		print "Waiting for este wey to be ready"
		time.sleep(1)

	print "Esta madre esta despertando" 
	vehicle.mode = VehicleMode("GUIDED")
	vehicle.armed = True
	
	while not vehicle.armed:
		print "Esperando a que despierte"
		time.sleep(1)

	print "Despegando cuidado"
	vehicle.simple_takeoff(initialAlt)

	while True:
		print " Altitude: ", vehicle.location.global_relative_frame.alt	
		if vehicle.location.global_relative_frame.alt>=initialAlt*0.95:
			print "Reached target altitude"
			break
		time.sleep(1)


def land():
	print "Landing"
	vehicle.mode = VehicleMode("LAND")
	time.sleep(10)
	vehicle.armed= False
	print "Ya se apago"


def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle on 1 Hz cycle
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)


def forward(duration):

	send_ned_velocity(np.cos(vehicle.heading),np.sin(vehicle.heading),0,duration)


def back(duration):

	send_ned_velocity(-1*np.cos(vehicle.heading),-1*np.sin(vehicle.heading),0,duration)	


def right(duration):

	send_ned_velocity(np.sin(vehicle.heading),np.cos(vehicle.heading),0,duration)


def left(duration):

	send_ned_velocity(-1*np.sin(vehicle.heading),-1*np.cos(vehicle.heading),0,duration)


def getthresholdedimg(hsv):#Amarillo
    threshImg = cv2.inRange(hsv,(25,100,20),(35,255,255))
    return threshImg


c = cv2.VideoCapture(0)
width,height = c.get(3),c.get(4)
print "frame width and height : ", width, height

ROIwidth = width/3
ROIwidth2 = ROIwidth*2
ROIheight = height/3
ROIheight2 = ROIheight*2



cv2.namedWindow('Output', cv2.WINDOW_NORMAL)


print("..::Presione La Letra q Para Salir::..")

vehicle = connect('udpin:0.0.0.0:14550', wait_ready=True)
#initial(2*quiroga)
#print "Altitude achieved"




while(1):
	_,f = c.read()
	f = cv2.flip(f,1)
	blur = cv2.medianBlur(f,5)
	hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
	thrImg = getthresholdedimg(hsv)
	erode = cv2.erode(thrImg,None,iterations = 3)
	dilate = cv2.dilate(erode,None,iterations = 10)

	image,contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	"""
	Lineas de cuadrantes para 3DR solo
	cv2.line(img=f, pt1=(426, 0), pt2=(426, 720), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	cv2.line(img=f, pt1=(853, 0), pt2=(853, 720), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	cv2.line(img=f, pt1=(0, 240), pt2=(1280, 240), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	cv2.line(img=f, pt1=(0, 480), pt2=(1280, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	"""	

	#Lineas de cuadrantes webcam
	cv2.line(img=f, pt1=(213, 0), pt2=(213, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	cv2.line(img=f, pt1=(426, 0), pt2=(426, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	cv2.line(img=f, pt1=(0, 160), pt2=(640, 160), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
	cv2.line(img=f, pt1=(0, 320), pt2=(640, 320), color=(255, 0, 0), thickness=2, lineType=8, shift=0)

	for cnt in contours:
		x,y,w,h = cv2.boundingRect(cnt)
		cx,cy = x+w/2, y+h/2
		cv2.rectangle(f,(x,y),(x+w,y+h),[0,0,255],2)
		
		""""
		En que cuadrante estoy para 3DR       
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

		# En que cuadrante estoy para WebCam
		if ((cx < 213) and (cy < 160)):
			print("Cuadrante   (1,1)")
		elif ((cx < 213) and (cy > 160) and (cy < 320)):
			print("Cuadrante   (2,1)")
		elif ((cx < 213) and (cy > 230) and (cy < 480)):
			print("Cuadrante   (3,1)")
		elif ((cx > 213) and (cx < 426) and (cy < 160)):
			print("Cuadrante   (1,2)")
		elif ((cx > 213) and (cx < 426) and (cy > 160) and (cy < 320)):
			print("Cuadrante   (2,2)")
			initial(2*quiroga)
			time.sleep(5)
			land()
		elif ((cx > 213) and (cx < 426) and (cy > 320) and (cy < 480)):
			print("Cuadrante   (3,2)")
		elif ((cx > 426) and (cy < 160)):
			print("Cuadrante   (1,3)")
		elif ((cx > 426) and (cy > 160) and (cy < 320)):
			print("Cuadrante   (2,3)")
		elif ((cx > 426) and (cy > 320)):
			print("Cuadrante   (3,3)")
	
		"""
		if(cv2.getTrackbarPos('Caliberate','Trackbars') == 1):        
		cv2.imshow('Output',thrImg)
		else:
		cv2.imshow('Output',f)
		"""
	cv2.imshow('Output',f)
		#cv2.waitKey(50)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		land()
		break


cv2.destroyAllWindows()
c.release()
vehicle.close()


	

