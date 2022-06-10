 #include <rtthread.h>
 #include <rtdevice.h>
 #include <board.h>
 #include <time.h>

 #include <ros.h>
 #include <std_msgs/Float64.h>
 #include <geometry_msgs/Twist.h>
 #include "motors.h"
 #include "ros/ros.h"
 #include "std_msgs/Float64MultiArray.h"

 #define PERIOD 3000000

static void MX_TIM3_Init(void);
static void MX_GPIO_Init(void);

TIM_HandleTypeDef htim3;

ros::NodeHandle  nh;
MotorControl mtr(1, 2);   //Motor

bool msgRecieved = false;
float velX = 0, turnBias = 0;
char stat_log[200];
int start = 0;
// 接收到命令时的回调函数
void velCB( const geometry_msgs::Twist& twist_msg)
{
  velX = twist_msg.linear.x;
  turnBias = twist_msg.angular.z;
  msgRecieved = true;
}
//Publisher
ros::Publisher<std_msgs::Float64MultiArray> locations("locations", 1000);

std_msgs::Float64 velX_tmp;
std_msgs::Float64 turnBias_tmp;
std_msgs::Float64 begin_temp;
ros::Publisher xv("vel_x", &velX_tmp);
ros::Publisher xt("turn_bias", &turnBias_tmp);

clock_t start_time, test_time;

static void rosserial_thread_entry(void *parameter)
{
    //Init motors, specif>y the respective motor pins
    mtr.initMotors();

    // 设置 ROS 的 IP 端口号
    nh.getHardware()->setConnection("192.168.125.21", 11411);

    //Init node>
    nh.initNode();



    // 发布了一个话题 /vel_x 告诉 ROS 小车速度
    nh.advertise(xv);

    // 发布了一个话题 /turn_bias 告诉 ROS 小车的旋转角速度
    nh.advertise(xt);

  
    mtr.stopMotors();

    //开始时刻
    start_time = clock();

    velX = 5;
    turnBias = 2;
    

    while (1)
    {
      mtr.moveBot(velX, turnBias);     //让第一辆小车绕圈

      velX_tmp.data = velX;
      turnBias_tmp.data = turnBias / mtr.turnFactor;

      // 更新话题内容
      xv.publish( &velX_tmp );
      xt.publish( &turnBias_tmp );
  
      test_time = clock();//获取当前时刻
      if(test_time - start_time < PERIOD){  //运动一定时间后，修改publisher，使小车二开始运动
          std_msgs::Float64MultiArray msg; #相当于ros中一个double数组
          double LocationArray[11] = {0, 0, 1.2, 2.4, 5.4, 6.2, 1.6, 4.8, 2.5, 6.3, 2.8, 3.6, -1};
          msg.data = LocationArray;
          // 发布了一个话题告诉location, 表示各个需要消毒的坐标
          locations.publish(msg);
      }
	    nh.spinOnce();
    }
}

int main(void)
{
    MotorControl m = MotorControl(1, 2, 3, 4);
    m.initMotors();
    m.moveBot(2000, 0);
    nh.getHardware()->setConnection("192.168.1.210", 11411);
    nh.initNode();
    std_msgs::Float64MultiArray msg; //std_msgs::String msg;
    
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

/**
  * @brief TIM3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM3_Init(void)
{

  /* USER CODE BEGIN TIM3_Init 0 */

  /* USER CODE END TIM3_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM3_Init 1 */

  /* USER CODE END TIM3_Init 1 */
  htim3.Instance = TIM3;
  htim3.Init.Prescaler = 71;
  htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim3.Init.Period = 50000;
  htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
  if (HAL_TIM_Base_Init(&htim3) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim3, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_Init(&htim3) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim3, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 500;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.Pulse = 3000;
  if (HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_2) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.Pulse = 400;
  if (HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_3) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.Pulse = 2000;
  if (HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_4) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM3_Init 2 */

  /* USER CODE END TIM3_Init 2 */
  HAL_TIM_MspPostInit(&htim3);

}

