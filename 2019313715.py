from socket import *
from datetime import datetime
from pathlib import Path
import logging
import signal
import sys

BUFFER_SIZE = 2048
MAX = 100

def handler(signal_received, frame):
	print("Goodbye!")
	sys.exit(0)

def read_text(file_name):
	return Path('./public/' + file_name).read_text()

signal.signal(signal.SIGINT, handler)

logger = logging.getLogger("logger")
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(name)s::[%(levelname)s]: %(message)s')

SERVER_IP = '127.0.0.1'
SERVER_PORT = 10080
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

logging.info('Server is ready!')

while True:
	conn, clientAddress = server_socket.accept()
	request = conn.recv(BUFFER_SIZE)	

	if not request:
		conn.close()
		break
	else:
		print(request)
		decoded_request = request.decode()
		logging.info(f"{datetime.now()}: {clientAddress} - {decoded_request}")

		index = read_text('index.html')

		response = "HTTP/1.0 200 OK\n\n" + index
		print(response)
		conn.send(response.encode())
#		conn.close()

server_socket.close()