import socket

def Main():
    host = '127.0.0.1'
    port = 5000

    # socket.socket() - default for TCP
    # with additional parameters - for UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    print ("Server Started")

    while True:
    	data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print ("Message from: " + str(addr)), ("From user: " + data)
    	data = data.upper()
    	print ("Seinding: " + data)
        # tcp just s.send(...) w/o tuple
    	s.sendto(data.encode('utf-8'), addr)

    s.close()

if __name__ == '__main__':
	Main()