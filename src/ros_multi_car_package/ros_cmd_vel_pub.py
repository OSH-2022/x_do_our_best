#!/usr/bin/python

import itertools
import rospy
from std_msgs.msg import Float64MultiArray #相当于ros中一个double数组
from geometry_msgs.msg import Twist

vel = Twist()
vel.linear.x = 0 #小车移动参数

def distance(x1, y1, x2, y2):
  ans = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)

dis = [[0] * n] * n #定义两点距离的二维数组

def shortest_way(Location, n):
  #找到所给坐标点的最短访问序列，并返回调整过的坐标序列
  min_dis = 10000000000000
  for i in range(0, n):
    for j in range(0, n):
      dis[i][j] = distance(Location[2 * i], Location[2 * i + 1], Location[2 * j], Location[2 * j + 1])
  nums = []
  for i in range(0, n):
    nums[i] = i
  for num in itertools.permutations(nums, n): #逐个生成各个点序号的全排列
    route_dis = 0
    for j in range(0, n - 1):
      route_dis += dis[num[j]][num[j + 1]]
    if route_dis < min_dis:
      min_dis = route_dis
      route = num

  m = 2 * n
  sorted_Location = [[0] * m]
  for i in range(0, n):
    sorted_Location[2 * i] = Location[2 * route[i]]
    sorted_Location[2 * i + 1] = Location[2 * route[i] + 1] #按找到的顺序把Location重排

  sorted_Location[2 * n] = 0
  sorted_Location[2 * n + 1] = 0
  sorted_Location[2 * n + 2] = -1 #最后返回初始位置
  return sorted_Location

def bias(x1, y1, x0, y0, x2, y2):
  a = distance(x1, y1, x0, y0)
  b = distance(x1, y1, x2, y2)
  c = distance(x0, y0, x2, y2)
  rad = (a * a + b * b - c * c) / 2 * a * b #余弦定理
  if rad > 0:
    flag = 1
  else:
    flag = 0
    rad = - rad #计算是往左还是往右偏转
  return flag, rad * 1270 #换算的偏转时间
  

def callback(data):
  global dis
  pub = rospy.Publisher('move', Float64MultiArray, queue_size=100) #把地图发给小车B
  n = 0
  for e in data:
    n = n + 1
    if e == -1:
      break
  n = (n - 1) / 2
  sorted_locations=shortest_way(Location, n) #返回找到的最短路径的坐标序列
  cnt = 0
  while cnt < n:
    if cnt == 0:
      flag, turn_tim = bias(sorted_locations[cnt * 2], sorted_locations[cnt * 2 + 1], -1, 0, sorted_locations[cnt * 2 + 2], sorted_locations[cnt * 2 + 3]) #初始时小车指向为确定
    if cnt > 0:
      flag, turn_tim = bias(sorted_locations[cnt * 2], sorted_locations[cnt * 2 + 1], sorted_locations[cnt * 2 - 2], sorted_locations[cnt * 2 - 1], sorted_locations[cnt * 2], sorted_locations[cnt * 2 + 1]) #按照小车之前方向与需要去的方向的偏差确定转角需要时间
    while turn_tim > 0:
      turn_tim = turn_tim - 1
      vel.linear.x = 0.8
      vel.linear.z = flag
      pub.publish(vel)
      rate.sleep()
    tim = distance(sorted_locations[cnt * 2], sorted_locations[cnt * 2 + 1], sorted_locations[cnt * 2 + 2], sorted_locations[cnt * 2 + 3]) * 112500 #计算移动距离所需要的时间
    while tim > 0:
      tim = tim - 1
      vel.linear.x = 0.8
      vel.linear.z = 0
      pub.publish(vel)
      rate.sleep()

     
def run():
  # Init Node
  rospy.init_node('listener')
  rospy.Subscriber('locations', Float64MultiArray ,callback, queue_size=100)# 接收start信号 回调函数callback
  rospy.spin()

if __name__=='__main__':
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
