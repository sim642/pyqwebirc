import requests
import urllib.parse
from .response import Response, ResponseType

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
        print("\t", r.json())
        return r.json()

    def connect(self, nick):
        self.cache_avoidance = "12345"
        self.t = 0

        self.s = self.request("n", nick=nick)[1]

    def send(self, msg):
        self.request("p", s=self.s, c=msg)

    def receive(self):
        return [Response.from_item(item) for item in self.request("s", s=self.s) if isinstance(item, list)]

    def __iter__(self):
        while True:
            for response in self.receive():
                if response.type == ResponseType.COMMAND:
                    yield response
                elif response.type == ResponseType.DISCONNECT:
                    return