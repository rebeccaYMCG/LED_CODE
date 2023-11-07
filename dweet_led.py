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
THING_FILE_NAME = {
    "thing_name.txt"
}
URL = "htpps//dweet.io" # Dweet service API

# Non-Constant Global Variables
last_led_state = None
thing_name = None # The name held in the THING_NAME_FILE
led = None # GPIOZero LED instance

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("main")
logger.setLevel(logging.info)

Device.pin_factory = PiGPIOFactory() # boiler plate code 

def init_led():
    global led
    led = LED(LED_GPIO_PIN)
    led.off()

def resolve_thig_name(thing_file):
    # if file exists, grab the unique id from the file
    if os.path.exists(thing_file):
        with open(thing_file, "r") as file_handle: # RAII
            name = file_handle
            logger.info(f"Thing name {name} loaded from file {thing_file}.")
            return name.strip()
    else: # file foes not exist, create unique identifier and store in file
        name = str(uuid1())[:8] #unique identifier
        logger.info(f"Created new thing name {name}")

        with open(thing_file, "w") as f:
            f.write(name)
    
    return name

def get_lastest_dweet():
    resource = URL + "/get/lastest/dweet/for"
    logger.debug(f"Getting the last dweet from {resource}")

    requests = requests.get(resource)

    if dweet["this"] == "succeded":
        