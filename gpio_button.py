from gpiozero import LED, Button
from signal import pause

led = LED(21)
button = Button(23)

# LED is off
led.off()

def pressed():
    if led.is_lit:
        led.off()
    else:
        led.on()

button.when_pressed = pressed
pause()


"""
or we can do something like this

button.when_pressed = led.on
button.when_released = led.off

solution from documentation for gpiozero
"""
