import pigpio
import signal

LED_GPIO_PIN = 21
BUTTON_GPIO_PIN = 23
pi = pigpio()

# verify the LED is initally off
pi.set_mode(LED_GPIO_PIN, pigpio.OUTPUT)
pi.write(LED_GPIO_PIN, 0)

# set up the input
pi.set_mode(LED_GPIO_PIN, pigpio.INPUT)
pi.set_pull_up_down(BUTTON_GPIO_PIN, pigpio.PUD_UP)
# button will only register a push every .1 seconds
pi.set_glitch_filter(BUTTON_GPIO_PIN, 100000) 

# callback function for when the button is pressed
def pressed():
    led_state = pi.read(LED_GPIO_PIN)
    if led_state == 1:
        pi.write(LED_GPIO_PIN, 0)
    else:
        pi.write(LED_GPIO_PIN, 1)

pi.callback(BUTTON_GPIO_PIN, pigpio.FALLING_EDGE, pressed)
signal.pause() # make sure our program doesn't exit 