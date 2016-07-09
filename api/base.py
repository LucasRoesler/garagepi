"""Hug API (local and HTTP access)"""

import hug
import RPi.GPIO as GPIO

import settings

GPIO.setmode(GPIO.BCM)
GPIO.setup(settings.LED_PIN, GPIO.OUT)

# configure the relay pins to the default off position
for pin_id, pin_num in settings.RELAY_PINS.items():
    GPIO.output(pin_num, GPIO.HIGH)
    GPIO.setup(pin_num, GPIO.OUT)


@hug.get(examples='name=Timothy&age=26')
@hug.local()
def test(name: hug.types.text, points: hug.types.number = 1, hug_timer=3):
    """Says hello to a user."""

    msg = 'Hello {name}! You have {points} schrute points.'.format(
        name=name,
        points=points,
    )
    return {
        'message': msg,
        'took': float(hug_timer)
    }


@hug.get(examples='output=0')
@hug.local()
def led_test(output: hug.types.number = 0, hug_timer=3):
    """Test the LED circuit attached to the RaspberryPi.

    Notes:
        - 0 represents the GPIO low state
        - 1 represents the GPIO high state
    """
    msg = 'No light!'
    PIN = settings.LED_PIN
    if output < 1:
        GPIO.output(PIN, GPIO.LOW)
        msg = 'Light off!'
    else:
        msg = 'Light on!'
        GPIO.output(PIN, GPIO.HIGH)

    state = GPIO.input(PIN)

    return {
        'status': state,
        'message': msg,
        'took': float(hug_timer),
    }


@hug.get(examples='value=0')
@hug.local()
def relay(value: hug.types.number = 0, relay: hug.types.number = 1, hug_timer=3):
    """Toggle the relay state for relay one.

    Notes:
        - 0 represents the GPIO low state
        - 1 represents the GPIO high state
    """
    PIN = settings.RELAY_PINS.get(relay, None)

    if PIN is None:
        raise Exception("Invalid relay id.")

    if value < 1:
        GPIO.output(PIN, GPIO.LOW)
    else:
        GPIO.output(PIN, GPIO.HIGH)

    state = GPIO.input(PIN)

    return {
        'status': state,
        'took': float(hug_timer),
    }
