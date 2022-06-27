#include <rtthread.h>
#include <rtdevice.h>
#include "motors.h"

#define SAMPLE_UART_NAME       "uart3"

//定义串口
static rt_device_t serial;

MotorControl::MotorControl(int fl_engine, int fl_turn)
{
    this->maxSpd = 500000;
    this->moveFactor = 1.0;
    this->turnFactor = 3.0;

    this->fl_engine = fl_engine;
    this->fl_turn = fl_turn;
}

void MotorControl::initMotors() {
    /* 以中断接收及轮询发送模式打开串口设备 */
    rt_device_open(serial, RT_DEVICE_FLAG_INT_RX);
    this->serial = serial;
}

// 小车运动
void MotorControl::moveBot(float spd, float bias) {
    float sE = spd * maxSpd;

    if (bias != 0)
    {
        rotateBot(spd, bias);
    }

    if (sE > 0) {
        char str1[] = "BUPD";
        char str2[] = "BUPU"
            rt_device_write(serial, 0, str1, (sizeof(str1) - 1));
        rt_thread_mdelay(1);
        rt_device_write(serial, 0, str2, (sizeof(str2) - 1));
    }
    else if (sE < 0) {
        char str[] = "BDND"
            char str2[] = "BDNU"
            rt_device_write(serial, 0, str1, (sizeof(str1) - 1));
        rt_thread_mdelay(1);
        rt_device_write(serial, 0, str2, (sizeof(str2) - 1));
    }


    rt_thread_mdelay(1);
}


// 小车旋转
void MotorControl::rotateBot(float spd, float bias) {
    if (bias > 0) {
        char str1[] = "BLFD";
        char str2[] = "BLFU"
            rt_device_write(serial, 0, str1, (sizeof(str1) - 1));
        rt_thread_mdelay(1);
        rt_device_write(serial, 0, str2, (sizeof(str2) - 1));
    }
    else if (bias < 0) {
        char str[] = "BRTD"
            char str2[] = "BRTU"
            rt_device_write(serial, 0, str1, (sizeof(str1) - 1));
        rt_thread_mdelay(1);
        rt_device_write(serial, 0, str2, (sizeof(str2) - 1));
    }
}

