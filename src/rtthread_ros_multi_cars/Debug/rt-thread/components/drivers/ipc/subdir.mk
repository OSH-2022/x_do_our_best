################################################################################
# 自动生成的文件。不要编辑！
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../rt-thread/components/drivers/ipc/completion.c \
../rt-thread/components/drivers/ipc/dataqueue.c \
../rt-thread/components/drivers/ipc/pipe.c \
../rt-thread/components/drivers/ipc/ringblk_buf.c \
../rt-thread/components/drivers/ipc/ringbuffer.c \
../rt-thread/components/drivers/ipc/waitqueue.c \
../rt-thread/components/drivers/ipc/workqueue.c 

OBJS += \
./rt-thread/components/drivers/ipc/completion.o \
./rt-thread/components/drivers/ipc/dataqueue.o \
./rt-thread/components/drivers/ipc/pipe.o \
./rt-thread/components/drivers/ipc/ringblk_buf.o \
./rt-thread/components/drivers/ipc/ringbuffer.o \
./rt-thread/components/drivers/ipc/waitqueue.o \
./rt-thread/components/drivers/ipc/workqueue.o 

C_DEPS += \
./rt-thread/components/drivers/ipc/completion.d \
./rt-thread/components/drivers/ipc/dataqueue.d \
./rt-thread/components/drivers/ipc/pipe.d \
./rt-thread/components/drivers/ipc/ringblk_buf.d \
./rt-thread/components/drivers/ipc/ringbuffer.d \
./rt-thread/components/drivers/ipc/waitqueue.d \
./rt-thread/components/drivers/ipc/workqueue.d 


# Each subdirectory must supply rules for building sources it contributes
rt-thread/components/drivers/ipc/%.o: ../rt-thread/components/drivers/ipc/%.c
	arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 -O0 -ffunction-sections -fdata-sections -Wall  -g -gdwarf-2 -DSOC_FAMILY_STM32 -DSOC_SERIES_STM32F4 -DUSE_HAL_DRIVER -DSTM32F407xx -I"D:\RT-ThreadStudio\workspace\rtthread_ros\drivers" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\drivers\include" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\drivers\include\config" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\libraries\CMSIS\Device\ST\STM32F4xx\Include" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\libraries\CMSIS\Include" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\libraries\CMSIS\RTOS\Template" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\libraries\STM32F4xx_HAL_Driver\Inc" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\libraries\STM32F4xx_HAL_Driver\Inc\Legacy" -I"D:\RT-ThreadStudio\workspace\rtthread_ros" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\applications" -I"D:\RT-ThreadStudio\workspace\rtthread_ros" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\packages\at_device-latest\class\esp8266" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\packages\at_device-latest\inc" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\packages\rosserial-melodic-latest\port" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\packages\rosserial-melodic-latest\src" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\packages\rosserial-melodic-latest" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\drivers\include" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\finsh" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\libc\compilers\common" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\libc\compilers\newlib" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\libc\cplusplus" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\libc\posix\io\poll" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\libc\posix\io\stdio" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\libc\posix\ipc" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\net\at\at_socket" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\net\at\include" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\net\netdev\include" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\net\sal\impl" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\net\sal\include\socket\sys_socket" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\net\sal\include\socket" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\components\net\sal\include" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\include" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\libcpu\arm\common" -I"D:\RT-ThreadStudio\workspace\rtthread_ros\rt-thread\libcpu\arm\cortex-m4" -include"D:\RT-ThreadStudio\workspace\rtthread_ros\rtconfig_preinc.h" -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -c -o "$@" "$<"

