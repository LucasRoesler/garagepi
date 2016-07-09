"""Hug API (local and HTTP access)"""

import hug


@hug.get(examples='name=Timothy&age=26')
@hug.local()
def happy_birthday(name: hug.types.text, age: hug.types.number = 1, hug_timer=3):
    """Says happy birthday to a user. Test."""
    return {'message': 'Happy {0} Birthday {1}! I think'.format(age, name),
            'took': float(hug_timer)}
