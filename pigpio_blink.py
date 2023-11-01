import pigpio 
from time import sleep

GPIO_PIN = 21
pi = pigpio.pi()
pi.set_mode(GPIO_PIN, pigpio.OUTPUT)

while True:
    pi.write(GPIO_PIN, 1) # 1 -> High: Turn to LED on
    sleep(1)
    pi.write(GPIO_PIN, 0) # 0 -> Low: Turn to LED off
    sleep(1)
