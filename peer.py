import socket, threading, time, sys

def read_file():
	global TCP_IP
	print "\n-Lendo o arquivo 'entrada' para obter os IPs e IDs de todas as maquinas"
	print " As informacoes sao:"
	with open('entrada','r') as file:
	    line = file.readline().split()
	    n_peers = line[0]
	    print "\t-Numero de peers:", n_peers
	    for line in file:
	        ips = line.split()
	        print "\t-IP: {0} com ID: {1}".format(ips[1],ips[0])
	        heartbeats[ips[0]] = 0
	        IPs.append(ips[1])
	        peersOnline.append(ips[0])
	TCP_IP = IPs[PEER_ID]
	print "\n Estamos na maquina com IP:", TCP_IP

def sender():
	global peersOnline
	global FREQ
	check_lider = 0
	print "\n-Nao existe um lider ainda"
	while(True):

	    time.sleep(FREQ)
	    if not check_lider and sincroniza():
	    	print "\n-TODOS CONECTARAM"
	    	print '\n-ID dos peers online:', peersOnline
	        print "\n-Escolhendo o primeiro lider"
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

	s.close()


def listening(sock):
	print "\n-Peer comecou a ouvir"
	global TCP_IP
	global heartbeats
	sock.bind((TCP_IP, TCP_PORT))
	global lider
	global IPs
	while 1:
		sock.listen(1)
		conn, addr = sock.accept()
		try:
			data = conn.recv(BUFFER_SIZE, socket.MSG_OOB)
		except socket.error, value:
			data = None
		if data:
			continue
		else:
			data = conn.recv(BUFFER_SIZE)
			if not data: continue
			if int(data) != PEER_ID:
				print " Peer com ID {0} vivo! Recebi uma mensagem do IP {1}".format(data,IPs[int(data)])
			heartbeats[data] = time.time()
			#print "received data:", heartbeats

	conn.close()

def choose_lider():
    global peersOnline
    global lider
    lider = peersOnline[0]
    t_out.paused = True
    print "\n-Preciso avisar os outros que mudou o lider. URGENTE!"
    print "\t Enviando mensagens urgentes"
    for i in IPs:
        try:
            so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            so.connect((i, TCP_PORT))
            so.send(MESSAGE, socket.MSG_OOB)
            so.close()
        except:
            pass
    if int(lider) == PEER_ID:
    	print "\n-Eu sou o novo lider, com ID {0}\n".format(lider)
    else:
    	print "\n-O novo lider possui ID {0}\n".format(lider)
    t_out.paused = False

def sincroniza():
    for i in heartbeats:
        if heartbeats[i] == 0:
            return False
    return True

def time_out():
    global heartbeats
    global lider
    global peersOnline
    global TIMEOUT
    while 1:
        time.sleep(2)
        for h in peersOnline:
            if PEER_ID != int(h):
                if (time.time() - heartbeats[h]) > TIMEOUT:
                    if heartbeats[h]:
                    	print "\n-TIMEOUT! Algo estah errado"
                        if h == lider:
                            print '\t O lider desconectou, precisamos eleger um novo lider'
                            peersOnline.remove(h)
                            print "\t Continuam online os peers com id:", peersOnline
                            choose_lider()
                        else:
							print "\t Peer {0} desconectou, nada muda. Mas preciso atualizar o vetor de peersOnline".format(h)
							peersOnline.remove(h)
							print "\t Continuam online os peers com id:", peersOnline


#=======================================================
PEER_ID = int(sys.argv[1])
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024 
MESSAGE = sys.argv[1]
FREQ = 2
TIMEOUT = 5
lider = None
IPs = []
peersOnline = []
heartbeats = {}

print "#######################################################################"

print " Programa iniciado em -", time.ctime()
print "\n DEFINIDO - frequencia dos heartbeats eh {0} segundos".format(FREQ)
print "\n DEFINIDO - Timeout eh {0} segundos".format(TIMEOUT)
read_file()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "\n-Abri o socket"
peer = threading.Thread(target=listening, args=(sock,))
peer.daemon = True
peer.start()

t_out = threading.Thread(target=time_out)
t_out.daemon = True
t_out.start()
print "\n-Esperando as outras maquinas conectarem"
sender()