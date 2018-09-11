import socket,os,schedule
from threading import Thread
#from SocketServer import ThreadingMixIn
import subprocess,thread,time
import threading
#from sendfile import sendfile
import requests
TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024
threads = []
ip_clients=[]
conn_socket=[]
url="http://192.168.2.6:8080/ClientsUpdates.php"
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))	
class ClientThread(Thread):

	def __init__(self,ip,port,sock):
        	Thread.__init__(self)
        	self.ip = ip
        	self.port = port
        	self.sock = sock
        	print " New thread started for "+ip+":"+str(port)

	#def run(self):
		
def back_listen():
		tcpsock.listen(5)
		while True:
			
			#print "Waiting for incoming connections..."
			(conn, (ip,port)) = tcpsock.accept()
			print 'Got connection from ', (ip,port)
			newthread = ClientThread(ip,port,conn)
			newthread.start()
			threads.append(newthread)
			ip_clients.append(ip)
			conn_socket.append(conn)

def ping():
	for i in range(len(ip_clients)):
		ip=ip_clients[i]
		response = os.system("ping -c 1 " + ip)
		if response == 0:
			
			
			params={'ip':ip,'status':1}
			r = requests.post(url, params)
			print (r.status_code)
			print (r.text)

			
			
		else:
    			
			params={'ip':ip,'status':0}
			r = requests.post(url, params)
			print (r.status_code)
			print (r.text)	
try:
	thread.start_new_thread(back_listen,())
except:
	print "Error: unable to start thread"
schedule.every(.25).minutes.do(ping)
while True:
    schedule.run_pending()
while 1:
	pass



