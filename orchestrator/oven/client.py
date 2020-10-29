import requests

class Oven():
    def __init__(self, host, port, id):
        self.baseurl = '{}:{}/oven'.format(host, port)
        self.id = id

    def place_pizza(self):
        try:
            x = requests.post(self.baseurl)
        except Exception as e:
            return None, 'Exception: {}'.format(e)
        if x.status_code != 201:
            return None, 'Invalid status code {}'.format(x.status_code)
        return True, None

    def pick_pizza(self):
        try:
            x = requests.delete(self.baseurl)
        except Exception as e:
            return None, 'Exception: {}'.format(e)
        if x.status_code != 204:
            return None, 'Invalid status code {}'.format(x.status_code)
        return True, None

    def get_status(self):
        try:
            x = requests.get(self.baseurl)
        except Exception as e:
            return 'unreachable', 'Exception: {}'.format(e)
        if x.status_code != 200:
            return 'broken', 'Invalid status code {}'.format(x.status_code)
        return x.json()['status'], None