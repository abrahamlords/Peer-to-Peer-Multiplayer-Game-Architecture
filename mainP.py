# manager: register, query players,query games,andde-register
"""
 First, start your manager program. Then start three (3) player processes that each register with
the server.
(d) Have one player issue a query players command.
(e) Have a different player issue a query games command.
(f) Exit the peers using de-register; terminate the server process. Graceful termination of your applica- tion is not required at this time.
"""
import random
# from socket import *
import sys

# serverAddress = sys.argv[1]
serverAddress = '100.100.100.100'
# serverPort = sys.argv[2]
serverPort = 51000
# clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket = '111.111.11.1'
extensionON = True

myGameID = -1
contacts = [{"contact": "Manager", "address": serverAddress, "port": serverPort}
	, {"contact": "Dealer", "address": '0.0.0.0', "port": 0}
	, {"contact": "player1", "address": '1.1.1.1', "port": 1}
	, {"contact": "player2", "address": '2.2.2.2', "port": 2}
	, {"contact": "player3", "address": '3.3.3.3', "port": 3}]
myShit = [{'hand': []}, {'hand': []}, {'hand': []}]
discardPile = []
currentPlayerI = 0
currentPlayer = contacts[2]

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
	for i in range(6):
		ii = 0
		for p in contacts[2:]:
			card = dek.getTopCard('hide')
			# print(str(i) + ': sending ' + card.toString('show') + ' to ' + str(p))
			myShit[ii]['hand'].append(card)
			ii = (ii + 1) % 3

	discardPile.append(dek.getTopCard())

def printHand():
	topRow = ''
	bottomRow = ''

	for i in range(3):
		topRow += (myShit[currentPlayerI]['hand'][i]).toString() + ' '
	for i in range(3,6):
		bottomRow += (myShit[currentPlayerI]['hand'][i]).toString() + ' '
	print(topRow + '\n' + bottomRow)
	return topRow + '\n' + bottomRow

def pickACard():
	if not extensionON:
		choice = random.randint(0,1)
	else:
		choice = random.randint(0, 2)
	card = ''
	if choice == 0:
		card = dek.getTopCard()
		print(currentPlayer['contact'] + ' picked a card from the deck')
		choice2 = random.randint(0, 1)
		if choice2 == 0:
			swapAny(card)
		if choice2 == 1:
			discardPile.append(card)
			print(currentPlayer['contact'] + ' discarded their new card')
	if choice == 1:
		card = discardPile.pop()
		print(currentPlayer['contact'] + ' picked a card from the discard pile')
		if len(discardPile) == 0:
			discardPile.append(dek.getTopCard())
		swapAny(card)
	if choice == 2:
		card, cardI = chooseFaceDown()
		stolenCard, otherPlayerI = steal(card)
		myShit[currentPlayerI]["hand"][cardI] = stolenCard
		print(currentPlayer['contact'] + ' stole ' + stolenCard.toString() + ' for *** from ' + contacts[otherPlayerI + 2][
			'contact'])


def pickOtherPlayerI():
	otherPlayer = random.randint(0, 2)
	while otherPlayer == currentPlayerI:
		otherPlayer = random.randint(0, 2)
	return otherPlayer
	
def steal(card):
	# send a player the card
	# get a (face up) card from them
	choice = random.randint(0, 5)
	otherPlayer = pickOtherPlayerI()
	theirCard = myShit[otherPlayer]["hand"][choice]
	while theirCard.hidden:
		choice = random.randint(0, 5)
		theirCard = myShit[otherPlayer]["hand"][choice]
	myShit[otherPlayer]["hand"][choice] = card  # their card gets replaced
	# return stolen card
	return theirCard, otherPlayer

def swapAny(newCard): #swap card with one of 6
	choice = random.randint(0, 5)
	myCard = myShit[currentPlayerI]["hand"][choice]
	discardPile.append(myCard)
	myShit[currentPlayerI]["hand"][choice] = newCard
	print(currentPlayer['contact'] + ' swapped ' + myCard.toString() + ' for ' + newCard.toString())
	myCard.hidden = False

def chooseFaceDown():
	while True:
		choice = random.randint(0, 5)
		myCard = myShit[currentPlayerI]["hand"][choice]
		if myCard.hidden:
			myCard.hidden = False
			return myCard, choice

def newCardAction(card, source):
	if source == 'discardPile':
		choice = 0
	else:
		choice = random.randint(0, 1)

	while not extensionON and choice == 1:
		if source == 'discardPile':
			choice = random.randint(0, 1)
		else:
			choice = random.randint(0, 2)

	if choice == 0:
		swapAny(card)
	'''if choice == 1:
		stolenCard = steal(card)
		swapFaceDown(stolenCard)'''
	if choice == 1:
		discardPile.append(card)
		print(currentPlayer['contact'] + ' discarded their new card')

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
		score = 0 # myScore
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
		print(currentPlayer['contact'] + '\'s score is ' + str(score))

		ii = (ii+1) % 3

	print()

def endRound():
	takeScore()
	for x in myShit:
		x["hand"].clear()

def hasHidden():
	for i in range(6):
		if (myShit[currentPlayerI]['hand'][i]).hidden:
			return True

def displayAllHands(stage = None):
	if stage == 'start':
		print('Start of round hands:')
	if stage == 'end':
		print('End of round hands:')
	ii = 0
	for p in contacts[2:]:
		currentPlayer = p
		print(currentPlayer['contact'] + '\'s hand is ')

		topRow = ''
		bottomRow = ''
		for i in range(3):
			topRow += (myShit[ii]['hand'][i]).toString() + ' '
		for i in range(3, 6):
			bottomRow += (myShit[ii]['hand'][i]).toString() + ' '
		print(topRow + '\n' + bottomRow)
		ii = (ii+1)%3
	print()

def PLAYBALL():
	global currentPlayerI
	global currentPlayer
	#for round in range(1, 10):
	for round in range(1, 2):
		print('Round: ' + str(round) + '\n')
		dealCards()
		turn2cardsUp()
		displayAllHands('start')
		allCardsUp = False
		while not allCardsUp:
			allCardsUp = True
			for p in contacts[2:]:
				currentPlayer = p
				if hasHidden():
					#print(currentPlayer['contact'] + '\'s hand is ')
					#printHand()
					#pickedCard, source = pickACard()
					pickACard()
					#newCardAction(pickedCard, source)
					#print('Now their hand is')
					#printHand()
					if hasHidden():
						allCardsUp = False
				else:
					print(currentPlayer['contact'] + ' is waiting for the others')
					#print(currentPlayer['contact'] + ' is waiting for the others. Their hand is ')
					#printHand()
				currentPlayerI = (currentPlayerI+1)%3
			print()
			displayAllHands()
		displayAllHands('end')
		endRound()
		# print('\n\n\n\n')
		# a player draws a card from either the top of the stock or the top of the discard pile
		# It can be swapped for one of the player’s 6 cards, or discarded.
		# If the card is swapped for one of the face-down cards, the card swapped-in is placed face-up.
		# The round for the “hole” ends when all of a player’s cards are face-up.
		# The dealer accumulates the score on that hole for all 9 holes in the game.


command = 'change contact'
receiverKey = -1
dek = Deck()

if __name__ == '__main__':
	'''print(dek)
	print(dek.getTopCard())
	dealCards()
	for c in myShit[currentPlayerI]['hand']:
		print(str(c))
	printHand()
'''

	PLAYBALL()
	
	print('good job!')
	"""
	while True:
		if (command == 'change contact'):
			printContactList()
			receiverKey = input("> ")
			while True:
				try:
					receiverKey = int(receiverKey)
					break
				except:
					print('enter an integer')

			while 0 >= receiverKey or receiverKey > len(contacts):
				print('Please try again')
				receiverKey = int(input("> "))

			receiverKey -= 1
			print("Enter message:")
			command = ''
		else:
			command = input("> ")
			#clientSocket.sendto(command.encode(), (contacts[receiverKey]["address"], contacts[receiverKey]["port"]))
			print('sent: ' + command + ' to ' + contacts[receiverKey]["address"] + ' at port ' + str(contacts[receiverKey]["port"]))

			#response, serverAddress = clientSocket.recvfrom(2048)  # buffer size is 2048

			#handleResponse(response.decode())
"""
