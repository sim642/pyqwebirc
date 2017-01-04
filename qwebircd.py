import socketserver
import qwebirc
import random
import threading

QWEBIRC_URL = "https://qwebirc.swiftirc.net"
NICK = "pyqwebircd"

class IRCHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.client = qwebirc.Client(QWEBIRC_URL)
        self.client.connect(NICK + str(random.randint(1, 1000)))

        self.irc_thread = threading.Thread(target=self.irc_loop)
        self.irc_thread.start()

        self.client_thread = threading.Thread(target=self.client_loop)
        self.client_thread.start()

        self.irc_thread.join()

    def irc_loop(self):
        while True:
            msg = self.rfile.readline().strip()
            print("-->", str(msg, "utf8"))
            self.client.send(msg)

    def client_loop(self):
        while True:
            for msg in self.client.receive():
                print("<--", msg)
                self.wfile.write(bytes(msg + "\r\n", "utf8"))


class ReusingTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

server = ReusingTCPServer(("", 6667), IRCHandler)
server.serve_forever()