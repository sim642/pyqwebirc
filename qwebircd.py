import socketserver
import qwebirc
import random
import threading
import socketserver_extra

# QWEBIRC_URL = "https://qwebirc.swiftirc.net"
# QWEBIRC_URL = "https://qwebirc.afternet.org"
QWEBIRC_URL = "http://irc.w3.org"
NICK = "pyqwebircd"

class IRCHandler(socketserver_extra.TextStreamRequestHandler):
    wnewline = "\r\n"

    def handle(self):
        self.log("connected")

        self.client = qwebirc.Client(QWEBIRC_URL)
        self.client.connect(NICK + str(random.randint(1, 1000)))

        self.irc_thread = threading.Thread(target=self.irc_loop)
        self.irc_thread.start()

        self.client_thread = threading.Thread(target=self.client_loop)
        self.client_thread.start()

        self.irc_thread.join()
        self.client_thread.join()

        self.log("disconnected")

    def irc_loop(self):
        for msg in self.rfile:
            msg = msg.strip()
            self.log("-->", msg)
            self.client.send(msg)

    def client_loop(self):
        for response in self.client:
            msg = str(response)
            self.log("<--", msg)
            self.wfile.write(msg + "\n")
            self.wfile.flush()
        self.connection.close() # close IRC connection if disconnect was server side

    def log(self, *args):
        ip, port = self.client_address
        print("{}:{}".format(ip, port), *args, sep="\t")

server = socketserver_extra.ReusingThreadingTCPServer(("", 6667), IRCHandler)
server.serve_forever()