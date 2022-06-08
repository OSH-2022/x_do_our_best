#include <rtthread.h>
  #include <rtdevice.h>
  #include "motors.h"

  #define PWM_DEV_NAME "pwm3"

  MotorControl::MotorControl(int fl_engine, int fl_turn)
  {
     this->maxSpd = 500000;
     this->moveFactor = 1.0;
     this->turnFactor = 3.0;

     this->fl_engine = fl_engine;
     this->fl_turn = fl_turn;
 }

 void MotorControl::initMotors() {
     /* 查找设备 */
     this->pwm_dev = (struct rt_device_pwm *)rt_device_find(PWM_DEV_NAME);
     if (pwm_dev == RT_NULL)
     {
         rt_kprintf("pwm sample run failed! can't find %s device!\n", PWM_DEV_NAME);
     }
     rt_kprintf("pwm found %s device!\n", PWM_DEV_NAME);
     rt_pwm_set(pwm_dev, fl_engine, maxSpd, 0);
     rt_pwm_enable(pwm_dev, fl_engine); //前进驱动的pwm

     rt_pwm_set(pwm_dev, fl_turn, maxSpd, 0);
     rt_pwm_enable(pwm_dev, fl_turn); //控制舵机的pwm
 }

 // 小车运动
 void MotorControl::moveBot(float spd, float bias) {
     float sE = spd * maxSpd;

     if(bias != 0)
     {
         rotateBot(spd, bias);
     }

     rt_pwm_set(pwm_dev, fl_engine, maxSpd, (rt_int32_t)sE);

     rt_thread_mdelay(1);
}


// 小车旋转
void MotorControl::rotateBot(float spd, float bias) {
    float b = bias * maxSpd;
    float sE = spd * maxSpd;

    rt_pwm_set(pwm_dev, fl_turn, maxSpd, (rt_int32_t)b);
    rt_pwm_set(pwm_dev, fl_engine, maxSpd, (rt_int32_t)sE);

    rt_thread_mdelay(1);
}

//Turn off both motors
void MotorControl::stopMotors()
{
    rt_pwm_set(pwm_dev, fl_engine, maxSpd, 0);
    rt_pwm_set(pwm_dev, fl_turn, maxSpd, 0);
}
