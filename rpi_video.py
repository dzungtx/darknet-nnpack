from subprocess import Popen, PIPE
import threading
from time import sleep
import os, fcntl
import cv2

cam = cv2.VideoCapture(1)

#spawn darknet process
yolo_proc = Popen(["./darknet",
                   "detect",
                   "./cfg/yolov3-tiny.cfg",
                   "./yolov3-tiny.weights",
                   "-thresh","0.1"],
                   stdin = PIPE, stdout = PIPE)

fcntl.fcntl(yolo_proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

while True:
    stdout = yolo_proc.stdout.read()

    if stdout is None:
        sleep(1)
        continue

    stdout = stdout.decode('ascii')

    if 'Enter Image Path' in stdout:
        ret, frame = cam.read()
        if not ret:
            print('Can not connect to camera')
            break
        cv2.imwrite('frame.jpg', frame)
        
        yolo_proc.stdin.write('frame.jpg\n'.encode('ascii'))
        yolo_proc.stdin.flush()
 
    if len(stdout.strip())>0:
        print('get %s' % stdout)

