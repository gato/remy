from robot.client import Robot
from order.order import Order
from oven.client import Oven
from time import sleep

pending_orders = [Order() for i in range(20)] 

robots = [
    Robot('http://localhost', 4000),
    Robot('http://localhost', 4001)
]

ovens = [
    Oven('http://localhost', 5000, 0),
    Oven('http://localhost', 5001, 1)
]

VALID_STEPS = [None, 'SPREAD', 'SCATTER', 'PLACE']
def pick_next_order_to_work(available_ovens):
    #TODO super dummy so far get first it can work on
    for order in filter(lambda x: x.step_done == True, pending_orders):
        #orders not in the last step if there are free ovens or one less if there is no free ovens
        limit = -1 if available_ovens else -2
        if order.last_step in VALID_STEPS[:limit]:
            return order
    return None

def print_status():
    done = 0
    for order in pending_orders:
        if order.last_step == VALID_STEPS[-1] and order.step_done:
            done += 1
    print('=======================================')
    print('== Orders: {}/{}'.format(done, len(pending_orders)))
    print('==')
    print('== Robots:')
    for i, robot in enumerate(robots):
        status, err = robot.get_status()
        print ('== {} is {}'.format(i, status))
    print('==')
    print('== Ovens:')
    for i, oven in enumerate(ovens):
        status, err = oven.get_status()
        print ('== {} is {}'.format(i, status))
    print('==\n')

def calculate_next_step(order):
    if order.last_step == VALID_STEPS[-1]:
        return None
    return VALID_STEPS[VALID_STEPS.index(order.last_step) + 1]
# From doc
# For each Robot:
#   If robot has finished a task update order status accordingly 
#   If robot is busy for more than a Y time trigger alert Robot not working, configure order to start again and remove it from pool 
# For each oven: 
    # Read oven status. Used for Top function below.
# Get Top N Orders that need to be processed by this Orchestrator (Before or After oven) (where N is the number of free robots, Top is some function that prioritize which order need to be tackled next probably with the idea of finishing more pizzas instead of having more in progress)
# For each free robot:
# Assign the next task and update status accordingly
# Verify conditions that may indicate the other orchestrator is dead and act accordingly
while True:
    idle_robots = []
    idle_ovens = []
    # for i, order in enumerate(pending_orders):
    #     print(i, order.last_step, order.step_done)
    # For each Robot:
    for i, robot in enumerate(robots):
        status, err = robot.get_status()
        #print ('robot {} is {}'.format(i, status))
        # If robot has finished a task update order status accordingly  
        if status == 'idle':
            idle_robots.append(robot) 
            if robot.last != None:
                # update order and remove it from robot
                order = robot.order
                order.update_order(robot.last)
                robot.clear_state()
        # If robot is busy for more than a Y time trigger alert Robot not working, configure order to start again and remove it from pool 
        # TODO: handle, not for skeleton project
    # For each oven: 
    for i, oven in enumerate(ovens):
        status, err = oven.get_status()
        #print ('oven {} is {}'.format(i, status))
        if status == 'empty':
            idle_ovens.append(oven)
    for r in idle_robots:
        order = pick_next_order_to_work(len(idle_ovens) > 0)
        if order == None:
            print('No more orders to work on')
            break
        next_step = calculate_next_step(order)
        oven = None
        if next_step == 'PLACE':
            oven = idle_ovens.pop()
        ok, err = r.command( next_step, order, oven.id if oven else None)
        if err != None:
            print(err)
            # TODO: maybe trigger an alert and/or remove the robot from the array of available robots
            continue
        # This is here only because i need to simulate robot putting pizza in oven and making 
        # the mock robot api do it is a burden. in reality oven.place_pizza and oven.pick_pizza 
        # will not exist as the robot will place and pick them and oven will only present a 
        # get status API
        if next_step == 'PLACE':
            oven.place_pizza() #asume it has worked
    # Verify conditions that may indicate the other orchestrator is dead and act accordingly
    # Yes, but not today :)
    print_status()
    sleep(1)