#!/usr/bin/python

import time
import cv2
import numpy as np

from pivideostream import PiVideoStream
from Adafruit_PWM_Servo_Driver import PWM


def rotate_image(image):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, 180, 1.0)
    image = cv2.warpAffine(image, M, (w, h))
    return image

def main():
    pwm = PWM(0x40)
    pwm.setPWMFreq(100)
    vs = PiVideoStream(resolution=(640,480)).start()
    time.sleep(1.0)
    frame = vs.read()
    prvs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame)
    hsv[...,1] = 255
    mode = 0
    speed = 0
    steer = 0

    while True:
        frame = vs.read()
        #frame = rotate_image(frame)
        next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if mode == 3:
            flow = cv2.calcOpticalFlowFarneback(prvs,next, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
            hsv[...,0] = ang*180/3.14/2
            hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
            bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

        cv2.putText(frame, "Speed: {}, Steer: {}".format(speed, steer),
            (10,20), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 0, 0))
        if mode == 1:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if mode == 2:
            frame = cv2.Canny(frame, 20, 100)
        if mode == 3:
            cv2.imshow("Frame", bgr)
        else:
            cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("f"):
            mode = 3
        if key == ord("e"):
            mode = 2
        if key == ord("g"):
            mode = 1
        if key == ord("c"):
            mode = 0
        if key == ord("l"):
            pwm.setPWM(0, 0, 500)
        if key == ord("r"):
            pwm.setPWM(0, 0, 300)
        if key == 81: # left
            if steer > -1:
                steer = steer - 0.1
        if key == 83: # right
            if steer < 1:
                steer = steer + 0.1
        if key == 82: # up
            if speed < 1:
                speed = speed + 0.1
        if key == 84: # down
            if steer > -1:
                speed = speed - 0.1
        if key == ord("s"):
            speed = 0
            steer = 0
        pwm.setPWM(0, 0, 500 + int(speed*100))
        pwm.setPWM(2, 0, 670 - int(steer*100))
        prvs = next

    cv2.destroyAllWindows()
    vs.stop()

if __name__ == '__main__':
    main()
