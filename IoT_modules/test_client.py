import socket
import sys
import threading


HEADER_LENGTH = 10
HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])


# Listen Thread
class ListenThread(threading.Thread):
	def __init__(self, _sock):
		threading.Thread.__init__(self)
		self.sock = _sock
		print("Listening Thread started")

	def run(self):
		while True:
			received = str(self.sock.recv(1024), "utf-8")
			print("Received:     {}".format(received))


# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	# Connect to server and send data
	sock.connect((HOST, PORT))
	device_name = input("Enter device name:\n > ")
	device_name =  device_name.encode("utf-8")
	device_name_header = f"{len(device_name):<{HEADER_LENGTH}}".encode("utf-8")
	sock.sendall(device_name_header + device_name)
	listening_thread = ListenThread(sock)
	listening_thread.start()			
	
	while True:
		my_input = input(" > ")
		message = my_input.encode("utf-8")
		message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
		sock.sendall(message_header + message)
		print("Sent:     {}".format(message))
