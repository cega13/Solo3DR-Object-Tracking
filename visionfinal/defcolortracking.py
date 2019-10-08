
import cv2
import numpy as np
import serial
import time
import ffmpeg

def getthresholdedimg1(hsv):#Amarillo
    threshImg = cv2.inRange(hsv,(25,100,20),(30,255,255))
    return threshImg
    
def getthresholdedimg2(hsv):#Rosa
    threshImg = cv2.inRange(hsv,(158,35,20),(168,230,255))
    return threshImg    
    
def getthresholdedimg3(hsv):#Rojo
    threshImg = cv2.inRange(hsv,(0,90,20),(5,230,255))
    return threshImg  
      
def getthresholdedimg4(hsv):#Verde
    threshImg = cv2.inRange(hsv,(40,90,20),(50,255,255))
    return threshImg 
       
def getthresholdedimg5(hsv):#Naranja
    threshImg = cv2.inRange(hsv,(5,90,20),(15,255,255))
    return threshImg    
 
     
def getTrackValue(value):
    return value


#c = cv2.VideoCapture(0)
c = ffmpeg("./sololink.sdp")
#c = cv2.VideoCapture("./sololink.sdp")
#c = cv2.VideoCapture(10.1.1.1)
width,height = c.get(3),c.get(4)
print "       Bienvenido"
print "frame width and height : ", width, height


#Dividir el
ROIwidth = width/3
ROIwidth2 = ROIwidth*2
ROIheight = height/3
ROIheight2 = ROIheight*2


#Declarar ventanas
cv2.namedWindow('Output', cv2.WINDOW_NORMAL)
ser = serial.Serial('COM11')

print'''..::Presione La Letra ESC Para Salir::..
 >Presiona 1 para seguir el  Color Amarillo
 >Presiona 2 para seguir el  Color Rosa
 >Presiona 3 para seguir el  Color Rojo
 >Presiona 4 para seguir el  Color Verde
 >Presiona 5 para seguir el  Color Naranja\n\n'''

color = input(" Presione el color que desea seguir: \n")
while(1):
    
    
    
    k =cv2.waitKey(10)
    if k== 27: #ESC for exit
    #if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    _,f = c.read()
    f = cv2.flip(f,1)
    blur = cv2.medianBlur(f,5)
    hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    
    #Leyendo color de input
    if color==1:
        thrImg = getthresholdedimg1(hsv)
    elif color ==2:
        thrImg = getthresholdedimg2(hsv)
    elif color ==3:
        thrImg = getthresholdedimg3(hsv)
    elif color ==4:
        thrImg = getthresholdedimg4(hsv)
    elif color ==5:
        thrImg = getthresholdedimg5(hsv)
        
    if k== 49: #1
        print "Siguiendo Color Amarillo"
        color=1  
    if k==50: #2
        print "Siguiendo Color Rosa"
        color=2
    if k==51:
        print "Siguiendo Color Rojo"
        color=3
    if k==52:
        print "Siguiendo Color Verde"
        color=4
    if k==53:
        print "Siguiendo Color Naranja"
        color=5
    
    erode = cv2.erode(thrImg,None,iterations = 3)
    dilate = cv2.dilate(erode,None,iterations = 10)

    image,contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
     #Lineas de cuadrantes para 3DR solo
    cv2.line(img=f, pt1=(426, 0), pt2=(426, 720), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    cv2.line(img=f, pt1=(853, 0), pt2=(853, 720), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    cv2.line(img=f, pt1=(0, 240), pt2=(1280, 240), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    cv2.line(img=f, pt1=(0, 480), pt2=(1280, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    '''
    #Lineas de cuadrantes para WebCam
    cv2.line(img=f, pt1=(213, 0), pt2=(213, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    cv2.line(img=f, pt1=(426, 0), pt2=(426, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    cv2.line(img=f, pt1=(0, 160), pt2=(640, 160), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    cv2.line(img=f, pt1=(0, 320), pt2=(640, 320), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    '''
    for cnt in contours:
    	x,y,w,h = cv2.boundingRect(cnt)
    	cx,cy = x+w/2, y+h/2
    	cv2.rectangle(f,(x,y),(x+w,y+h),[0,0,255],2)
        
	#En que cuadrante estoy para 3DR       
        if((cx < 426)and(cy<240)):
            print("Cuadrante   (1,1)")
            ser.write("A")

        elif((cx < 426)and(cy > 240) and (cy<480)):
            print("Cuadrante   (2,1)")
            ser.write("I")

        elif((cx < 426)and(cy > 480) and (cy<720)):
            print("Cuadrante   (3,1)")
            ser.write("Z")

        elif((cx>426)and(cx<853)and(cy<240)):
            print("Cuadrante   (1,2)")
            ser.write("A")

        elif((cx>426)and(cx<853)and(cy>240)and(cy<480)):
            print("Cuadrante   (2,2)")
            ser.write("Q")

        elif((cx>426)and(cx<853)and(cy>480)and(cy<720)):
            print("Cuadrante   (3,2)")
            ser.write("Z")

        elif((cx>853)and(cy<240)):
            print("Cuadrante   (1,3)")
            ser.write("A")

        elif((cx>853)and(cy>240)and(cy<480)):
            print("Cuadrante   (2,3)")
            ser.write("D")

        elif((cx>853)and(cy>480)):	
            print("Cuadrante   (3,3)")
            ser.write("Z")
        
	'''
        #En que cuadrante estoy para WebCam
        if((cx < 213)and(cy<160)):
            print("Cuadrante   (1,1)")
            ser.write(b"Adelante\n\r")
        elif((cx < 213)and(cy > 160) and (cy<320)):
            print("Cuadrante   (2,1)")
            ser.write(b"Izquierda\n\r")
        elif((cx < 213)and(cy > 230) and (cy<480)):
            print("Atras   (3,1)")
            ser.write(b"Adelante\n\r")
        elif((cx>213)and(cx<426)and(cy<160)):
            print("Cuadrante   (1,2)")
            ser.write(b"Adelante\n\r")
        elif((cx>213)and(cx<426)and(cy>160)and(cy<320)):
            print("Cuadrante   (2,2)")
            ser.write(b"Quieto\n\r")
        elif((cx>213)and(cx<426)and(cy>320)and(cy<480)):
            print("Atras   (3,2)")
            ser.write(b"Adelante\n\r")
        elif((cx>426)and(cy<160)):
            print("Cuadrante   (1,3)")
            ser.write(b"Adelante\n\r")
        elif((cx>426)and(cy>160)and(cy<320)):
            print("Cuadrante   (2,3)")
            ser.write(b"Derecha\n\r")
        elif((cx>426)and(cy>320)):
            print("Cuadrante   (3,3)")
            ser.write(b"Atras\n\r")
	'''   
    cv2.imshow('Output',f)
    

        
ser.write("G")
cv2.destroyAllWindows()
c.release()
ser.close()
