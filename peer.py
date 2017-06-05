import socket, threading, time, sys

BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
MESSAGE = sys.argv[1]
check_lider = 0
lider = 100
TCP_PORT = None

def Listening(s):
    global hearthbeats
    global lider
    last = time.time()
    s.bind((socket.gethostbyname(socket.gethostname()), TCP_PORT))
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
            hearthbeats[data] += 1
            last = time.time()
            print "received data:", data
        print last
        if (time.time() - last > 5):
            print "entrei"
            for vivo in vivos:
                if(hearthbeats[vivo] == addr[0]):
                    if(hearthbeats[str(lider)] == addr[0]):
                        vivos.remove(vivo)
                        lider = 100
                        choose_lider()
                    else:
                        vivos.remove(vivo)


    conn.close()


def choose_lider():
    for i in IPS:
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
    

# def server():
#     global IP
#     global TCP_PORT
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((socket.gethostbyname(socket.gethostname()), 5000))
#     s.listen(1)
#     while True:
#         conn, addr = s.accept()
#         peers = threading.Thread(target=Listening, args=(conn, addr))
#         peers.daemon = True
#         peers.start()
#     conn.close




#=======================================================
IPS = []
vivos = []
hearthbeats = {}

global IP   

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

peer = threading.Thread(target=Listening, args=(s,))
peer.daemon = True
peer.start()

IP = socket.gethostbyname(socket.gethostname())


with open('entrada.txt','r') as file:
    line = file.readline().split()
    n_peers = line[0]
    TCP_PORT = int(line[1])
    for line in file:
        ips = line.split()
        hearthbeats[ips[0]] = 0
        IPS.append(ips[1])
        vivos.append(ips[0])


print hearthbeats
print IPS
print vivos


while(True):

    time.sleep(2)
    if not check_lider and sincroniza():
        print "escolhendo lider"
        choose_lider()
        check_lider = 1
    for i in IPS:
        if i != IP or not check_lider:
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

    #if check_lider:
     #   procurar_desconectado(cont)
    print lider
