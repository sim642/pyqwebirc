import requests
import urllib.parse

class Client:
    def __init__(self, url):
        self.url = url

    def get_url(self, char):
        return urllib.parse.urljoin(self.url, "e/" + char)

    @property
    def params(self):
        return {
            "r": self.cache_avoidance,
            "t": self.t
        }

    def request(self, char, **data):
        r = requests.post(self.get_url(char), params=self.params, data=data)
        self.t += 1
        return r.json()

    def connect(self, nick):
        self.cache_avoidance = "12345"
        self.t = 0

        self.s = self.request("n", nick=nick)[1]

    def send(self, msg):
        self.request("p", s=self.s, c=msg)

    def receive(self):
        items = self.request("s", s=self.s)
        return list(map(Client.stringify_msg, filter(Client.is_msg, items)))

    @staticmethod
    def is_msg(item):
        return isinstance(item, list) and item[0] == "c"

    @staticmethod
    def stringify_msg(item):
        _, command, prefix, args = item

        str = ""
        if prefix:
            str += ":{} ".format(prefix)
        str += command
        if args:
            if " " in args[-1]:
                params = args[:-1]
                trailing = args[-1]
            else:
                params = args
                trailing = None

            if params:
                str += " " + " ".join(params)
            if trailing:
                str += " :{}".format(trailing)

        return str
