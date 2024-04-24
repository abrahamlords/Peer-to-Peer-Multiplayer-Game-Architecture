from socket import *
import sys
serverPort = 51000  #51000 to 51499


serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)  # buffer size = 2048

    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    serverSocket.sendto(message, ('10.120.70.145', 51001))
    serverSocket.sendto(message, ('10.120.70.145', 51002))
