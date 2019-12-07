import socket
import select
import sys
import time
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = '0.0.0.0'
Port = 8081
server.bind((IP_address, Port))
server.listen(100)
list_of_clients ={}
list_ip = {}
temp = []

def clientthread(conn, addr):
	multi = conn.recv(2048)
	list_of_clients[conn] = multi
	for ipclients in list_ip:
		if list_ip[ipclients] == "connected2" and ipclients == addr[0]:
			dtn(conn,addr[0])
	while True:
		try:
			message = conn.recv(2048)
			if message:
				print ("<" + addr[0] + "> " + message)
				message_to_send = ("<" + addr[0] +"> " + message)
				multicast(message_to_send,conn, addr[0])


			else:
				remove(conn, addr[0])
		except:
			continue

def dtn(connection,ip):
	print temp
	for message in temp:
		print message

		connection.send(message)
		time.sleep(0.4)
		# temp.remove(message)



def multicast(message,connection, ip):
	for clients in list_of_clients: 
		if clients==connection:
			grup = list_of_clients[clients]
	for clients in list_of_clients: 
		if clients!=connection and list_of_clients[clients] == grup:
			try:
				clients.send(message)
			except:
				clients.close()
				remove(clients, addr[0])
	for ipclients in list_ip:
		if list_ip[ipclients] == "disconnected":
			temp.append(message)

def remove(connection, ip):
	if connection in list_of_clients:
		del list_of_clients[connection]
		list_ip[ip] = "disconnected"
		print list_of_clients
		print list_ip

while True:
	conn , addr = server.accept()
	flek=0
	for ip in list_ip:
		if ip == addr[0]:
				flek=1
				list_ip[ip] = "connected2"
	if flek==0:
		list_ip[addr[0]] = "connected"
	print (addr[0] + " connected")
	start_new_thread(clientthread, (conn,addr))

conn.close()
server.close()