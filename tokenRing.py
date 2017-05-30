import pickle, Queue, select, socket, sys, threading, time, zlib

#-----------------------------------------------------DICIONARIO DE SERVIDORES---------------------------------------------------------

servs = {
        'bowmore' : '200.17.202.53',
        'priorat' : '200.17.202.49',
        'taliskeri' : '200.17.202.57',
        'macalani' : '200.17.202.6',
        'mumm' : '200.17.202.11',
        }

#-----------------------------------------------------DICIONARIO DE PRIORIDADES---------------------------------------------------------

priority_queue = {
	'7' : 1,
	'6' : 2,
	'5' : 3,
	'4' : 4,
	'3' : 5,
	'2' : 6,
	'1' : 7,
	'0' : 8, }

#------------------------------------------------------------PACOTE--------------------------------------------------------------------

class Package:
    def __init__(self, type, sender, dest, prio, data=None):
        #tipo 0 para mensagem, tipo 1 para bastao, tipo 2 para ack
        self.mark = '~'
        self.type = int(type)
        self.prio = int(prio)
        self.sender = int(sender)
        self.dest = int(dest)
        self.data = data[0:300]
        self.crc = zlib.crc32(str(self.type) + str(self.prio) + str(self.sender) + str(self.dest) + self.data)

#-------------------------------------------------SOCKET, FILA DE PACOTES E BASTAO-----------------------------------------------------

class Socket:
    def __init__(self, id, my_addr, my_port, conect_addr, conect_port):
        self.id = int(id)
        self.my_addr = my_addr
        self.my_port = my_port
        self.conect_addr = conect_addr
        self.conect_port = conect_port
        self.pack_queue = Queue.PriorityQueue()
        self.hasToken = False
        self.TIMEOUT = 40
        self.HOLD_TOKEN = 10
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.my_addr, self.my_port))

    def queue(self, message):
        pack = Package(0, self.id, message[0] , message[2], message[4:])
        self.pack_queue.put((priority_queue[str(pack.prio)], pack))

    def send(self, pack):
        spack = pickle.dumps(pack)
        self.sock.sendto(spack, (self.conect_addr, self.conect_port))

    def genToken(self):
        token = Package(1, 0, self.id, 0, "novo")
        #print("gerei bastao")
        #print("passei bastao")
        self.send(token)

    def sendToken(self, prio):
        token = Package(1, 0, self.id, prio, "token")
        #print("passei bastao")
        self.send(token)

#-------------------------------------------------TIME OUT, RECEBER MENSAGENS, PASSAGEM DE BASTAO----------------------------------------------------

def TokenRing(sock):
    tkArrival = time.time()
    while True:
        if time.time() - tkArrival > sock.TIMEOUT and not sock.hasToken:
            sock.genToken()
            tkArrival = time.time()
        if time.time() - tkArrival > sock.HOLD_TOKEN and sock.hasToken:
            sock.hasToken = False
            sock.sendToken(tokenPrio)
        if sock.hasToken:
            time.sleep (1)
            if not sock.pack_queue.empty():
		    aux, h_prio = sock.pack_queue.get()
                    if h_prio.prio > tokenPrio:
                        sock.pack_queue.put((aux, h_prio))
                        sock.hasToken = False
                        sock.sendToken(h_prio.prio)
                    elif h_prio.prio == tokenPrio:
                        sock.send(h_prio)
                        sock.hasToken = False
                        sock.sendToken(int(0));
                    else:
                        sock.pack_queue.put((aux, h_prio))
                        sock.hasToken = False
                        sock.sendToken(tokenPrio)
            else:
                sock.hasToken = False
                sock.sendToken(tokenPrio)

        else:
            sock.sock.setblocking(0)
            thing = select.select([sock.sock], [], [], sock.HOLD_TOKEN)
            if thing[0]:
                sdata, addr = sock.sock.recvfrom(500)
                data = pickle.loads(sdata)
                if (data.type == 1 and (zlib.crc32(str(data.type) + str(data.prio) + str(data.sender) + str(data.dest) + data.data) != data.crc)):
                    print("Erro de CRC!")
                else:
                    if data.type == 1: #token
                        if data.data[0] == 'n':
                            if data.dest != sock.id:
                                sock.tkArrival = time.time()
                                sock.sendToken(0)
                            else:
                                data.data = 'token'
                                sock.hasToken = True
                                tokenPrio = data.prio
                                tkArrival = time.time()
                        elif data.data[0] == 't':
                            sock.hasToken = True
                            tokenPrio = data.prio
                            tkArrival = time.time()
                    else:
                        if (data.dest == sock.id):
                            data.type = 2
                            print "Msg de :", data.sender, "com prioridade", data.prio, ":", data.data
                            sock.send(data)
                        if (data.sender != sock.id):
                            sock.send(data)
                        if(data.sender == sock.id and data.type != 2):
                            print("Destino nao esta na rede")

#------------------------------------------------------------MAIN--------------------------------------------------------------------

#id = raw_input('Digite seu ID : ')
#my_addr = raw_input('Digite seu Endereco : ')
#my_port = raw_input('Digite sua Porta : ')
#conect_addr = raw_input('Digite o Endereco da conexao : ')
conect_port = '5013'


sock = Socket(sys.argv[1], sys.argv[2], int(conect_port), sys.argv[3], int(conect_port))
#sock = Socket(id, my_addr, int(conect_port), conect_addr, int(conect_port))

#------------------------------------------------------------THREAD------------------------------------------------------------------

token_ring = threading.Thread(target=TokenRing, args=(sock,))
token_ring.daemon = True
token_ring.start()

#------------------------------------------------------------ENTRADA-----------------------------------------------------------------

#if(id == '0'):

if(sys.argv[1] == '0'):
   sock.genToken()
print 'Digite ID destino (0 - 3), a prioridade (0 - 7) e a mensagem (menor que 300) : '

while(True):
    message = raw_input()

    #if message[0] != id:

    if len(message) < 300:
        if message[0] != sys.argv[1]:
            sock.queue(message)
        #else:
            #print "Msg de :", message[0], "com prioridade", message[2], ":", message[4:]
    else:
        print "Mande uma mensagem menor que 300 caracteres."

sock.close()
