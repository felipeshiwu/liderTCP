import socket, threading, time, sys

peer_id = int(sys.argv[1])
TCP_IP = sys.argv[2]
TCP_PORT = 5000
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
MESSAGE = sys.argv[1]
check_lider = 0
lider = 100

def Listening(s):
    global hearthbeats
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
            hearthbeats[data] += 1
            if not data: continue
           # print "received data:", data

    conn.close()


def choose_lider():
    for i in TCP_IPS:
        try:
            so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            so.connect((i, TCP_PORT))
            so.send(MESSAGE, socket.MSG_OOB)
            so.close()
        except:
            pass

def sincroniza():
    for i in hearthbeats:
        if hearthbeats[i] == 0:
            return False
    return True
    
def procurar_desconectado(cont):
    for i in vivos:
        if int(i) != peer_id:
            if hearthbeats[i] != cont:
                lider = 100
                print "precisamos de um novo lider"
                choose_lider()
                vivos.remove(i)
    

#=======================================================
TCP_IPS = []
vivos = []
hearthbeats = {}
n = raw_input()
for i in range(0,int(n)):
    port = raw_input()
    ide = raw_input()
    TCP_IPS.append(port)
    hearthbeats[ide] = 0
    vivos.append(ide)
    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

peer = threading.Thread(target=Listening, args=(s,))
peer.daemon = True
peer.start()

cont = 0
while(True):

    time.sleep(2)
    if not check_lider and sincroniza():
        print "escolhendo lider"
        choose_lider()
        check_lider = 1
    for i in TCP_IPS:
        if i != TCP_IP or not check_lider:
            try:
                so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                so.connect((i, TCP_PORT))
                so.send(MESSAGE)
                so.close()
            except:
                pass
               # if i == lider:
                #    lider = 5
                 #   choose_lider()
    cont+=1
   #if check_lider:
    #    procurar_desconectado(cont)
    print lider
