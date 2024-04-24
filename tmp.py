#manager: register, query players,query games,andde-register
"""
 First, start your manager program. Then start three (3) player processes that each register with
the server.
(d) Have one player issue a query players command.
(e) Have a different player issue a query games command.
(f) Exit the peers using de-register; terminate the server process. Graceful termination of your applica- tion is not required at this time.
"""

from socket import *
import ast
import sys
#serverName = sys.argv[1]
#serverPort = sys.argv[2]
serverPort = 51000

clientSocket = socket(AF_INET, SOCK_DGRAM)

class Card:
    def __init__(self, value, suit):
        self.hidden = True
        if (value == 11):
            self.value = "J"
        elif (value == 12):
            self.value = "Q"
        elif (value == 13):
            self.value = "K"
        else:
            self.value = value
        self.suit = suit

    def toString(self, hiddenOverride=None):
        if not self.hidden or hiddenOverride == 'show':
            return '{:3}'.format(str(self.value) + str(self.suit))
        elif hiddenOverride == 'hide':
            return '***'
        else:
            return '***'

    def turnOver(self):
        self.hidden = False

    def __str__(self):
        return '{:3}'.format(str(self.value) + self.suit)

command = ''
if __name__ == '__main__':
    val, suit = '', ''
    response = 'KD'
    try:
        val = int(response[0])
        if val == 1:
            if response[1] == '0':
                val = 10
                suit = response[2]
            else:
                suit = response[1]
        else:
            suit = response[1]
    except:
        if response[0] == 'J':
            val = 11
        if response[0] == 'Q':
            val = 12
        if response[0] == 'K':
            val = 13
        suit = response[1]

    print((Card(val, suit)).toString('show'))

'''    
    contacts = [{"contact": "Manager", "address": '1.1.1', "port": serverPort}
        , {"contact": "Dealer", "address": '0.0.0.0', "port": 0}
        , {"contact": "player1", "address": '1.1.1.1', "port": 1}
        , {"contact": "player2", "address": '2.2.2.2', "port": 2}
        , {"contact": "player3", "address": '3.3.3.3', "port": 3}]

    tets = "{'user': 'b', 'address': '10.120.70.145', 'port': '51002'}"

    contacts.append(ast.literal_eval(tets))
    print(contacts[5]['address'])
    print(str(int('10D')))

    myContactInfo = ['name', 'address', 'port']
    myContactInfo = (input('Enter your contact info: ')).split(' ')  # ['name', 'address', 'port']
    myContactInfo[2] = int(myContactInfo[2])

    print(str((myContactInfo[1]) + str(myContactInfo[2])))

    while True:
        command = input("> ")
        messageList = command.split("\#n")
        print(messageList[0])

        
        clientSocket.sendto(command.encode(), (serverName, serverPort))
        response, serverAddress = clientSocket.recvfrom(2048)  # buffer size is 2048
        print(response.decode())
'''
