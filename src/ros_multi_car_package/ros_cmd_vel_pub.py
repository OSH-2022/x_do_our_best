#!/usr/bin/python

import rospy
from Location_Array import Location_Array
from std_msgs.msg import int

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
rospy.init_node('listen&pub')
rospy.Subscriber('start', int ,callback,queue_size=10)# 接收start信号 回调函数callback
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
