#!/usr/bin/python

import rospy
from std_msgs.msg import String

import time
from Adafruit_PWM_Servo_Driver import PWM

pwm = PWM(0x40)

def cb(data):
    global pwm
    d = data.data.split(' ')
    throttle = int(d[0])
    steer = int(d[1])
    pwm.setPWM(0, 0, 500 + throttle)
    pwm.setPWM(2, 0, 670 + steer)
    rospy.loginfo(data.data)

def listener():
    global pwm
    pwm.setPWMFreq(100)
    rospy.init_node("listener")
    rospy.Subscriber("drivedata", String, cb)
    rospy.spin()

if __name__ == '__main__':
    listener()
