from robot.client import Robot
from order.order import Order
from oven.client import Oven
from time import sleep

#pending orders starts empty gets populated by orders in oven

pending_orders = [] 

robots = [
    Robot('http://localhost', 4100),
    Robot('http://localhost', 4101)
]

ovens = [
    Oven('http://localhost', 5000, 0),
    Oven('http://localhost', 5001, 1)
]

VALID_STEPS = [None, 'PICK', 'SLICE', 'PACK']

def pick_next_order_to_work():
    #TODO super dummy so far get first it can work on
    for order in filter(lambda x: x.step_done == True, pending_orders):
        if order.last_step in VALID_STEPS[:-1]:
            return order
    return None

def print_status():
    done = 0
    for order in pending_orders:
        if order.last_step == VALID_STEPS[-1] and order.step_done:
            done += 1
    print('=======================================')
    print('== Orders: {}/{}'.format(done, len(pending_orders)))
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

while True:
    idle_robots = []
    # For each oven: 
    # check oven and if is idle place orders to pick from it
    for oven in ovens:
        status, err = oven.get_status()
        if status == 'idle':
            # there is a pizza to remove (add it to the pending orders)
            pending_orders.append(Order(oven))
            # This is here only because i need to remove pizza from oven as there is no central OrderDB in demo
            # also this method do not exist in real deployment as oven don't place nor pick pizzas robots do that. 
            oven.pick_pizza() #asume it has worked

    for robot in robots:
        status, err = robot.get_status()
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
    for r in idle_robots:
        order = pick_next_order_to_work()
        if order == None:
            print('No more orders to work on')
            break
        next_step = calculate_next_step(order)
        oven = None
        if next_step == 'PICK':
            oven = order.oven
        ok, err = r.command( next_step, order, oven.id if oven else None)
        if err != None:
            print(err)
            # TODO: maybe trigger an alert and/or remove the robot from the array of available robots
            continue
    # Verify conditions that may indicate the other orchestrator is dead and act accordingly
    # Yes, but not today :)
    print_status()
    sleep(1)