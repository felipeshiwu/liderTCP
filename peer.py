import socket, threading, time, sys

def read_file():
	global TCP_IP
	with open('entrada','r') as file:
	    line = file.readline().split()
	    n_peers = line[0]
	    for line in file:
	        ips = line.split()
	        heartbeats[ips[0]] = 0
	        IPs.append(ips[1])
	        peersOnline.append(ips[0])
	TCP_IP = IPs[PEER_ID]

def sender():
	check_lider = 0
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
	    print lider

	s.close()


def listening(sock):
	global TCP_IP
	global heartbeats
	sock.bind((TCP_IP, TCP_PORT))
	global lider
	while 1:
		sock.listen(1)
		conn, addr = sock.accept()
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
    global peersOnline
    global lider
    lider = peersOnline[0]
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
    global peersOnline
    TIMEOUT = 5
    while 1:
        time.sleep(2)
        for h in peersOnline:
            if PEER_ID != int(h):
                if (time.time() - heartbeats[h]) > TIMEOUT:
                    if heartbeats[h]:
                        if h == lider:
                            print 'elegendo novo lider'
                            peersOnline.remove(h)
                            choose_lider()
                        else:
                            peersOnline.remove(h)


#=======================================================
PEER_ID = int(sys.argv[1])
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024 
MESSAGE = sys.argv[1]
lider = None
IPs = []
peersOnline = []
heartbeats = {}

read_file()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

peer = threading.Thread(target=listening, args=(sock,))
peer.daemon = True
peer.start()

t_out = threading.Thread(target=time_out)
t_out.daemon = True
t_out.start()

sender()