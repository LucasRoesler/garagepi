"""Hug API (local and HTTP access)"""

import hug
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)


@hug.get(examples='name=Timothy&age=26')
@hug.local()
def happy_birthday(name: hug.types.text, age: hug.types.number = 1, hug_timer=3):
    """Says happy birthday to a user."""
    return {'message': 'Happy {0} Birthday {1}! I think'.format(age, name),
            'took': float(hug_timer)}


@hug.get(examples='output=0')
@hug.local()
def led_test(output: hug.types.number = 0, hut_timer=3):
    """Test the LED circuit attached to the RaspberryPi."""
    if output < 1:
        GPIO.output(18, GPIO.LOW)
    else:
        GPIO.output(18, GPIO.HIGH)

    state = GPIO.input(18)

    return {'status': state}
