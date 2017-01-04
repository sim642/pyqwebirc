import socketserver
import qwebirc
import random
import threading

# QWEBIRC_URL = "https://qwebirc.swiftirc.net"
# QWEBIRC_URL = "https://qwebirc.afternet.org"
QWEBIRC_URL = "http://irc.w3.org"
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
        self.client_thread.join()

    def irc_loop(self):
        for msg in self.rfile:
            msg = msg.strip()
            print("-->", str(msg, "utf8"))
            self.client.send(msg)

    def client_loop(self):
        for msg in self.client:
            print("<--", msg)
            self.wfile.write(bytes(msg + "\r\n", "utf8"))
        self.connection.close() # close IRC connection if disconnect was server side

class ReusingMixIn:
    allow_reuse_address = True

class ReusingThreadingTCPServer(ReusingMixIn, socketserver.ThreadingTCPServer):
    pass

server = ReusingThreadingTCPServer(("", 6667), IRCHandler)
server.serve_forever()