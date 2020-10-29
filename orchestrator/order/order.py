class Order():
    def __init__(self, oven=None):
        self.last_step = None
        self.step_done = True
        self.oven=oven
    
    def update_order(self, step):
        self.last_step = step
        self.step_done = True

    def set_in_progress(self):
        self.step_done = False

    def set_done(self):
        self.step_done = True
    
    def in_progress(self):
        return not self.step_done