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
    
 private:
     //¶¨Òå´®¿Ú
     static rt_device_t serial;
};
