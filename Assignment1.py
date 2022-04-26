#Author: Sunil Lal

#This is a simple HTTP server which listens on port 8080, accepts connection request, and processes the client request 
#in sepearte threads. It implements basic service functions (methods) which generate HTTP response to service the HTTP requests. 
#Currently there are 3 service functions; default, welcome and getFile. The process function maps the requet URL pattern to the service function.
#When the requested resource in the URL is empty, the default function is called which currently invokes the welcome function.
#The welcome service function responds with a simple HTTP response: "Welcome to my homepage".
#The getFile service function fetches the requested html or img file and generates an HTTP response containing the file contents and appropriate headers.

#To extend this server's functionality, define your service function(s), and map it to suitable URL pattern in the process function.

#This web server runs on python v3
#Usage: execute this program, open your browser (preferably chrome) and type http://servername:8080
#e.g. if server.py and broswer are running on the same machine, then use http://localhost:8080



from socket import *
import _thread
from xml.etree import ElementTree as ET
import pycurl
import json
import sys
from io import BytesIO

#token = 'pk_714d71dd258d40019c06d1ea28fb06f6'

#sandbox ##########################################
token = 'Tpk_4d88dfb8d4024e5bbea97f0f1b5ccadf'
###################################################

serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = int(sys.argv[1])
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("", serverPort))

serverSocket.listen(5)
print('The server is running')	
# Server should be up and running and listening to the incoming connections

#Extract the given header value from the HTTP request message
def getHeader(message, header):

	if message.find(header) > -1:
		value = message.split(header)[1].split()[0]
	else:
		value = None

	return value

#service function to fetch the requested file, and send the contents back to the client in a HTTP response.
def getFile(filename):

	try:

		# open and read the file contents. This becomes the body of the HTTP response
		f = open(filename, "rb")
		
		body = f.read()


		header = ("HTTP/1.1 200 OK\r\n\r\n").encode()

	except IOError:

		# Send HTTP response message for resource not found
		header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
		body = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode()

	return header, body

#service function to generate HTTP response with a simple welcome message
def default(message):


	header = "HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm=Access to staging site\r\n\r\n".encode()
	body = ("<html><head></head><body><h1>Welcome</h1></body></html>\r\n").encode()

	#"Authorization: Basic MDg0OTMyMjc6MDg0OTMyMjc=\r\n"

	return header, body

def authorized(message):
	header = ("HTTP/1.1 200 OK\r\n\r\n").encode()
	body = ("<html><head></head><body><h1>Welcome to my page</h1></body></html>\r\n").encode()

	return header, body

def portfolio(message):
	header = ("HTTP/1.1 200 OK\r\n\r\n").encode()
	body = ("<html><head></head><body><h1>Portfolio</h1></body></html>\r\n").encode()

	return header, body

def error(message):
	header = ("HTTP/1.1 200 OK\r\n\r\n").encode()
	body = ("<html><head></head><body><h1>ERROR - SOMTHING IS WRONG</h1></body></html>\r\n").encode()

	return header, body

def graph(message):
	temp_res = message.split()[1][1:20]
	temp_res2 = message.split()[1][1:]
	print(temp_res)
	temp_res2 = temp_res2.split('=')[1]
	stocksymbol = temp_res2
	print(stocksymbol)

	response_buffer = BytesIO()
	curl = pycurl.Curl()  # Set the curl options which specify the Google API server, the parameters to be passed to the API,
	# and buffer to hold the response
	curl.setopt(curl.SSL_VERIFYPEER, False)


	# curl.setopt(curl.URL, f'https://sandbox.iexapis.com/stable/stock/{stocksymbol}/chart/5y?chartCloseOnly=true&token={token}')
	curl.setopt(curl.URL, f'https://sandbox.iexapis.com/stable/stock/{stocksymbol}/chart/5y?chartCloseOnly=true&token={token}')

	curl.setopt(curl.WRITEFUNCTION, response_buffer.write)

	curl.perform()
	curl.close()

	body = '{\"graph\": ' + (response_buffer.getvalue().decode('UTF-8')) + '}'

	body = (body).encode()
	header = ("HTTP/1.1 200 OK\r\n\r\n").encode()

	return header, body

def research(message):
	print("research method")
	temp_res = message.split()[1][1:20]
	temp_res2 = message.split()[1][1:]
	print(temp_res)
	temp_res2 = temp_res2.split('=')[1]
	stocksymbol = temp_res2

	response_buffer = BytesIO()
	curl = pycurl.Curl()  # Set the curl options which specify the Google API server, the parameters to be passed to the API,
	# and buffer to hold the response
	curl.setopt(curl.SSL_VERIFYPEER, False)

	#curl.setopt(curl.URL, f'https://cloud.iexapis.com/stable/stock/{stocksymbol}/stats?token={token}')
	#curl2.setopt(curl.URL, f'https://sandbox.iexapis.com/stable/stock/{stocksymbol}/chart/5y?chartCloseOnly=true&token={token}')

	##########SANDBOX MODE################################################################################
	curl.setopt(curl.URL, f'https://sandbox.iexapis.com/stable/stock/{stocksymbol}/stats?token={token}')
	##########SANDBOX MODE################################################################################

	curl.setopt(curl.WRITEFUNCTION, response_buffer.write)

	curl.perform()
	curl.close()

	body = (response_buffer.getvalue().decode('UTF-8')).encode()
	header = ("HTTP/1.1 200 OK\r\n\r\n").encode()

	return header, body


#We process client request here. The requested resource in the URL is mapped to a service function which generates the HTTP reponse 
#that is eventually returned to the client. 
def process(connectionSocket) :	
	# Receives the request message from the client
	message = connectionSocket.recv(1024).decode()
	print(message)


	if message.find("Authorization: Basic MDg0OTMyMjc6MDg0OTMyMjc=") > -1 :

		#if temp_res == 'research?stcksymbol':


		if message.find("stock") > -1:
			#############Getting the Stock Symobls from API##########################################################
			response_buffer = BytesIO()
			curl = pycurl.Curl()  # Set the curl options which specify the Google API server, the parameters to be passed to the API,
			# and buffer to hold the response
			curl.setopt(curl.SSL_VERIFYPEER, False)
			#curl.setopt(curl.URL, 'https://cloud.iexapis.com/stable/ref-data/symbols?token=' + token)
			##########SANDBOX MODE################################################################################
			curl.setopt(curl.URL, 'https://sandbox.iexapis.com/stable/ref-data/symbols?token=' + token)
			##########SANDBOX MODE################################################################################
			curl.setopt(curl.WRITEFUNCTION, response_buffer.write)

			curl.perform()
			curl.close()

			body = response_buffer.getvalue().decode('UTF-8')
			#convert from json to python
			body = json.loads(body)


			et = ET.parse('portfolio.xml')
			temp_message = message.split()[-1]
			temp = temp_message.split('=')[1]
			stock_value = temp.split('&')[0]

			####################Getting the latest quote#######################################################################################
			response_buffer2 = BytesIO()
			curl2 = pycurl.Curl()  # Set the curl options which specify the Google API server, the parameters to be passed to the API,
			# and buffer to hold the response
			curl2.setopt(curl2.SSL_VERIFYPEER, False)
			curl2.setopt(curl2.URL, f'https://sandbox.iexapis.com/stable/stock/{stock_value}/quote?token={token}')

			curl2.setopt(curl2.WRITEFUNCTION, response_buffer2.write)

			curl2.perform()
			curl2.close()

			body2 = response_buffer2.getvalue().decode('UTF-8')
			body2 = json.loads(body2)

			latest_price = body2['latestPrice']
			############################################################################################################

			temp = temp_message.split('=')[3]
			price_value = temp.split('&')[0]
			if price_value == '':
				price_value = 0

			root = et.getroot()

			found_stock = False
			for child in root.iter('stock'):
				if child.get('symbol') == stock_value:
					previous_quantity = int(child.find('quantity').text)
					found_stock = True
			if price_value == 0:
				gainORloss = str(0)
			else:
				gainORloss = str((latest_price - float(price_value)) / float(price_value) * 100)

			#loop through all stock symbole to see if stock_value is valid symobl
			for x in body:
				if x['symbol'].find(stock_value) > -1:
					found = True
					break
				else:
					found = False
			#if stock_value is valid symbol
			if found:
				if found_stock:
					for child in root.iter('stock'):
						if child.get('symbol') == stock_value:
							temp = temp_message.split('=')[2]
							quantity_value = int(temp.split('&')[0])
							quantity_result = int(child.find('quantity').text)
							quantity_result += quantity_value
							if quantity_result < 0:
								responseHeader, responseBody = error(message)
								connectionSocket.send(responseHeader)
								# Send the content of the HTTP body (e.g. requested file) to the connection socket
								connectionSocket.send(responseBody)
								# Close the client connection socket
								connectionSocket.close()
								break

							child.find('quantity').text = str(quantity_result)
							child.find('gainNloss').text = gainORloss

							if quantity_result != 0:
								price = (previous_quantity*float(child.find('price').text) + quantity_value*float(price_value)) / float(child.find('quantity').text)

							if quantity_value > 0:
								child.find('price').text = str("{:.2f}".format(price))

							for quant in root.findall('stock'):
								result = int(quant.find('quantity').text)
								if result == 0:
									root.remove(quant)

				else:
					investment = ET.SubElement(et.getroot(), 'stock')
					investment.set('symbol', stock_value)

					temp = temp_message.split('=')[2]
					quantity_value = int(temp.split('&')[0])
					quantity_result = 0
					if quantity_value > 0:
						quantity_result += quantity_value
					else:
						quantity_result -= quantity_value

					quantity = ET.SubElement(investment, 'quantity')
					quantity.text = str(quantity_result)

					price = ET.SubElement(investment, 'price')
					price.text = price_value

					gainNloss = ET.SubElement(investment, 'gainNloss')
					gainNloss.text = gainORloss



				et.write('portfolio.xml')
			# if stock_value is not valid run error message
			else :
				responseHeader, responseBody = error(message)
				connectionSocket.send(responseHeader)
				# Send the content of the HTTP body (e.g. requested file) to the connection socket
				connectionSocket.send(responseBody)
				# Close the client connection socket
				connectionSocket.close()




		if len(message) > 1:

			# Extract the path of the requested object from the message
			# Because the extracted path of the HTTP request includes
			# a character '/', we read the path from the second character
			resource = message.split()[1][1:]
			print(resource)
			temp_res = message.split()[1][1:20]

			# map requested resource (contained in the URL) to specific function which generates HTTP response
			if resource == "":
				responseHeader, responseBody = authorized(message)
			elif resource == "portfolio":
				print("portfolio loop")
				responseHeader, responseBody = getFile('portfolio.html')
			elif resource == "research":
				print('research loop')
				responseHeader, responseBody = getFile('research.html')
			elif temp_res == "research?stcksymbol":
				print('else loop')
				responseHeader, responseBody = research(message)
			elif resource.find('graph') > -1:
				responseHeader, responseBody = graph(message)
			else:
				responseHeader, responseBody = getFile(resource)
	else:
		responseHeader, responseBody = default(message)

	# Send the HTTP response header line to the connection socket
	connectionSocket.send(responseHeader)
	# Send the content of the HTTP body (e.g. requested file) to the connection socket
	connectionSocket.send(responseBody)
	# Close the client connection socket
	connectionSocket.close()


#Main web server loop. It simply accepts TCP connections, and get the request processed in seperate threads.
while True:
	
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()
	#Clients timeout after 60 seconds of inactivity and must reconnect.
	connectionSocket.settimeout(60)
	# start new thread to handle incoming request
	_thread.start_new_thread(process,(connectionSocket,))





