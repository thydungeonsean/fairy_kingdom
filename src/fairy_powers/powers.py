

LURE = 0
SEE = 1
SLEEP = 2
GUST = 3
RIVER = 4
ROCK = 5
MARK = 6

name_to_key = {
    'LURE': LURE,
    'SEE': SEE,
    'SLEEP': SLEEP,
    'GUST': GUST,
    'RIVER': RIVER,
    'ROCK': ROCK,
    'MARK': MARK
}

key_to_name = {v: k for k, v in name_to_key.iteritems()}

POWER_BUTTONS = set(name_to_key.keys())
