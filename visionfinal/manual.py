
import numpy
import time
from dronekit import VehicleMode, connect
from pymavlink import mavutil

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

	send_ned_velocity(numpy.cos(vehicle.heading),numpy.sin(vehicle.heading),0,duration)
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
"""
def back(duration):

	send_ned_velocity(-1*numpy.cos(vehicle.heading),-1*numpy.sin(vehicle.heading),0,duration)	
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
"""

def right(duration):

	send_ned_velocity(numpy.sin(vehicle.heading),numpy.cos(vehicle.heading),0,duration)
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
"""

def left(duration):

	send_ned_velocity(-1*numpy.sin(vehicle.heading),-1*numpy.cos(vehicle.heading),0,duration)
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
"""	

		


vehicle = connect('udpin:0.0.0.0:14550', wait_ready=True)
vehicle.armed = True



   


initial(quiroga)
print "Altitude achieved"
time.sleep(5)

"""
Adelante x > 0
Atras x < 0
Izquierda y < 0
Derecha y > 0
Abajo z > 1
Arriba z < 1
"""

"""
forward(1)
back(1)
right(1)
left(1)
land()

vehicle.close()

"""