#include <rtthread.h>
 #include <rtdevice.h>
 #include <board.h>

 #include <ros.h>
 #include <std_msgs/Float64.h>
 #include <geometry_msgs/Twist.h>
 #include "motors.h"

ros::NodeHandle  nh; //开启一个节点（node handle）
MotorControl mtr(1, 2);   //Motor

bool msgRecieved = false;
float velX = 0, turnBias = 0; //前进速度和偏转角度
char stat_log[200];

// 接收到命令时的回调函数
void velCB( const geometry_msgs::Twist& twist_msg)
{
  velX = twist_msg.linear.x; //设置前进速度，linear.x指向机器人前方
  //设置偏转角度，angular.z代表平面机器人的角速度，因为此时z轴为旋转轴
  turnBias = twist_msg.angular.z;
  msgRecieved = true; //标记接收到了消息
}
//Subscriber
//创建一个Subscriber，消息管道为cmd_vel,注册回调函数为velCB
ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", velCB );

//Publisher
std_msgs::Float64 velX_tmp;
std_msgs::Float64 turnBias_tmp;
ros::Publisher xv("vel_x", &velX_tmp);//发送当前速度
ros::Publisher xt("turn_bias", &turnBias_tmp);//发送当前偏转角度

static void rosserial_thread_entry(void *parameter)
{
    //Init motors, specify the respective motor pins
    mtr.initMotors();

    //Init node
    nh.initNode();

    // 订阅了一个话题 /cmd_vel 接收控制指令
    nh.subscribe(sub);

    // 发布了一个话题 /vel_x 告诉 ROS 小车速度
    nh.advertise(xv);

    // 发布了一个话题 /turn_bias 告诉 ROS 小车的旋转角速度
    nh.advertise(xt);

    mtr.stopMotors();

    while (1)
    {
      // 如果接收到了控制指令
      if (msgRecieved)
      {
        velX *= mtr.maxSpd; //转换速度
        mtr.moveBot(velX, turnBias);
        msgRecieved = false; //设置结束把标志置false
      }

      velX_tmp.data = velX;
      turnBias_tmp.data = turnBias/mtr.turnFactor; //设置publisher值

      // 更新话题内容
      xv.publish( &velX_tmp );
      xt.publish( &turnBias_tmp );

      nh.spinOnce(); //回调处理函数
    }
}

int main(void)
{
    // 启动一个线程用来和 ROS 通信
    rt_thread_t thread = rt_thread_create("rosserial",     rosserial_thread_entry, RT_NULL, 2048, 8, 10);
    if(thread != RT_NULL)
    {
        rt_thread_startup(thread);
        rt_kprintf("[rosserial] New thread rosserial\n");
    }
    else
    {
        rt_kprintf("[rosserial] Failed to create thread rosserial\n");
    }
    return RT_EOK;
}
