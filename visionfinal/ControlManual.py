import time
import sys, termios, tty, os
from dronekit import VehicleMode, connect
from pymavlink import mavutil


altitude =1

def initial():
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


def land():
	print "Landing"
	vehicle.mode = VehicleMode("LAND")
	time.sleep(5)
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
	"""
	Correct vehicle forward movement based in heading
	"""
	#Norte
	if (vehicle.heading >= 0 and vehicle.heading < 22 ) or vehicle.heading >= 337:
		send_ned_velocity(1,0,0,duration)
	#Nor-este
	if vehicle.heading >= 22 or vehicle.heading < 67:
		send_ned_velocity(1,1,0,duration)
	#Este
	if vehicle.heading >= 67 and vehicle.heading < 112:
		send_ned_velocity(0,1,0,duration)
	#Sur-este
	if vehicle.heading >= 112 and vehicle.heading < 157:
		send_ned_velocity(-1,1,0,duration)
	#Sur
	if vehicle.heading >= 157 and vehicle.heading < 202:
		send_ned_velocity(-1,0,0,duration)
	#Sur-oeste
	if vehicle.heading >= 202 and vehicle.heading < 247:
		send_ned_velocity(-1,-1,0,duration)
	#Oeste
	if vehicle.heading >= 247 and vehicle.heading < 292:
		send_ned_velocity(0,-1,0,duration)
	#Nor-oeste
	if vehicle.heading > 292 and vehicle.heading < 337:
		send_ned_velocity(1,-1,0,duration)

def back(duration):
	"""
	Correct vehicle back movement based in heading
	"""
	#Norte
	if (vehicle.heading >= 0 and vehicle.heading < 22 ) or vehicle.heading >= 337:
		send_ned_velocity(-1,0,0,duration)
	#Nor-este
	if vehicle.heading >= 22 or vehicle.heading < 67:
		send_ned_velocity(-1,-1,0,duration)
	#Este
	if vehicle.heading >= 67 and vehicle.heading < 112:
		send_ned_velocity(0,-1,0,duration)
	#Sur-este
	if vehicle.heading >= 112 and vehicle.heading < 157:
		send_ned_velocity(1,-1,0,duration)
	#Sur
	if vehicle.heading >= 157 and vehicle.heading < 202:
		send_ned_velocity(1,0,0,duration)
	#Sur-oeste
	if vehicle.heading >= 202 and vehicle.heading < 247:
		send_ned_velocity(1,1,0,duration)
	#Oeste
	if vehicle.heading >= 247 and vehicle.heading < 292:
		send_ned_velocity(0,1,0,duration)
	#Nor-oeste
	if vehicle.heading > 292 and vehicle.heading < 337:
		send_ned_velocity(-1,1,0,duration)

def right(duration):
	"""
	Correct vehicle right movement based in heading
	"""
	#Norte
	if (vehicle.heading >= 0 and vehicle.heading < 22 ) or vehicle.heading >= 337:
		send_ned_velocity(0,1,0,duration)
	#Nor-este
	if vehicle.heading >= 22 or vehicle.heading < 67:
		send_ned_velocity(-1,1,0,duration)
	#Este
	if vehicle.heading >= 67 and vehicle.heading < 112:
		send_ned_velocity(-1,0,0,duration)
	#Sur-este
	if vehicle.heading >= 112 and vehicle.heading < 157:
		send_ned_velocity(-1,-1,0,duration)
	#Sur
	if vehicle.heading >= 157 and vehicle.heading < 202:
		send_ned_velocity(0,-1,0,duration)
	#Sur-oeste
	if vehicle.heading >= 202 and vehicle.heading < 247:
		send_ned_velocity(1,-1,0,duration)
	#Oeste
	if vehicle.heading >= 247 and vehicle.heading < 292:
		send_ned_velocity(1,0,0,duration)
	#Nor-oeste
	if vehicle.heading > 292 and vehicle.heading < 337:
		send_ned_velocity(1,1,0,duration)

def left(duration):
	"""
	Correct vehicle left movement based in heading
	"""
	#Norte
	if (vehicle.heading >= 0 and vehicle.heading < 22 ) or vehicle.heading >= 337:
		send_ned_velocity(0,-1,0,duration)
	#Nor-este
	if vehicle.heading >= 22 or vehicle.heading < 67:
		send_ned_velocity(1,-1,0,duration)
	#Este
	if vehicle.heading >= 67 and vehicle.heading < 112:
		send_ned_velocity(1,0,0,duration)
	#Sur-este
	if vehicle.heading >= 112 and vehicle.heading < 157:
		send_ned_velocity(1,1,0,duration)
	#Sur
	if vehicle.heading >= 157 and vehicle.heading < 202:
		send_ned_velocity(0,1,0,duration)
	#Sur-oeste
	if vehicle.heading >= 202 and vehicle.heading < 247:
		send_ned_velocity(-1,1,0,duration)
	#Oeste
	if vehicle.heading >= 247 and vehicle.heading < 292:
		send_ned_velocity(-1,0,0,duration)
	#Nor-oeste
	if vehicle.heading > 292 and vehicle.heading < 337:
		send_ned_velocity(-1,-1,0,duration)

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

vehicle = connect('udpin:0.0.0.0:14550', wait_ready=True)
initial()
print """
Despegar = t
Aterrizar = y
Adelante = w
Atras = s
Derecha = d
Izquierda = a
Arriba = k
Abajo = l
"""

	

while(1):
	char = getch()
	
	if char == "t":
		print "Despegando cuidado"
		vehicle.simple_takeoff(altitude)

		while True:
			print " Altitude: ", vehicle.location.global_relative_frame.alt	
			if vehicle.location.global_relative_frame.alt>=altitude*0.95:
				print "Reached target altitude"
				break
	if char == "w":
		#Adelante
		forward(1)
	if char == "s":
		#Atras
		back(1)
	if char == "d":
		#Derecha
		right(1)
	if char == "a":
		#Izquierda
		left(1)
	if char == "k":
		#Arriba
		send_ned_velocity(0,0,-1,1)
	if char == "l":
		#Abajo
		send_ned_velocity(0,0,1,1)	
	if char == "y":
		land()
		break
	if char == "q":
		vehicle.armed = False
		break			

"""
	Adelante x > 0
	Atras x < 0
	Abajo z > 0
	Arriba z < 0
	Derecha y > 0
	Izquierda y < 0
"""



vehicle.close()

