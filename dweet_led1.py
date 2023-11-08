import json
import signal
import os
import sys
import logging
from gpiozero import Device, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from uuid import uuid1
import requests

# Constant global variables
LED_GPIO_PIN = 21
THING_FILE_NAME = "thing_name.txt"
URL = "https://dweet.io" # Dweet service API

# Non-Constant Global Variables
last_led_state = None
thing_name = None # The name held in the THING_NAME_FILE
led = None # GPIOZero LED instance

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

Device.pin_factory = PiGPIOFactory() # boiler plate code 

def init_led():
    global led
    led = LED(LED_GPIO_PIN)
    led.off()

def resolve_thing_name(thing_file):
    name = None
    # if file exists, grab the unique id from the file
    if os.path.exists(thing_file):
        with open(thing_file, "r") as file_handle: # RAII
            name = file_handle.read()
            logger.info(f"Thing name {name} loaded from file {thing_file}.")
            return name.strip()
    else: # file foes not exist, create unique identifier and store in file
        name = str(uuid1())[:8] #unique identifier
        logger.info(f"Created new thing name {name}")

        with open(thing_file, "w") as f:
            f.write(name)
    
    return name

def get_lastest_dweet():
    resource = URL + f"/dweet/for/{thing_name}"
    logger.info(f"Getting the last dweet from {resource}")

    request = requests.get(resource)

    if request.status_code == 200:
        dweet = request.json()
        logger.info(f"Last dweet for thing was {dweet}")

        dweet_content = None
        if dweet["this"] == "succeeded":
            dweet_content = dweet["with"]["content"]
            print(f"dweet content: {dweet_content}")
        
        return dweet_content
    else:
        print(f"unable to retrieve dweet with code: {request.status_code}")
    return None
    
def poll_dweets_forever(delay_sec=10):
    """poll dweet.io for dweets about our thing"""
    #while True:
    dweet = get_lastest_dweet()
    sleep(delay_sec)
    if dweet is not None:
        process_dweet(dweet) 

def process_dweet(dweet):
    global last_led_state

    if not "state" in dweet:
        logging.info("Dweet content does not contain a 'state' key")
        return 
    
    led_state = dweet["state"]

    if requested_state == last_led_state:
        logging.info("LED is already in state {requested_state}")
        return
    
    # at this point, the led is not in the requested state

    if requested_state == "on":
        led.on()
    elif requested_state == "blinking":
        led.blink()
    else: # want to turn the LED off or to som unexpected state
        requested_state = "off"
        led.off()


    last_led_state = led_state
    logger.info(f"LED is in state {led_state}")

def print_instructions():
    """Print instructions to terminal."""
    print("LED Control URLs - Try them in your web browser:")
    print("  On    : " + URL + "/dweet/for/" + thing_name + "?state=on")
    print("  Off   : " + URL + "/dweet/for/" + thing_name + "?state=off")
    print("  Blink : " + URL + "/dweet/for/" + thing_name + "?state=blink\n")

def signal_handler(sig, frame):
    led.off()
    sys.exit(0)

thing_name = resolve_thing_name(THING_FILE_NAME)
init_led()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler) # Captures when CTRL - c is pressed
    print_instructions()

    print("Waiting for dweets. Press CTRL - C to exit")
    logger.info("Entering poll")
    poll_dweets_forever()
