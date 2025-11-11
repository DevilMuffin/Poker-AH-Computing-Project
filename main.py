#Imports
import random
import sqlite3
import sys
import os

dbFile = 'PokerData.db'
gamePlayed = False
if os.path.exists(dbFile):
    gamePlayed = True


#Adds default data to database
def insertFirstData():
    try:
        sqliteConnection = sqlite3.connect(dbFile)
        cursor = sqliteConnection.cursor()

        insertQuery = '''INSERT INTO player (name, chipValue, wins, losses, betsPlaced) VALUES (?, ?, ?, ?, ?)'''

        for i in range(len(players)):
            cursor.execute(insertQuery, (players[i].getName(), players[i].getChips(), players[i].getWins(), players[i].getLosses(), players[i].getBetsPlaced()))

        sqliteConnection.commit()


    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()


#If game has not been played before
def firstPlay():
    try:
        with open(dbFile, 'w') as f:
            pass

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

    name = input("Enter your name: ")
    players[0].setName(name)
    players[1].setName("Bob")
    players[2].setName("Alice")
    players[3].setName("James")
    players[4].setName("Jacob")
    players[5].setName("Scott")
    insertFirstData()
    startPoker()


#Create class for player (Update later)
class Player:
    def __init__(self, name ,chipValue, wins, losses, betsPlaced):
        self.__name = name
        self.__chipValue = chipValue
        self.__wins = wins
        self.__losses = losses
        self.__betsPlaces = betsPlaced

    def getName(self):
        return self.__name

    def getChips(self):
        return self.__chipValue

    def getWins(self):
        return self.__wins

    def getLosses(self):
        return self.__losses

    def getBetsPlaced(self):
        return self.__betsPlaces
    
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


#Generates a random card without generating the same one twice
def generateCard():
    while True:

        cardSuit = random.choice(list(deck.keys()))
        cardType = random.choice(list(deck[cardSuit].keys()))

        if deck[cardSuit][cardType] != False:
            card = createCard(cardType, cardSuit)
            deck[cardSuit][cardType] = False
            return card, cardSuit, cardType


#Deals out the flop
def dealFlop():
    card1, cardSuit1, cardType1 = generateCard()
    card2, cardSuit2, cardType2 = generateCard()
    card3, cardSuit3, cardType3 = generateCard()
    cards = [card1, card2, card3]
    splitCards = [card.split("\n") for card in cards]

    for lines in zip(*splitCards):
        print(" ".join(lines))


#Deletes dbFile which then allows gamePlayed to be false again
def deleteData():
    os.remove(dbFile)


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


#Updates data of players in the database
def updateData(chipValue, wins, losses, betsPlaced, name):
    try:
        sqliteConnection = sqlite3.connect(dbFile)
        cursor = sqliteConnection.cursor()

        insertQuery = '''UPDATE player SET chipValue= ?,wins = ?,losses = ?,betsPlaced = ? WHERE name = ?'''

        cursor.execute(insertQuery, (chipValue, wins, losses, betsPlaced, name))


    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()


#Starting the poker round
def startPoker():
    print("We will now begin the game")
    print(f'Your name is {players[0].getName()}') # Testing
    dealer = random.choice(players)
    dealerIndex = players.index(dealer)
    print(f'The dealer is {dealer.getName()}')
    print("Pre Flop:")
    print(f"The player to the left of the dealer ({players[dealerIndex+1 % len(players)].getName()}) will place the small blind")
    if players[dealerIndex+1 % len(players)] == players[0]:
        sb = int(input("You are please place a small blind ($1-5): "))
        while sb not in range(1, 6):
            print("Please enter a value from 1 - 5")
            sb = int(input("You are please place a small blind ($1-5): "))


#Play Game
def playGame():
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
                firstPlay()
            elif choice == 2:
                print("Continuing last game")
                loadData()
                startPoker()
    else:
        firstPlay()


#Insertion Sort Algorithm
def leaderboardSort(stat):
    array = []
    for i in range(len(players)):
        if stat == "chipValue":
            value = players[i].getChips()
        elif stat == "wins":
            value = players[i].getWins()
        elif stat == "losses":
            value = players[i].getLosses()
        elif stat == "betsPlaced":
            value = players[i].getBetsPlaced()
        array.append([players[i], value])
        
    n = len(array)
        
    #Insertion Sort
    for i in range(1, n):
        current = array[i]
        previous = i - 1
        while previous >= 0 and current[1] > array[previous][1]:
            array[previous + 1] = array[previous]
            previous -= 1
        array[previous + 1] = current

    print(f'From highest to lowest for {stat}')

    for i in range(n):
        player = array[i][0]
        value = array[i][1]
        print(str(1+i) + ":", player.getName(), "-", str(value))
                

#Display sorted leaderboard of player stats
def viewStats():
    print("How would you like to sort stats by:")
    print("1: Most Chips")
    print("2: Most Wins")
    print("3: Most Losses")
    print("4: Most Bets Placed")
    choice = 0
    while choice not in [1, 2, 3, 4]:
        try:
            choice = int(input("Enter Choice: "))
        except:
            print("Please enter a correct option")
    if choice == 1:
        leaderboardSort("chipValue")
    elif choice == 2:
        leaderboardSort("wins")
    elif choice == 3:
        leaderboardSort("losses")
    elif choice == 4:
        leaderboardSort("betsPlaced")

#Exit
def endProgram():
    sys.exit()

def startProgram():
    print("Welcome to terminal poker")
    print("Please select what you would like to do")
    print("1: Play")
    print("2: View Player Stats")
    print("3: Exit")
    choice = 0
    while choice not in [1, 2, 3]:
        try:
            choice = int(input("Enter Choice: "))
        except:
            print("Please enter a correct option")
    if choice == 1:
        playGame()
    elif choice == 2:
        if gamePlayed:
            loadData()
        viewStats()
    elif choice == 3:
        endProgram()
    

#Running the program
startProgram()
