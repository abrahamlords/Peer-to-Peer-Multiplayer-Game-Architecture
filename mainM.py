
import random
from socket import *
from typing import Union, Any

users = []    # users not playing a game  # stores dictionaries such as {"user": user, "address": address, "port": port}
players = []  # players in a game  # stores dictionaries
games = []    # ongoing games # stores {"id": gameID, "dealer": dealer, "players": newGamePlayers[]})
gameID = 0
""""""

def register(user, address, port):
    for x in users:
        if x["user"] == user:
            print("username in use")
            return "FAILURE"
        if x["port"] == port:
            print("port in use")
            return "FAILURE"
    users.append({"user": user, "address": address, "port": port})
    return 'SUCCESS'

"""
The manager also returns a game-identifier and a list of k users that together 
will play a game of Six Card Golf. Starting with the dealer, and then or each 
of the k other players, the manager returns the tuples stored in the “database” 
for each user. This includes, at a minimum, the user name, IPv4-address, and 
port. (While the dealer’s tuple is given first, the tuples of the players can 
be given in any order.).
"""
def startGame(dealer, k):
    playerQuant = int(k)
    newGamePlayers = []
    dealerInfo = {}
    global gameID

    cool = False
    for i in range(len(users)):  # make sure that the dealer is an available user
        if (users[i]["user"] == dealer):
            dealerInfo = users.pop(i)
            cool = True
            break
    if not cool:
        print(dealer + " is not available")
        return "FAILURE"

    if 0 < playerQuant < 4:  # if correct number of players
        if len(users) < playerQuant:  # check if enough players are available
            print("not enough users available")
            return "FAILURE"
        else:

            for x in range(playerQuant):
                nextI = random.randint(0, len(users)-1)
                newGamePlayers.append(users.pop(nextI))

        games.append({"id": gameID, "dealer": dealerInfo, "players": newGamePlayers})
        gameID += 1

        strang = "SUCCESS"
        strang += "\ngameID: " + str(gameID)
        strang += "\ndealer:\n" + str(dealerInfo)
        strang += '\nplayers:'
        for p in newGamePlayers:
            strang += "\n" + str(p)

        return strang
    else:
        print("player quantity must be from 1 to 3")
        return "FAILURE"


def queryPlayers():
    response = "Players in Game:\n"
    if len(players) == 0:
        response += "\t None"
    else:
        for x in players:
            response += '\t' + str(x) + '\n'
    response += "\nPlayers Waiting:\n"
    if len(users) == 0:
        response += "\t None"
    else:
        for x in users:
            response += '\t' + str(x) + '\n'
    return response

"""query games, to query the games of Six Card Golf currently ongoing. 
This command returns a return code equal to the number of ongoing games, 
and a list that includes information for each game, including at least the game identifier, 
user name of the dealer, and the user names for each other player in the game. 
If there are no games ongoing, the return code is set to zero and the list is empty."""
def queryGames():
    if len(games) == 0:
        return "0\nCurrent Games:\n\tempty list"
    else:
        strang = str(len(games)) + '\nCurrent Games:\n'
        for i in range(len(games)):
            strang += '\t Game ID: ' + games[i]['id'] +' Dealer: ' + games[i]['dealer'] + '\n'
            strang += '\t Players: \n'
            for p in games[i]['players']:
                strang += '\t\t' + str(p)

        return strang

def endGame(gameID, dealer):
    for g in games:
        if g["id"] == gameID:
            if g["dealer"] == dealer:
                del g
                return "SUCCESS"
            else:
                print("dealer doesn't match gameID")
                return "FAILURE"
    print("game ID not found")
    return "FAILURE"

def deRegister(user):
    # if user is not in a game as a play or a dealer than remove and return "SUCCESS"
    for i in range(len(users)):
        if users[i]["user"] == user:
            del users[i]
            return "SUCCESS"
    print("user not found or is in game")
    return "FAILURE"

def printEverything():
    print('\nusers')
    for x in users:
        print(x)
    print('\nplayers')
    for x in players:
        print(x)
    print('\ngames')
    for x in games:
        print(x)
    return "SUCCESS"


"""
serverPort = 51000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
"""

if __name__ == '__main__':
    print("ur mom is ready to receive")

    while True:
        #message, clientAddress = serverSocket.recvfrom(2048)
        message = input('> ')
        #messageList = message.decode().split(" ")
        messageList = message.split(" ")
        #print('  received - ' + message.decode())

        if messageList[0] == 'register':  # register ⟨user⟩ ⟨IPv4-address⟩ ⟨port⟩
            response = register(messageList[1], messageList[2], messageList[3])
        elif messageList[0] == 'query':
            if messageList[1] == 'players':
                response = queryPlayers()
            elif messageList[1] == 'games':
                response = queryGames()
        elif messageList[0] == 'start':
            if messageList[1] == 'game':
                response = startGame(messageList[2], messageList[3])
        elif messageList[0] == 'end':
            response = endGame(messageList[1], messageList[2])
        elif messageList[0] == 'de-register':
            response = deRegister(messageList[1])
        elif messageList[0] == 'print':
            response = printEverything()
        else:
            print("invalid command")
            response = 'FAILURE'

        print(response)
        #serverSocket.sendto(response.encode(), clientAddress)

