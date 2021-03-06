from socket import *
from datetime import datetime
from pathlib import Path
import logging
import signal
import sys

BUFFER_SIZE = 2048
SERVER_IP = '127.0.0.1'
SERVER_PORT = 10080

class HTTPResponse:
	"""
	Abstraction for the HTTP Response
	Allows building HTTP responses easily
	"""
	def __init__(self, resource_name, content_type):
		self.http_standard = 'HTTP/1.0'
		self.resource = resource_name
		self.content_type = content_type
		self.is_text = 'text' in content_type

	def __get_response(self, body, code):
		content_length = f"Content-Length: {len(body)}" if not self.is_text else ''
		return f"{self.http_standard}# {code}\nContent-Type: {self.content_type}\n{content_length}\n\n{body}"

	def __read_bytes(self, file_name):
		return Path('./public/' + file_name).read_bytes()

	def __read_text(self, file_name):
		return Path('./public/' + file_name).read_text()

	def __read_file(self, file_name):
		return self.__read_text(file_name) if self.is_text else self.__read_bytes(file_name)

	def __return_404_body(self):
		return self.__read_file('404.html')

	def to_s(self):
		try:
			response = self.__get_response(self.__read_file(self.resource), '200 OK')
		except FileNotFoundError:
			response = self.__get_response(self.__return_404_body(), '404 Not Found')
		finally:
			return response


class HTTPHandler:
	"""
	Handles HTTP Requests and Responses
	"""
	server_socket = socket(AF_INET, SOCK_STREAM)
	server_socket.bind((SERVER_IP, SERVER_PORT))
	server_socket.listen(1)

	def __init__(self):
		super(HTTPHandler, self).__init__()

	def close(self):
		self.server_socket.close()

	def handle(self):
		conn, client_address = self.server_socket.accept()
		request = conn.recv(BUFFER_SIZE)

		if not request:
			conn.close()
			return False

		decoded_request = request.decode()
		logging.info(f"{datetime.now()} : {client_address} - {decoded_request}")

		request_list = decoded_request.strip().split('\n')

		headers = dict(header_field.strip().split(':', 1) for header_field in request_list[1:-1])

		request_line = request_list[0].split()
		headers['Request Type'] = request_line[0].strip()
		headers['Resource Name'] = request_line[1]
		headers['HTTP Standard'] = request_line[2].strip()

		response = getattr(self, headers['Request Type'].lower())(headers)
		
		conn.sendall(response.encode())
		return True

	def get(self, request):
		resource = 'index.html' if request['Resource Name'] == '/' else request['Resource Name']
		content_type = request['Accept'].split(',')[0]
		response = HTTPResponse(resource, content_type)
		print("hi")
		return response.to_s()

	def post(self, request):
		pass

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