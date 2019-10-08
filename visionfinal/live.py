import cv2
import numpy
from dronekit import VehicleMode, connect

cam = cv2.VideoCapture("./sololink.sdp")
#cam = cv2.VideoCapture(0)
print cam.isOpened()
#vehicle = connect('udpin:0.0.0.0:14550',wait_ready=True)
#print "Armed : %s" % vehicle.armed
#vehicle.armed = True

while(True):
        ret, frame = cam.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()
