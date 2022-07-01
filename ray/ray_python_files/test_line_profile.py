import time
import profile

@profile
def fun():
    a = 0
    b = 0
    for i in range(100000):
        a = a + i * i

    for i in range(3):
        b += 1
        time.sleep(0.1)

    return a + b


fun()
