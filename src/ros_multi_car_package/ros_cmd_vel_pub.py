#!/usr/bin/python

import rospy
from Location_Array import Location_Array
#from geometry_msgs.msg import Twist
from pynput.keyboard import Key, Listener

vel = Twist()
vel.linear.x = 0

def on_press(key):

    try:
        if(key.char == 'w'):
            print("Forward")
            vel.linear.x = 0.8
            vel.angular.z = 0

        if(key.char == 's'):
            print("Backward")
            vel.linear.x = -0.8
            vel.angular.z = 0

        if(key.char == 'a'):
            print("Counter Clockwise")
            vel.linear.x = 0
            vel.angular.z = -0.8

        if(key.char == 'd'):
            print("Clockwise")
            vel.linear.x = 0
            vel.angular.z = 0.8

        return False

    except AttributeError:
        print('special key {0} pressed'.format(key))
        return False

def on_release(key):
    vel.linear.x = 0
    vel.angular.z = 0

    return False

def callback():
pub = rospy.Publisher('map', Location_Array, queue_size=10) #把地图发给小车B
while not rospy.is_shutdowm();
     msg=Location_Array()
     msg.size=5
     msg.Location=[0,0,0,0,0,0,0,0,0,0]
     pub.publish(msg)
     rate.sleep()
     
def run():
# Init Node
rospy.init_node('my_cmd_vel_publisher')
rospy.Subscriber('start', , queue_size=10)# 接收start信号
rospy.spin()

if __name__=='__main__'
  run()
# Set rate
#rate = rospy.Rate(10)

#listener = Listener(on_release=on_release, on_press = on_press)

#while not rospy.is_shutdown():
#    print(vel.linear.x)
#    pub.publish(vel)
#    vel.linear.x = 0
#    vel.angular.z = 0
#    rate.sleep()

#    if not listener.running:
 #       listener = Listener(on_release=on_release, on_press = on_press)
 #       listener.start()
