import socket
import sys
import threading


def create_packet(payload):
	encoded_payload = payload.encode("utf-8")
	encoded_payload_header = f"{len(encoded_payload):<{HEADER_LENGTH}}".encode("utf-8")
	return encoded_payload_header, encoded_payload


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
	encoded_device_name_header, encoded_device_name = create_packet(device_name)
	sock.sendall(encoded_device_name_header + encoded_device_name)
	listening_thread = ListenThread(sock)
	listening_thread.start()			
	
	while True:
		message = input("\n > ")
		encoded_message_header, encoded_message = create_packet(message)
		sock.sendall(encoded_message_header + encoded_message)
		print("Sent:     {}".format(message))
	listening_thread.join()
