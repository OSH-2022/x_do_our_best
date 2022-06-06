#!/usr/bin/env python
#!coding=utf-8

import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
# from PIL import Image as PIL
 
def callback(data):
 
    global bridge
    img_pub = rospy.Publisher('image_raw', Image, queue_size=1)  # 发布的话题：'image_raw'
    cv_img = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    cv_img = cv_img - 1
    cv_img90 = np.rot90(cv_img, -1)  #  处理图片
 
    data90 = bridge.cv2_to_imgmsg(cv_img90, encoding="bgr8")
 
    img_pub.publish(data90)  # 发布图片
 
    rospy.loginfo(cv_img90[0][0])
 

def displayWebcam():
    rospy.init_node('webcam_display', anonymous=True)  # 创建节点的名称：'webcam_display'
    global bridge
    bridge = CvBridge()
    rospy.Subscriber('image_raw0', Image, callback)  #  订阅的话题： 'image_raw0' 
    rospy.spin()
 
if __name__ == '__main__':
    displayWebcam()
