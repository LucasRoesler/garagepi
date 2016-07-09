"""Hug API (local and HTTP access)"""

import hug
import RPi.GPIO as GPIO

import settings

GPIO.setmode(GPIO.BCM)
GPIO.setup(settings.LED_PIN, GPIO.OUT)
GPIO.setup(settings.RELAY_PIN_1, GPIO.OUT)


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
    """Test the LED circuit attached to the RaspberryPi."""
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
def relay_one(value: hug.types.number = 0, hug_timer=3):
    """Toggle the relay state."""
    PIN = settings.RELAY_PIN_1

    if value < 1:
        GPIO.output(PIN, GPIO.LOW)
    else:
        GPIO.output(PIN, GPIO.HIGH)

    state = GPIO.input(PIN)

    return {
        'status': state,
        'took': float(hug_timer),
    }
