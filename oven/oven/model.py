from datetime import datetime, timedelta

# time to cook a pizza (totally made up)
TIME_TO_COOK=10


#Just For simulating a oven and it's state
class Oven:
    def __init__(self):
        self.empty = True
        self.start = None

    def busy(self):
        ''' check if oven is currently doing something '''
        return (not self.empty) and self.start + timedelta(seconds=TIME_TO_COOK) > datetime.now()

    def place_pizza(self):
        ''' DUMMY: pizza placed in oven '''
        if self.busy():
            raise Exception('Oven is busy')
        if not self.empty:
            raise Exception('Oven not Empty')
        self.empty = False
        self.start = datetime.now()

    def pick_pizza(self):
        if self.busy():
            raise Exception('Oven is busy')
        if self.empty:
            raise Exception('Oven is Empty')
        self.empty = True


THE_OVEN = Oven()

def get_oven():
    return THE_OVEN
