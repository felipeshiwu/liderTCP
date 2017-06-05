import socket, threading, time, sys

peer_id = int(sys.argv[1])
TCP_IP = sys.argv[2] 
TCP_PORT = 5036
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
MESSAGE = sys.argv[1]
check_lider = 0
lider = 100

def Listening(s):
    global heartbeats
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
            print 'Novo lider' 
        else:
            data = conn.recv(BUFFER_SIZE)
            if not data: continue
            heartbeats[data] = time.time()
            #print "received data:", heartbeats

    conn.close()


def choose_lider():
    global vivos
    global lider
    lider = vivos[0]
    t_out.paused = True
    for i in IPs:
        try:
            so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            so.connect((i, TCP_PORT))
            so.send(MESSAGE, socket.MSG_OOB)
            so.close()
        except:
            pass
    t_out.paused = False

def sincroniza():
    for i in heartbeats:
        if heartbeats[i] == 0:
            return False
    return True

def time_out():
    global heartbeats
    global lider
    global vivos
    TIMEOUT = 5
    while 1:
        time.sleep(2)
        for h in vivos:
            if peer_id != int(h):
                if (time.time() - heartbeats[h]) > TIMEOUT:
                    if heartbeats[h]:
                        if h == lider:
                            print 'elegendo novo lider'
                            vivos.remove(h)
                            choose_lider()
                        else:
                            vivos.remove(h)


#=======================================================
IPs = []
vivos = []
heartbeats = {}
#n = raw_input()
#for i in range(0,int(n)):
#    port = raw_input()
#    ide = raw_input()
#    TCP_PORTS.append(int(port))
#    heartbeats[ide] = 0
#    vivos.append(ide)
#
with open('entrada','r') as file:
    line = file.readline().split()
    n_peers = line[0]
    for line in file:
        ips = line.split()
        heartbeats[ips[0]] = 0
        IPs.append(ips[1])
        vivos.append(ips[0])


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

peer = threading.Thread(target=Listening, args=(s,))
t_out = threading.Thread(target=time_out)
peer.daemon = True
t_out.daemon = True
peer.start()
t_out.start()

while(True):

    time.sleep(2)
    if not check_lider and sincroniza():
        print "escolhendo lider"
        choose_lider()
        check_lider = 1
    for i in IPs:
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
    #if check_lider:
    #    procurar_desconectado(cont)
    print lider

s.close()
