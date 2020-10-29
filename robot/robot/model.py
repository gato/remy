from datetime import datetime, timedelta
from random import random
#Just For simulating a robot and it's state

SPREAD_TOMATO_SAUCE = {'description': 'Spreading tomato sauce on a pizza crust', 'command': 'SPREAD', 'params': [], 'duration': 5, 'random_delay': 3}
SCATTER_CHEESE = {'description': 'Scattering cheese over tomato sauce', 'command': 'SCATTER', 'params': [], 'duration': 2, 'random_delay': 2}
PLACE_PIZZA = {'description': 'Placing pizza in one of the ovens', 'command': 'PLACE', 'params':['oven'], 'duration': 3, 'random_delay': 1}

PICK_PIZZA = {'description': 'Picking pizza from one of the ovens', 'command': 'PICK', 'params':['oven'], 'duration': 5, 'random_delay': 2}
SLICE_PIZZA = {'description': 'Slicing it into pieces', 'command': 'SLICE', 'params':[], 'duration': 3, 'random_delay': .5}
PACK_PIZZA = {'description': 'Packing pizza into the box', 'command': 'PACK', 'params':[], 'duration': 3, 'random_delay': 2}

def to_map(arr):
    m = {}
    for item in arr:
        m[item['command']] = item
    return m

BEFORE_ROLE = to_map([SPREAD_TOMATO_SAUCE, SCATTER_CHEESE, PLACE_PIZZA])
AFTER_ROLE = to_map([PICK_PIZZA, SLICE_PIZZA, PACK_PIZZA])

class Robot:
    def __init__(self, role):
        if role not in [BEFORE_ROLE, AFTER_ROLE]:
            raise Exception('Invalid Role')
        self.role = role
        self.current = None
        self.delay = 0
        self.start = None

    def busy(self):
        ''' check if robot is currently doing something '''
        return self.current != None and self.start + timedelta(seconds=self.current['duration'] + self.delay) > datetime.now()

    def perform(self, command, params):
        ''' DUMMY: perform instruccion '''
        if self.busy():
            raise Exception('Robot is busy')
        if not self.valid_command(command):
            raise Exception('invalid command')
        if not self.valid_params(command, params):
            raise Exception('invalid parameters')
        self.current = self.role[command]
        self.delay = random() * self.current['random_delay']
        self.start = datetime.now()

    def valid_command(self, command):
        return command in self.role

    def valid_params(self, command, params):
        # check if parameters are present
        for p in self.role[command]['params']:
            if p not in params or params[p] is None:
                return False
        return True

    def get_task(self):
        return self.current['description'] if self.busy() else 'idle'

#dummy robot state
THE_ROBOT = None
def configure_robot(role):
    global THE_ROBOT
    THE_ROBOT = Robot(role)

def get_robot():
    return THE_ROBOT
