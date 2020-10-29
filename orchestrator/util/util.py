def print_status(orders, robots, ovens, valid_steps):
    done = 0
    for order in orders:
        if order.last_step == valid_steps[-1] and order.step_done:
            done += 1
    print('=======================================')
    print('== Orders: {}/{}'.format(done, len(orders)))
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