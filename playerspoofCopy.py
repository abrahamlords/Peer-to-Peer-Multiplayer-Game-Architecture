# manager: register, query players,query games,andde-register
"""
 First, start your manager program. Then start three (3) player processes that each register with
the server.
(d) Have one player issue a query players command.
(e) Have a different player issue a query games command.
(f) Exit the peers using de-register; terminate the server process. Graceful termination of your applica- tion is not required at this time.
"""
import random
import ast
from socket import *
import sys

serverAddress = sys.argv[1]
#serverPort = sys.argv[2]
serverPort = 51000
clientSocket = socket(AF_INET, SOCK_DGRAM)
extensionON = True

myGameID = -1
contacts = [{"user": "Manager", "address": serverAddress, "port": serverPort}]

myContactInfo = ['name', 'address', 'port']

myShit = [{'hand': []}, {'hand': []}]
discardPile = []
currentPlayerI = 0
currentPlayer = {"user": "player1", "address": '1.1.1.1', "port": 1}


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


class Deck:
    def __init__(self):  # constructor makes and shuffles a standard 52 card deck
        self.deck = []
        for x in range(52):
            val = (x % 13) + 1
            # newCard = Card(-1, "-")
            if 0 <= x < 13:  # diamonds
                newCard = Card(val, "D")
            if 13 <= x < 26:  # hearts
                newCard = Card(val, "H")
            if 26 <= x < 39:  # clubs
                newCard = Card(val, "C")
            if 39 <= x < 52:  # spades
                newCard = Card(val, "S")
            self.deck.append(newCard)
        random.shuffle(self.deck)

    def __str__(self):
        return ' '.join(c.toString(True) for c in self.deck)

    def reshuffle(self):
        self.deck = discardPile.copy()
        discardPile.clear()
        for c in self.deck:
            c.hidden = True
        random.shuffle(self.deck)
        discardPile.append(self.getTopCard())
        print('Discard pile reshuffled into deck.')

    def getTopCard(self, hiddenOverride=None):
        if len(self.deck) == 0:
            self.reshuffle()
        topCard = self.deck.pop()
        if (hiddenOverride != 'hide'):
            topCard.turnOver()
        return topCard


def dealCards():
    dek = Deck()
    global myShit
    for i in range(6):
        ii = 0
        for p in contacts[2:]:
            card = dek.getTopCard('hide')
            print(str(i) + ': sending ' + card.toString('show') + ' to ' + str(p))
            clientSocket.sendto(card.toString('show').encode(), (p["address"], int(p["port"])))
            myShit[ii]['hand'].append(card)
            ii = (ii + 1) % 2

    discardPile.append(dek.getTopCard())


def printHand():
    topRow = ''
    bottomRow = ''

    for i in range(3):
        topRow += (myShit[currentPlayerI]['hand'][i]).toString() + ' '
    for i in range(3, 6):
        bottomRow += (myShit[currentPlayerI]['hand'][i]).toString() + ' '
    print(topRow + '\n' + bottomRow)
    return topRow + '\n' + bottomRow


def pickACard():
    choice = random.randint(0, 2)
    card = ''
    source = ''
    if choice == 0:
        card = dek.getTopCard()
        source = 'deck'
    if choice == 1:
        card = discardPile.pop()
        source = 'discard pile'
        if len(discardPile) == 0:
            discardPile.append(dek.getTopCard())
    if choice == 2:
        stolenCard = steal(card)
        swapFaceDown(stolenCard)

    print(currentPlayer['user'] + ' picked a card from the ' + source)
    sendMessage('You picked a card from the ' + source)
    return card, source


def pickOtherPlayerI():
    otherPlayer = random.randint(0, 1) # hardcoded for 2 players
    while otherPlayer == currentPlayerI:
        otherPlayer = random.randint(0, 1)
    return otherPlayer


def steal(card):
    # send a player the card
    # get a (face up) card from them
    choice = random.randint(0, 5)
    otherPlayer = pickOtherPlayerI()
    print(str(otherPlayer))
    theirCard = myShit[otherPlayer]["hand"][choice]
    while theirCard.hidden:
        choice = random.randint(0, 5)
        theirCard = myShit[otherPlayer]["hand"][choice]
    myShit[otherPlayer]["hand"][choice] = card  # their card gets replaced
    # return stolen card
    print(currentPlayer['user'] + ' stole ' + theirCard.toString() + ' from ' + contacts[otherPlayer + 2]['user'])
    sendMessage('You stole ' + theirCard.toString() + ' from ' + contacts[otherPlayer + 2]['user'])
    message = currentPlayer['user'] + ' stole ' + theirCard.toString() + ' from you'
    clientSocket.sendto(message.encode(), (contacts[otherPlayer + 2]["address"], int(contacts[otherPlayer + 2]["port"])))
    return theirCard


def swapAny(newCard):  # swap card with one of 6
    choice = random.randint(0, 5)
    myCard = myShit[currentPlayerI]["hand"][choice]
    discardPile.append(myCard)
    myShit[currentPlayerI]["hand"][choice] = newCard
    print(currentPlayer['user'] + ' swapped ' + myCard.toString() + ' for ' + newCard.toString())
    sendMessage( 'You swapped ' + myCard.toString() + ' for ' + newCard.toString())
    myCard.hidden = False


def swapFaceDown(newCard):  # swap card with any hidden
    swapSucc = False
    while not swapSucc:
        choice = random.randint(0, 5)
        myCard = myShit[currentPlayerI]["hand"][choice]
        if myCard.hidden:
            myCard.hidden = False
            discardPile.append(myCard)
            myShit[currentPlayerI]["hand"][choice] = newCard
            swapSucc = True
            sendMessage('You swapped their card for ***')


# print(currentPlayer['user'] + ' swapped ' + myCard.toString() + ' for ' + newCard.toString())

def newCardAction(card, source):
    if source == 'discardPile':
        choice = random.randint(0, 1)
    else:
        choice = random.randint(0, 2)

    while not extensionON and choice == 1:
        if source == 'discardPile':
            choice = random.randint(0, 1)
        else:
            choice = random.randint(0, 2)

    if choice == 0:
        swapAny(card)
    if choice == 1:
        stolenCard = steal(card)
        swapFaceDown(stolenCard)
    if choice == 2:
        discardPile.append(card)
        print(currentPlayer['user'] + ' discarded their new card')
        sendMessage('You discarded your new card')


def turn2cardsUp():
    for x in myShit:
        x["hand"][0].turnOver()
        x["hand"][1].turnOver()


def scoreChart(card):
    if type(card.value) == int:
        if card.value == 2:
            return -2
        else:
            return card.value
    else:
        if card.value == 'J' or card.value == 'Q':
            return 10
        elif card.value == 'K':
            return 0
        else:
            return -99999


'''Scoring. Each ace counts 1 point. Each 2 counts minus 2 points. 
Each numeral card from 3 to 10 scores face value. 
Each jack or queen scores 10 points. 
Each king scores zero points. 
A pair of equal cards in the same column scores zero points for the column (even if the equal cards are twos). '''


def takeScore():
    ii = 0
    for p in contacts[2:]:
        score = 0  # myScore
        currentPlayer = p
        topRow = []
        bottomRow = []
        for i in range(3):
            topRow.append(myShit[ii]['hand'][i])
        for i in range(3, 6):
            bottomRow.append(myShit[ii]['hand'][i])

        for i in range(3):
            if topRow[i].value == bottomRow[i].value:
                pass  # go to next col
            else:
                score += scoreChart(topRow[i])
                score += scoreChart(bottomRow[i])
        print(currentPlayer['user'] + '\'s score is ' + str(score))
        sendToAllParts(currentPlayer['user'] + '\'s score is ' + str(score))
        ii = (ii + 1) % 2

    print()
    sendToAllParts('\n')


def endRound():
    takeScore()
    for x in myShit:
        x["hand"].clear()


def hasHidden():
    for i in range(6):
        if (myShit[currentPlayerI]['hand'][i]).hidden:
            return True

def displayCommand(p):
    pass

def displayAllHands(stage=None):
    if stage == 'start':
        print('Start of round hands:')
    if stage == 'end':
        print('End of round hands:')
    ii = 0
    for p in contacts[2:]:
        currentPlayer = p
        print(currentPlayer['user'] + '\'s hand is ')

        topRow = ''
        bottomRow = ''
        for i in range(3):
            topRow += (myShit[ii]['hand'][i]).toString() + ' '
        for i in range(3, 6):
            bottomRow += (myShit[ii]['hand'][i]).toString() + ' '
        print(topRow + '\n' + bottomRow)
        message = topRow + '\n' + bottomRow + '\n'
        clientSocket.sendto(message.encode(), (contacts[ii+2]["address"], int(contacts[ii+2]["port"])))
        ii = (ii + 1) % 2
    print()

def sendToAllParts(message):
    #message = command + ' ' + ' '.join(args)
    for i in range(1, len(contacts)+1):
        print('  ' + str(i) + ' - ' + str(contacts[i-1]))

    for i in range(1, len(contacts)):
        print('sending to addess ' + contacts[i]["address"] + ' port ' + str(contacts[i]["port"]))
        clientSocket.sendto(message.encode(), (contacts[i]["address"], int(contacts[i]["port"])))

def PLAYBALL():
    global currentPlayerI
    global currentPlayer
    # for round in range(1, 10):
    for round in range(1, 2):
        sendToAllParts('Round: ' + str(round) + '\n')
        dealCards()
        turn2cardsUp()
        displayAllHands('start')
        allCardsUp = False
        while not allCardsUp:
            allCardsUp = True
            for p in contacts[2:]:
                currentPlayer = p
                if hasHidden():
                    # print(currentPlayer['user'] + '\'s hand is ')
                    # printHand()
                    pickedCard, source = pickACard()
                    newCardAction(pickedCard, source)
                    # print('Now their hand is')
                    # printHand()
                    if hasHidden():
                        allCardsUp = False
                else:
                    print(currentPlayer['user'] + ' is waiting for the others')
                    sendMessage('Other players still have unrevealed hands')
                # print(currentPlayer['user'] + ' is waiting for the others. Their hand is ')
                # printHand()
                currentPlayerI = (currentPlayerI + 1) % 2
            print()
            displayAllHands()
        displayAllHands('end')
        endRound()


# print('\n\n\n\n')

def chooseContact():
    print("Who would you like to contact?")
    for i in range(1, len(contacts)+1):
        print('  ' + str(i) + ' - ' + str(contacts[i-1]))

    receiverKey = input("> ")
    while type(receiverKey) != int:
        try:
            receiverKey = int(receiverKey)
            break
        except:
            print('enter an integer')

    while 0 >= receiverKey or receiverKey > len(contacts):
        print('Please try again')
        receiverKey = int(input("> "))

    return receiverKey-1

def sendMessage(message):
    clientSocket.sendto(message.encode(), (currentPlayer["address"], int(currentPlayer["port"])))


def sendCommand(receiverKey, command, args):
    message = command + ' ' + ' '.join(args)
    clientSocket.sendto(message.encode(), (contacts[receiverKey]["address"], int(contacts[receiverKey]["port"])))
    #response, serverAddress = clientSocket.recvfrom(2048)  # buffer size is 2048
    #return(response.decode())

def register():
    getMyInfo()
    sendCommand(0, 'register', myContactInfo)
    response, serverAddress = clientSocket.recvfrom(2048)
    response = response.decode()
    resList = response.split('\n')
    while resList[0] != 'SUCCESS':
        print(resList[1])
        getMyInfo()
        sendCommand(0, 'register', myContactInfo)
        response, serverAddress = clientSocket.recvfrom(2048)
        response = response.decode()
        resList = response.split('\n')

def playAsDealer():
    PLAYBALL()

def playAsParticipant():
    while True:
        response, serverAddress = clientSocket.recvfrom(2048)
        print(response.decode())

def playGame():
    global currentPlayer
    currentPlayer = contacts[2]
    contactName = contacts[1]['user']
    me = myContactInfo[0]
    if contactName == me:
        playAsDealer()
    else:
        playAsParticipant()

def joinGame():
    register()
    print(' Waiting for game...')
    print(waitForGame())

def startGame():
    register()
    dealer = input('Dealer: ')
    k = input('Number of players: ')
    sendCommand(0, 'start game', [dealer, k])
    print(waitForGame())

def waitForGame():
    response, serverAddress = clientSocket.recvfrom(2048)
    response = response.decode()
    resList = response.split('\n')

    if (resList[0] != 'SUCCESS'):
        print('start game failed')
        return
    myGameID = int(resList[1].split(' ')[1])
    # resList[2] is 'dealer: '

    contacts.append(ast.literal_eval(resList[3]))  # add dealer to contacts
    # resList[4] is 'players: '
    for p in resList[5:]:
        contacts.append(ast.literal_eval(p))
    return response

def getMyInfo():
    global clientSocket
    global myContactInfo
    myContactInfo = (input('Enter your contact info: ')).split(' ')  # ['name', 'address', 'port']
    #myContactInfo[2] = int(myContactInfo[2])
    clientSocket.bind((myContactInfo[1], int(myContactInfo[2])))

def sayhi():
    while True:
        receiverKey = chooseContact()
        clientSocket.sendto('hi\n\n\n'.encode(), (contacts[receiverKey]["address"], contacts[receiverKey]["port"]))

def standby():
    response, serverAddress = clientSocket.recvfrom(2048)
    response = response.decode()
    print(response)

    pass
"""
What would you like to do?
    1 - send message
    2 - join game
        register(input(name), address, port)
        wait
    3 - start game
        register()
        start_game()
"""


command = 'change contact'
receiverKey = -1
dek = Deck()

if __name__ == '__main__':
    while True:
        if (command == 'change contact'):
            receiverKey = chooseContact()

            print("Enter message:")
            command = ''
        else:
            command = input("> ")
            if (command == 'join'):
                joinGame()
                playGame()
            elif (command == 'start'):
                startGame()
                playGame()
            elif (command == 'hi'):
                sayhi()
            elif (command == 'standby'):
                standby()
            elif (command != 'change contact' and command != 'r'):
                clientSocket.sendto(command.encode(), (contacts[receiverKey]["address"], contacts[receiverKey]["port"]))
                response, serverAddress = clientSocket.recvfrom(2048)  # buffer size is 2048
                print(response.decode())