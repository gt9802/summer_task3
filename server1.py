import cv2, imutils, socket
import numpy as np
import time
import base64
import threading

BUFF_SIZE = 65536
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

ip ="192.168.43.222"
port = 1234

#binding ip and port number
s.bind((ip,port))

#receives packet from sender and show  using cv2
def recv():
    while True:
        packet,_ = s.recvfrom(BUFF_SIZE)
        data = base64.b64decode(packet,' /')
        npdata = np.fromstring(data,dtype=np.uint8)
        frame = cv2.imdecode(npdata,1)
        cv2.imshow("sender",frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            s.close()
            break

        
#function to send image stream to sender program 
def send():
    #opens webcam
    vid = cv2.VideoCapture(0)
    #set the width t osend image in a single shot of datagram
    WIDTH=400
    #receives datagram on its socket address
    while(vid.isOpened()):
        #starts capturing images
        _,frame = vid.read()
        #resize the image
        frame = imutils.resize(frame,width=WIDTH)
        #encode the image with a jpeg with a quality of 80%
        encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
        #base64 encoding  
        message = base64.b64encode(buffer)
        s.sendto(message,("192.168.43.148",1235))

       

#multithreading
x1 = threading.Thread( target=recv )
x2 = threading.Thread( target=send )

x1.start()
x2.start()

