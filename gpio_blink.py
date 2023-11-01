from gpiozero import LED # not sure if this is proper
from time import sleep 

led = LED(21)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
