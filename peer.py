import socket, threading, time, sys

peer_id = int(sys.argv[1])
TCP_PORTS = [5000, 5001, 5002, 5003]
TCP_IP = '127.0.0.1'
TCP_PORT = TCP_PORTS[peer_id]
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
MESSAGE = sys.argv[1]
lider = 5
lider_on = 0

def Listening(s):
    s.bind((TCP_IP, TCP_PORT))
    global lider
    while 1:
        s.listen(1)
        conn, addr = s.accept()
        try:
            data = conn.recv(BUFFER_SIZE, socket.MSG_OOB)
        except socket.error, value:
            data = None
        if data:
            if int(data) < lider:
                lider = int(data)
        else:
            data = conn.recv(BUFFER_SIZE)
            if not data: continue
            print "received data:", data

    conn.close()

def check_lider(lider_on):
    if lider_on == 0:
        return 0
    else:
        return 1

def choose_lider():
    global lider
    lider = 5
    for i in TCP_PORTS:
        try:
            so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            so.connect((TCP_IP, i))
            so.send(MESSAGE, socket.MSG_OOB)
            so.close()
        except:
            pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

peer = threading.Thread(target=Listening, args=(s,))
peer.daemon = True
peer.start()


while(True):

    time.sleep(2)
    for i in range(0,4):
        if i != peer_id:
            try:
                so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                so.connect((TCP_IP, TCP_PORTS[i]))
                so.send(MESSAGE)
                so.close()
            except:
                if i == lider:
                    print 'lider dead'
                    choose_lider()
    if not check_lider(lider_on):
        choose_lider()
        lider_on = 1
    print lider
