 #include <rtthread.h>
 #include <rtdevice.h>
 #include <board.h>
 #include <time.h>

 #include <ros.h>
 #include <std_msgs/Float64.h>
 #include <geometry_msgs/Twist.h>
 #include "motors.h"

 #define PERIOD 3000000

static void MX_TIM3_Init(void);
static void MX_GPIO_Init(void);

TIM_HandleTypeDef htim3;

ros::NodeHandle  nh;
MotorControl mtr(1, 2, 3, 4);   //Motor

bool msgRecieved = false;
float velX = 0, turnBias = 0;
char stat_log[200];

// 接收到命令时的回调函数
void velCB( const geometry_msgs::Twist& twist_msg)
{
  velX = twist_msg.linear.x;
  turnBias = twist_msg.angular.z;
  msgRecieved = true;
}
//Subscriber
ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", velCB );

//Publisher
std_msgs::Float64 velX_tmp;
std_msgs::Float64 turnBias_tmp;
std_msgs::Float64 begin_temp;
ros::Publisher xv("vel_x", &velX_tmp);
ros::Publisher xt("turn_bias", &turnBias_tmp);
ros::Publisher start("start", &begin_temp);  //小车二开始运动的信号

clock_t start_time, test_time;

static void rosserial_thread_entry(void *parameter)
{
    //Init motors, specif>y the respective motor pins
    mtr.initMotors();

    //Init node>
    nh.initNode();

    // 订阅了一个话题 /cmd_vel 接收控制指令
    nh.subscribe(sub);

    // 发布了一个话题 /vel_x 告诉 ROS 小车速度
    nh.advertise(xv);

    // 发布了一个话题 /turn_bias 告诉 ROS 小车的旋转角速度
    nh.advertise(xt);

    // 发布了一个话题 /begin running 告诉 ROS 小车二开始跑
    nh.advertise(start);

    mtr.stopMotors();

    //开始时刻
    start_time = clock();

    velX = 5;
    turnBias = 2;
    tr.moveBot(velX, turnBias);     //让第一辆小车绕圈

    while (1)
    {
      // 如果接收到了控制指令
    //   if (msgRecieved)
    //   {
    //     velX *= mtr.maxSpd;
    //     mtr.moveBot(velX, turnBias);
    //     msgRecieved = false;
    //   }

      velX_tmp.data = velX;
      turnBias_tmp.data = turnBias/mtr.turnFactor;

      // 更新话题内容
      xv.publish( &velX_tmp );
      xt.publish( &turnBias_tmp );
      start.publish( &begin_temp );

      nh.spinOnce();

      test_time = clock();//获取当前时刻
      if(test_time - start_time < PERIOD){  //运动一定时间后，修改publisher，使小车二开始运动
          begin_temp = 1;
      }
    }
}

int main(void)
{
    MX_GPIO_Init();
    uint8_t ch1 = rt_pin_get("PA.6");
    uint8_t ch2 = rt_pin_get("PA.7");
    uint8_t ch3 = rt_pin_get("PB.0");
    uint8_t ch4 = rt_pin_get("PB.1");

    rt_pin_mode(ch1, PIN_MODE_OUTPUT);
    rt_pin_mode(ch2, PIN_MODE_OUTPUT);
    rt_pin_mode(ch3, PIN_MODE_OUTPUT);
    rt_pin_mode(ch4, PIN_MODE_OUTPUT);
    MX_TIM3_Init();
    MotorControl m = MotorControl(1, 2, 3, 4);
    m.initMotors();
    m.moveBot(2000, 0);
    nh.getHardware()->setConnection("192.168.1.210", 11411);
    nh.initNode();
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

static void MX_GPIO_Init(void)
{

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

}
