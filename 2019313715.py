from socket import *
from datetime import datetime
import logging

BUFFER_SIZE = 2048
MAX = 100

logger = logging.getLogger("logger")
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(name)s::[%(levelname)s]: %(message)s')

SERVER_IP = '127.0.0.1'
SERVER_PORT = 10080
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

number = randint(0, MAX)
guesses = 0

logging.info('Server is ready!')
conn, clientAddress = server_socket.accept()

while True:
	request = conn.recv(BUFFER_SIZE)	

	if not request:
		break
	else:
		decoded_request = request.decode()
		logging.info(f"{datetime.now()}: {clientAddress} - {decoded_request}")

		conn.send(response.encode())
