#include <rtthread.h>

 class MotorControl {
   public:
     //Var
     rt_uint32_t  maxSpd;
     float moveFactor;
     float turnFactor;

    MotorControl(int fl_for, int fl_back,
                 int fr_for, int fr_back);
    void initMotors();
    void rotateBot(int dir, float spd);
    void moveBot(float spd, float bias);
    void stopMotors();
  private:
    struct rt_device_pwm *pwm_dev;
    //The pins
    int fl_for;
    int fl_back;
    int fr_for;
    int fr_back;
    int bl_for;
    int bl_back;
    int br_for;
    int br_back;
};
