#include <rtthread.h>
#include <rtdevice.h>
#include "motors.h"

#define PWM_DEV_NAME "pwm3"

  MotorControl::MotorControl(int fl_for, int fl_back,
                             int fr_for, int fr_back)
  {
     this->maxSpd = 500000;
     this->moveFactor = 1.0;
     this->turnFactor = 3.0;

     this->fl_for = fl_for;
     this->fl_back = fl_back;

     this->fr_for = fr_for;
     this->fr_back = fr_back;
 }

 void MotorControl::initMotors() {
     /* 查找设备 */
     this->pwm_dev = (struct rt_device_pwm *)rt_device_find(PWM_DEV_NAME);
     if (pwm_dev == RT_NULL)
     {
         rt_kprintf("pwm sample run failed! can't find %s device!\n", PWM_DEV_NAME);
     }
     rt_kprintf("pwm found %s device!\n", PWM_DEV_NAME);
     rt_pwm_set(pwm_dev, fl_for, maxSpd, 0);
     rt_pwm_enable(pwm_dev, fl_for);

     rt_pwm_set(pwm_dev, fl_back, maxSpd, 0);
     rt_pwm_enable(pwm_dev, fl_back);

     rt_pwm_set(pwm_dev, fr_for, maxSpd, 0);
     rt_pwm_enable(pwm_dev, fr_for);

     rt_pwm_set(pwm_dev, fr_back, maxSpd, 0);
     rt_pwm_enable(pwm_dev, fr_back);
 }

 // 小车运动
 void MotorControl::moveBot(float spd, float bias) {
     float sL = spd * maxSpd;
     float sR = spd * maxSpd;
     int dir = (spd > 0) ? 1 : 0;

     if(bias != 0)
     {
         rotateBot((bias > 0) ? 1 : 0, bias);
         return;
     }

     if( sL < -moveFactor * maxSpd)
     {
         sL = -moveFactor * maxSpd;
     }
     if( sL > moveFactor * maxSpd)
     {
         sL = moveFactor * maxSpd;
     }

     if( sR < -moveFactor * maxSpd)
     {
         sR = -moveFactor * maxSpd;
     }
     if( sR > moveFactor * maxSpd)
     {
         sR = moveFactor * maxSpd;
     }

     if (sL < 0)
     {
         sL *= -1;
     }

     if (sR < 0)
     {
         sR *= -1;
     }

     rt_kprintf("Speed Left: %ld\n", (rt_int32_t)sL);
     rt_kprintf("Speed Right: %ld\n", (rt_int32_t)sR);

     if(dir)
     {
         rt_pwm_set(pwm_dev, fl_for, maxSpd, (rt_int32_t)sL);
         rt_pwm_set(pwm_dev, fl_back, maxSpd, 0);
         rt_pwm_set(pwm_dev, fr_for, maxSpd, (rt_int32_t)sR);
         rt_pwm_set(pwm_dev, fr_back, maxSpd, 0);
     }
     else
     {
         rt_pwm_set(pwm_dev, fl_for, maxSpd, 0);
         rt_pwm_set(pwm_dev, fl_back, maxSpd, (rt_int32_t)sL);
         rt_pwm_set(pwm_dev, fr_for, maxSpd, 0);
         rt_pwm_set(pwm_dev, fr_back, maxSpd, (rt_int32_t)sR);
     }

    rt_thread_mdelay(1);
}


// 小车旋转
void MotorControl::rotateBot(int dir, float spd) {
    float s = spd * maxSpd;
    if (dir < 0)
    {
        s *= -1;
    }
    if(dir)
    {
        // Clockwise
        rt_pwm_set(pwm_dev, fl_for, maxSpd, (rt_int32_t)s);
        rt_pwm_set(pwm_dev, fl_back, maxSpd, 0);
        rt_pwm_set(pwm_dev, fr_for, maxSpd, 0);
        rt_pwm_set(pwm_dev, fr_back, maxSpd, (rt_int32_t)s);
    }
    else
    {
        // Counter Clockwise
        rt_pwm_set(pwm_dev, fl_for, maxSpd, 0);
        rt_pwm_set(pwm_dev, fl_back, maxSpd, (rt_int32_t)s);
        rt_pwm_set(pwm_dev, fr_for, maxSpd, (rt_int32_t)s);
        rt_pwm_set(pwm_dev, fr_back, maxSpd, 0);
    }
    rt_thread_mdelay(1);
}

//Turn off both motors
void MotorControl::stopMotors()
{
    rt_pwm_set(pwm_dev, fl_for, maxSpd, 0);
    rt_pwm_set(pwm_dev, fl_back, maxSpd, 0);
    rt_pwm_set(pwm_dev, fr_for, maxSpd, 0);
    rt_pwm_set(pwm_dev, fr_back, maxSpd, 0);
}
