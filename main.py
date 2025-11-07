#Imports
import random
import sqlite3
import sys
import os

dbFile = 'PokerData.db'
gamePlayed = False
if os.path.exists(dbFile):
    gamePlayed = True

#create database and tables if not created already
try:
    sqliteConnection = sqlite3.connect(dbFile)
    cursor = sqliteConnection.cursor()

    query = """CREATE TABLE IF NOT EXISTS player (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR NOT NULL,
        chipValue INTEGER NOT NULL,
        wins INTEGER NOT NULL,
        losses INTEGER NOT NULL,
        betsPlaced INTEGER NOT NULL
    );"""

    cursor.execute(query)

    sqliteConnection.commit()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

finally:
    if sqliteConnection:
        sqliteConnection.close()

#Create class for player (Update later)
class Player:
    def __init__(self, name ,chipValue, wins, losses, betsPlaced):
        self.__name = name
        self.__chipValue = chipValue
        self.__wins = wins
        self.__losses = losses
        self.__betsPlaces = betsPlaced

    def displayName(self):
        return f'Your name is {self.__name}'

    def displayChips(self):
        return f'You have {self.__chipValue} chips'

    def displayWins(self):
        return f'You have {self.__wins} wins'

    def displayLosses(self):
        return f'You have {self.__losses} losses'

    def displayBetsPlaced(self):
        return f'You have placed {self.__betsPlaces} bets'
    
    def increaseChips(self, amount):
        self.__chipValue += amount

    def increaseWins(self, amount):
        self.__wins += amount

    def increaseLosses(self, amount):
        self.__losses += amount

    def increaseBetsPlaced(self, amount):
        self.__betsPlaces += amount

    def setName(self, nameValue):
        self.__name = nameValue

    def setChips(self, amount):
        self.__chipValue = amount

    def setWins(self, amount):
        self.__wins = amount

    def setLosses(self, amount):
        self.__losses = amount

    def setBetsPlaced(self, amount):
        self.__betsPlaces = amount
        

players = [Player("placeholder", 100, 0, 0, 0) for i in range(6)]

#Setting card values
cardValues = {i: str(i) for i in range(2, 11)}
cardValues.update({
    1: "Ace (Low)",
    11: "Jack",
    12: "Queen",
    13: "King",
    14: "Ace (High)"
})


#Creating suit dicts
cardsHearts = {i: True for i in range(1, 14)}
cardsDiamonds = {i: True for i in range(1, 14)}
cardsSpades = {i: True for i in range(1, 14)}
cardsClubs = {i: True for i in range(1, 14)}

deck = {
    "Hearts": cardsHearts,
    "Diamonds": cardsDiamonds,
    "Spades": cardsSpades,
    "Clubs": cardsClubs
}

#Creating hand types


def createCard(cardType, cardSuit):
    cardSymbols = {i: str(i) for i in range(2, 11)}
    cardSymbols.update({
        1: "A",
        11: "J",
        12: "Q",
        13: "K",
    })

    cardSuits = {
        "Hearts": "♥",
        "Diamonds": "♦",
        "Clubs": "♣",
        "Spades": "♠"
    }

    cardSymbol = cardSymbols[cardType]

    cardSuitSymbol = cardSuits[cardSuit]

    if cardType == 10:
        card = f"""┌─────────┐
│{cardSymbol}       │
│         │
│    {cardSuitSymbol}    │
│         │
│       {cardSymbol}│
└─────────┘"""
    else:
        card = f"""┌─────────┐
│{cardSymbol}        │
│         │
│    {cardSuitSymbol}    │
│         │
│        {cardSymbol}│
└─────────┘"""

    return card


def generateCard():
    while True:

        cardSuit = random.choice(list(deck.keys()))
        cardType = random.choice(list(deck[cardSuit].keys()))

        if deck[cardSuit][cardType] != False:
            card = createCard(cardType, cardSuit)
            deck[cardSuit][cardType] = False
            return card, cardSuit, cardType


def dealCards():
    card1, cardSuit1, cardType1 = generateCard()
    card2, cardSuit2, cardType2 = generateCard()
    card3, cardSuit3, cardType3 = generateCard()
    cards = [card1, card2, card3]
    splitCards = [card.split("\n") for card in cards]

    for lines in zip(*splitCards):
        print(" ".join(lines))


def deleteData():
    pass

#Loads data from the database into the players array
def loadData():
    try:
        sqliteConnection = sqlite3.connect(dbFile)
        sqliteConnection.row_factory = sqlite3.Row
        cursor = sqliteConnection.cursor()

        cursor.execute("SELECT * FROM player")
        rows = cursor.fetchall()

        index = 0

        for row in rows:
            players[index].setName(row["name"])
            players[index].setChips(row["chipValue"])
            players[index].setWins(row["wins"])
            players[index].setLosses(row["losses"])
            players[index].setBetsPlaced(row["betsPlaced"])
            index += 1


    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()

#If game has not been played before
def firstPlay():
    name = input("Enter your name: ")
    players[0].setName(name)
    players[0].setName("Bob")
    players[0].setName("Alice")
    players[0].setName("James")
    players[0].setName("Jacob")
    players[0].setName("Scott")
    startPoker()



#Starting the poker round
def startPoker():
    print("We will now begin the game")


#Play Game
def playGame(gamePlayed):
    print("In this game there will be 6 players including yourself")

    if gamePlayed:
        print("Would you like to continue where you left off?")
        print("1: Yes")
        print("2: No")
        choice = int
        while choice not in [1, 2]:
            try:
                choice = int(input("Enter Choice: "))
            except:
                print("Please enter a correct option")
        if choice == 1:
            print("Continuing last game")
            loadData()
            startPoker()
        elif choice == 2:
            print("This will reset all stats for you and the bots, are you sure?")
            print("1: Yes")
            print("2: No")
            choice = int
            while choice not in [1, 2]:
                try:
                    choice = int(input("Enter Choice: "))
                except:
                    print("Please enter a correct option")
            if choice == 1:
                print("Deleting save data and starting new game")
                deleteData()
            elif choice == 2:
                print("Continuing last game")
                loadData()
                startPoker()
        else:
            firstPlay()

    

#View Stats
def viewStats():
    pass

#Exit
def endProgram():
    sys.exit()

def startProgram():
    print("Welcome to terminal poker")
    print("Please select what you would like to do")
    print("1: Play")
    print("2: View Player Stats")
    print("3: Exit")
    choice = int
    while choice not in [1, 2, 3]:
        try:
            choice = int(input("Enter Choice: "))
        except:
            print("Please enter a correct option")
    if choice == 1:
        playGame(gamePlayed)
    elif choice == 2:
        viewStats()
    elif choice == 3:
        endProgram()
    

#Running the program
startProgram()
