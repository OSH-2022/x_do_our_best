#include <rtthread.h>

class MotorControl {
public:
    //Var
    rt_uint32_t  maxSpd;
    float moveFactor;
    float turnFactor;

    MotorControl(int fl_engine, int fl_turn);
    void initMotors();
    void rotateBot(float spd, float bias);
    void moveBot(float spd, float bias);
    void stopMotors();
private:
    struct rt_device_pwm* pwm_dev;
    //The pins
    int fl_engine;
    int fl_turn;
};
