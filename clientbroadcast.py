import socket
import select
import sys
import marshal

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = '0.0.0.0'
Port = 8081
server.connect((IP_address,Port))

while True:
	socket_list = [sys.stdin, server]
	read_socket,write_socket,error_socket = select.select(socket_list,[],[])

	for socks in read_socket:
		if socks == server:
			message = socks.recv(2024)
			print message
		else :
			# message = sys.stdin.readline()
			message = raw_input()
			server.send(message)
			sys.stdout.flush()
server.close()
