import socket, threading, time, sys

peer_id = int(sys.argv[1])
TCP_PORTS = [5000, 5001, 5002, 5003]
TCP_IP = '127.0.0.1'
TCP_PORT = TCP_PORTS[peer_id]
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
MESSAGE = "tuts " + sys.argv[1]


def Listening(s):
    s.bind((TCP_IP, TCP_PORT))

    while 1:
        s.listen(1)
        conn, addr = s.accept()
        data = conn.recv(BUFFER_SIZE)
        if not data: continue
        print "received data:", data

    conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

peer = threading.Thread(target=Listening, args=(s,))
peer.daemon = True
peer.start()


while(True):

    time.sleep(2)
    for i in range(0,4):
        if i != peer_id:
            so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            so.connect((TCP_IP, TCP_PORTS[i]))
            so.send(MESSAGE)
            so.close()
