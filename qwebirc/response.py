import enum

@enum.unique
class ResponseType(enum.Enum):
    CONNECT = "connect"
    COMMAND = "c"
    DISCONNECT = "disconnect"

class Response:
    subtypes = {}

    def __init__(self, item):
        self.type = self.get_item_type(item)

    @staticmethod
    def get_item_type(item):
        return ResponseType(item[0])

    @classmethod
    def from_item(cls, item):
        return cls.subtypes.get(cls.get_item_type(item), cls)(item)

def for_type(type):
    def decorator(cls):
        Response.subtypes[type] = cls
        return cls

    return decorator

@for_type(ResponseType.CONNECT)
class ConnectResponse(Response):
    def __init__(self, item):
        super().__init__(item)


@for_type(ResponseType.COMMAND)
class CommandResponse(Response):
    def __init__(self, item):
        super().__init__(item)
        _, self.command, self.prefix, self.args = item
        self.parse_args()

    def parse_args(self):
        if self.args:
            if " " in self.args[-1]:
                self.params = self.args[:-1]
                self.trailing = self.args[-1]
            else:
                self.params = self.args
                self.trailing = None
        else:
            self.params = self.trailing = None

    def __str__(self):
        str = ""
        if self.prefix:
            str += ":{} ".format(self.prefix)
        str += self.command
        if self.params:
            str += " " + " ".join(self.params)
        if self.trailing:
            str += " :{}".format(self.trailing)
        return str


@for_type(ResponseType.DISCONNECT)
class DisconnectResponse(Response):
    def __init__(self, item):
        super().__init__(item)
        self.reason = item[1]