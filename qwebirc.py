import requests
import time

BASE_URL = "https://qwebirc.swiftirc.net/e/"
S_URL = BASE_URL + "s"
P_URL = BASE_URL + "p"
N_URL = BASE_URL + "n"

cache_avoidance = "12345"
t = 0

nick = "pyqwebirc_simmy"

def connect(nick):
    global t
    r = requests.post(N_URL, params={"r": cache_avoidance, "t": t}, data={"nick": nick})
    t += 1
    return r.json()[1]

s = connect(nick)

def send(msg):
    global t
    r = requests.post(P_URL, params={"r": cache_avoidance, "t": t}, data={"s": s, "c": msg})
    t += 1

def recv():
    global t
    r = requests.post(S_URL, params={"r": cache_avoidance, "t": t}, data={"s": s})
    t += 1
    out = []
    for row in r.json():
        # print(row)
        if isinstance(row, list) and row[0] == "c":
            command = row[1]
            prefix = row[2]
            args = row[3]

            st = ""
            if prefix:
                st += ":" + prefix + " "
            st += command
            if len(args) >= 1:
                if len(args) > 1:
                    st += " " + " ".join(args[:-1])
                st += " :" + args[-1]
            out.append(st)
    return out


print(recv())
send("MODE {} +x".format(nick))
send("JOIN #sim ")

while True:
    print(recv())
    # time.sleep(3)