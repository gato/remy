import requests

class Robot():
    def __init__(self, host, port):
        self.baseurl = '{}:{}/robot'.format(host, port)
        self.last = None
        self.order = None

    def command(self, command, order, oven):
        payload = {'command': command, 'oven': oven}
        self.clear_state()
        try:
            x = requests.post(self.baseurl, json=payload)
        except Exception as e:
            return None, 'Exception: {}'.format(e)
        if x.status_code != 201:
            return None, 'Invalid status code {}'.format(x.status_code)
        self.last = command
        self.order = order
        order.set_in_progress()
        return True, None

    def spread(self, order):
        return self.command('SPREAD', order, None)

    def scatter(self, order):
        return self.command('SCATTER', order, None)

    def place(self, order, oven):
        return self.command('PLACE', order, oven)

    def pick(self, order, oven):
        return self.command('PICK', order, oven)

    def slice(self, order):
        return self.command('SLICE', order, None)

    def pack(self, order):
        return self.command('PACK', order, None)

    def get_status(self):
        try:
            x = requests.get(self.baseurl)
        except Exception as e:
            return 'unreacheable', 'Exception: {}'.format(e)
        if x.status_code != 200:
            return 'broken', 'Invalid status code {}'.format(x.status_code)
        return x.json()['status'], None

    def clear_state(self):
        self.last = None
        self.order = None