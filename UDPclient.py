from socket import *
import sys
serverName = sys.argv[1]
serverPort = 51000

clientSocket1 = socket(AF_INET, SOCK_DGRAM)
clientSocket1.bind(('10.120.70.145', 51001))
clientSocket2 = socket(AF_INET, SOCK_DGRAM)
clientSocket2.bind(('10.120.70.145', 51002))

message = input('Input lowercase sentence:')

clientSocket1.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket1.recvfrom(2048)  # buffer size = 2048
massage, serverAddress = clientSocket1.recvfrom(2048)  # buffer size = 2048
print(modifiedMessage.decode())
print(massage.decode())

try:
	plzno, serverAddress = clientSocket2.recvfrom(2048, MSG_DONTWAIT)  # buffer size = 2048
	print(plzno.decode())
except:
	print('no massange')


clientSocket1.close()
