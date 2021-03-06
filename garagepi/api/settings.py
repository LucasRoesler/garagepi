try:
    from local_settings import API_KEY
except:
    import os
    API_KEY = os.environ.get('API_KEY')

LED_PIN = 18


RELAY_PIN_1 = 17
RELAY_PIN_2 = 27
RELAY_INIT_STATE = 'HIGH'

DOOR_MOVE_STATE = 'LOW'
DOOR_DETECTOR_PIN = 16
DOOR_RELAY_ID = 2

RELAY_PINS = {
    1: RELAY_PIN_1,
    2: RELAY_PIN_2,
}
