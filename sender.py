import cv2, imutils, socket
import numpy as np
import time
import base64
import threading
BUFF_SIZE = 65536
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

ip = "192.168.43.148"

port = 1235

s.bind((ip,port))


def send():
    vid = cv2.VideoCapture(0)
    encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
    message = base64.b64encode(buffer)
    s.sendto(message,("192.168.43.222",1234))


def recv():
    while True:
        packet,_ = s.recvfrom(BUFF_SIZE)
        data = base64.b64decode(packet,' /')
        npdata = np.fromstring(data,dtype=np.uint8)
        frame = cv2.imdecode(npdata,1)
        cv2.imshow("server",frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            s.close()
            cv2.destroyAllWindows()

x1 = threading.Thread( target=send )
x2 = threading.Thread( target=recv )

x1.start()
x2.start()

