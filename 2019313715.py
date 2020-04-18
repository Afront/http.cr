from socket import *
from datetime import datetime
from pathlib import Path
import logging
import signal
import sys

BUFFER_SIZE = 2048
SERVER_IP = '127.0.0.1'
SERVER_PORT = 10080

class HTTPHandler:
	server_socket = socket(AF_INET, SOCK_STREAM)
	server_socket.bind((SERVER_IP, SERVER_PORT))
	server_socket.listen(1)

	def __init__(self):
		super(HTTPHandler, self).__init__()

	def close_connection(self):
		self.server_socket.close()

	def handle(self):
		conn, client_address = self.server_socket.accept()
		request = conn.recv(BUFFER_SIZE)

		if not request:
			conn.close()
			return False

		print(request)
		decoded_request = request.decode()
		logging.info(f"{datetime.now()}: {client_address} - {decoded_request}")

		index = read_text('index.html')

		response = "HTTP/1.0 200 OK\n\n" + index

		print(request.split())
		conn.sendall(response.encode())
		return True

def read_text(file_name):
	return Path('./public/' + file_name).read_text()




def sigint_handler(signal_received, frame):
	print("Goodbye!")
	sys.exit(0)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, sigint_handler)
	http_handler = HTTPHandler()

	logger = logging.getLogger("logger")
	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(name)s::[%(levelname)s]: %(message)s')
	logging.info('Server is ready!')

	while http_handler.handle():
		pass

	http_handler.close()