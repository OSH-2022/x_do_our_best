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
MotorControl mtr(1, 2);   //Motor

bool msgRecieved = false;
int start = 0;
float velX = 0, turnBias = 0;
char stat_log[200];
float length[10][10] = { 0 };
float total = 0;
int order[10] = { 0 };
void Permutation(int m, int n, int arr[], int temp[])
{
	int i, temp_total = 0;
	//递归到底层
	if (m >= n)
	{
		temp_total += length[0][arr[0]];
		for (i = 1; i < n; i++)
		{//按这个点顺序计算总路径长度
			temp_total += length[arr[i - 1]][arr[i]];
		}
		if (!total)
			total = temp_total;
		else if (temp_total < total) {
			total = temp_total;
			for (int j = 0; j < n; j++) {
				order[j] = arr[j];
			}
		}
	}
	else
	{
		for (i = 0; i < n; i++)
		{
			if (temp[i] == 0)
			{
				temp[i] = 1;
				arr[m] = i + 1;
				//递归到下一层
				Permutation(m + 1, n, arr, temp);
				//保证递归后保持上一层的顺序
				temp[i] = 0;
			}
		}
	}
}

void ShortestWay(float*location, int n) {

	//从原点出发 数组前两个数为0
	for (int i = 0; i < n; i++) {
		for (int j = 1; j < n; j++) {
			length[i][j] = (location[i] - location[j])*(location[i] - location[j]) +
				(location[i + 1] - location[j + 1])*(location[i + 1] - location[j + 1]);
		}
	}

	int arr[10] = { 1,2,3,4,5,6,7,8,9,10 };//经过点的顺序
	int temp[10] = { 0 };
	Permutation(0, n, arr, temp);

}
// 接收到命令时的回调函数
/*void velCB( const geometry_msgs::Twist& twist_msg)
{
  velX = twist_msg.linear.x;
  turnBias = twist_msg.angular.z;
  msgRecieved = true;
}
*/

void startRun(const my_topic::Location_Array::ConstPtr& msg) {
	int size = msg.size;
	float location[10] = msg.location;
	ShortestWay(location, size);
}
//Subscriber
//订阅目标地点的消息
ros::Subscriber<my_topic::Location_Array> sub("map", 1，startRun );

//Publisher
std_msgs::Float64 velX_tmp;
std_msgs::Float64 turnBias_tmp;
std_msgs::Float64 begin_temp;
ros::Publisher xv("vel_x", &velX_tmp);
ros::Publisher xt("turn_bias", &turnBias_tmp);


static void rosserial_thread_entry(void *parameter)
{
    //Init motors, specif>y the respective motor pins
    mtr.initMotors();

    // 设置 ROS 的 IP 端口号
    nh.getHardware()->setConnection("192.168.125.21", 11411);

    //Init node>
    nh.initNode();

    // 订阅了一个话题 /cmd_vel 接收控制指令
    nh.subscribe(sub);

    // 发布了一个话题 /vel_x 告诉 ROS 小车速度
    nh.advertise(xv);

    // 发布了一个话题 /turn_bias 告诉 ROS 小车的旋转角速度
    nh.advertise(xt);

   
    mtr.stopMotors();

    //开始时刻
  
    velX = 0;
    turnBias = 0;

    while (1)
    {
      // 如果接收到了控制指令
       if (msgRecieved)
       {
         velX *= mtr.maxSpd;
         mtr.moveBot(velX, turnBias);
         msgRecieved = false;
       }

      velX_tmp.data = velX;
      turnBias_tmp.data = turnBias/mtr.turnFactor;

      // 更新话题内容
      xv.publish( &velX_tmp );
      xt.publish( &turnBias_tmp );
 
      nh.spinOnce();

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
