#Imports
import random
import sqlite3
import sys
import os
import time
from itertools import combinations
from collections import Counter


#So I don't need to type time.sleep every time
def wait(amount):
    time.sleep(amount)

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
            name VARCHAR(20) NOT NULL,
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
    while name.lower() in ["bob", "alice", "james", "jacob", "scott"]:
        print("Please choose a unique name")
        name = input("Enter your name: ")
    players[0].setName(name)
    players[1].setName("Bob")
    players[2].setName("Alice")
    players[3].setName("James")
    players[4].setName("Jacob")
    players[5].setName("Scott")
    insertFirstData()
    startPoker()


#Create class for player
class Player:
    def __init__(self, name ,chipValue, wins, losses, betsPlaced, currentHandScore, hasFolded):
        self.__name = name
        self.__chipValue = chipValue
        self.__wins = wins
        self.__losses = losses
        self.__betsPlaces = betsPlaced
        self.__currentHandScore = currentHandScore
        self.__hasFolded = hasFolded

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
    
    def getCurrentHandScore(self):
        return self.__currentHandScore
    
    def getHasFolded(self):
        return self.__hasFolded
    
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

    def setCurrentHandScore(self, amount):
        self.__currentHandScore = amount

    def setHasFolded(self, value):
        self.__hasFolded = value
        

players = [Player("placeholder", 1000, 0, 0, 0, 0, False) for i in range(6)]


#Creating suit dicts
cardsHearts = {i: True for i in range(2, 15)}
cardsDiamonds = {i: True for i in range(2, 15)}
cardsSpades = {i: True for i in range(2, 15)}
cardsClubs = {i: True for i in range(2, 15)}

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
        14: "A",
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


def dealPreFlop(playerName):
    card1, cardSuit1, cardType1 = generateCard()
    card2, cardSuit2, cardType2 = generateCard()

    if playerName == players[0].getName():
        cards = [card1, card2]
        splitCards = [card.split("\n") for card in cards]

        for lines in zip(*splitCards):
            print(" ".join(lines))

    card1 = [cardSuit1, cardType1]
    card2 = [cardSuit2, cardType2]

    return card1, card2


#Deals out the flop
def dealFlop():
    card1, cardSuit1, cardType1 = generateCard()
    card2, cardSuit2, cardType2 = generateCard()
    card3, cardSuit3, cardType3 = generateCard()
    cards = [card1, card2, card3]
    splitCards = [card.split("\n") for card in cards]

    for lines in zip(*splitCards):
        print(" ".join(lines))

    card1 = [cardSuit1, cardType1]
    card2 = [cardSuit2, cardType2]
    card3 = [cardSuit3, cardType3]

    cards = [card1, card2, card3]

    return cards


def dealNextRound(cards):
    card, cardSuit, cardType = generateCard()
    print(card)

    card = [cardSuit, cardType]

    cards.append(card)

    return cards


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
def updateData(player):
    chipValue = player.getChips()
    wins = player.getWins()
    losses = player.getLosses()
    betsPlaced = player.getBetsPlaced()
    name = player.getName()

    try:
        sqliteConnection = sqlite3.connect(dbFile)
        cursor = sqliteConnection.cursor()

        insertQuery = '''UPDATE player SET chipValue= ?,wins = ?,losses = ?,betsPlaced = ? WHERE name = ?'''

        cursor.execute(insertQuery, (chipValue, wins, losses, betsPlaced, name))

        sqliteConnection.commit()


    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()


#Determines hand strength
def determineHandStrength(hand):
    score = 0
    rank1 = hand[0][1]
    rank2 = hand[1][1]
    suit1 = hand[0][0]
    suit2 = hand[1][0]

    high = max(rank1, rank2)
    low = min(rank1, rank2)
    diff = abs(rank1 - rank2)

    if rank1 == rank2:
        score = 100 + rank1 * 3
    else:
        score = rank1 + rank2

        #For High Ranking cards in hands without a pair
        if high == 14: # Ace
            score += 14
        elif high == 13: # King
            score += 12
        elif high == 12: # Queen
            score += 8
        elif high == 11: # Jack
            score += 5

        #If both cards are high ranking but not a pair
        if rank1 >= 11 and rank2 >= 11:
            score += 8

    if suit1 == suit2: #suited bonus
        score += 10

    if diff == 1:
        score += 5 #Difference of 1 (consecutive) bonus

    if diff == 2:
        score += 5 #Difference of 2 (semi-consecutive) bonus

    score += random.randint(-5, 5) #Adds a level of randomness

    return score


#What the bot will do based off hand strength
def preFlopBotAlg(score):
    r = random.random()

    if score > 80:
        if r < 0.9:
            action = "raise"
        else:
            action = "fold"

    elif score > 50:
        if r < 0.7:
            action = "raise"
        else:
            action = "call"

    elif score > 30:
        if r < 0.8:
            action = "call"
        else:
            action = random.choice(["raise", "fold"])
    
    else:
        if r < 0.7:
            action = "fold"
        else: action = random.choice(["raise", "call"])

    return action


#Check how strong your 5 card hand is
def determine5HandStrength(cards, noisy=False):
    noise = random.randint(-2000, 2000) if noisy else 0

    ranks = [r for s,r in cards]
    suits = [s for s,r in cards]

    
    #Sorts ranks high to low
    ranksSorted = sorted(ranks, reverse=True)


    #Handle ace high and low
    unique = sorted(set(ranks))
    if 14 in unique:
        unique.append(1)


    #Detect straight
    straightHigh = 0
    for i in range(len(unique)-4):
        window = unique[i:i+5]
        if all(window[j]-window[j-1] == 1 for j in range(1, 5)):
            straightHigh = window[-1]

    
    #Detect Flush
    flush = None
    suitCounts = Counter(suits)
    for s, c in suitCounts.items():
        if c >= 5:
            flush = s
            break


    #Detect duplicates
    rankCounts = Counter(ranks)
    counts = sorted(rankCounts.values(), reverse=True)


    #Check straight flush
    if flush:
        flushCards = sorted([r for (s, r) in cards if s == flush])
        if 14 in flushCards:
            flushCards.append(1)

        for i in range(len(flushCards)-4):
            window = flushCards[i:i+5]
            if all(window[j]-window[j-1] == 1 for j in range(1, 5)):
                high = window[-1]
                if high == 14:  #Royal Flush
                    return 1000000 + noise
                else:
                    return 900000 + high * 10 + noise

    #Four of a kind
    if counts[0] == 4:
        quadRank = max(rank for rank, c in rankCounts.items() if c == 4)
        kicker = max(rank for rank, c in rankCounts.items() if c != 4)
        return 800000 + quadRank * 20 + kicker + noise

    #Full House
    if counts[0] == 3 and counts[1] >= 2:
        tripsRank = max(rank for rank, c in rankCounts.items() if c == 3)
        pairRank = max(rank for rank, c in rankCounts.items() if c >= 2 and rank != tripsRank)
        return 700000 + tripsRank * 20 + pairRank + noise

    #Flush
    if flush:
        sortedFlush = sorted([r for s, r in cards if s == flush], reverse=True)
        return 600000 + sum(sortedFlush[i] * (15 ** (4 - i)) for i in range(5)) + noise

    #Straight
    if straightHigh:
        return 500000 + straightHigh * 10 + noise

    #Three of a Kind
    if counts[0] == 3:
        tripsRank = max(rank for rank, c in rankCounts.items() if c == 3)
        kickers = sorted((r for r in ranks if r != tripsRank), reverse=True)
        return 400000 + tripsRank * 20 + kickers[0] * 2 + kickers[1] + noise

    #Two Pair
    if counts[0] == 2 and counts[1] == 2:
        pairs = sorted([rank for rank, c in rankCounts.items() if c == 2], reverse=True)
        kicker = max(rank for rank, c in rankCounts.items() if c == 1)
        return 300000 + pairs[0] * 30 + pairs[1] * 5 + kicker + noise

    #One Pair
    if counts[0] == 2:
        pairRank = max(rank for rank, c in rankCounts.items() if c == 2)
        kickers = sorted((r for r in ranks if r != pairRank), reverse=True)
        return 200000 + pairRank * 40 + kickers[0] * 4 + kickers[1] * 3 + kickers[2] + noise

    #High Card
    return 100000 + ranksSorted[0]*20 + ranksSorted[1]*5 + noise


def postBlindActions(score, hasBet):
    score = score/1000000
    r = random.random()
    action = "check"

    if score > 0.8:
        if not hasBet:
            if r < 0.85:
                action = "bet"
            else:
                action = "check"
        else:
            if r < 0.9:
                action = "raise"
            else:
                action = "call"
    
    elif score > 0.5:
        if not hasBet:
            if r < 0.6:
                action = "bet"
            else:
                action = "check"
        else:
            if r < 0.7:
                action = "call"
            else:
                action = "raise"

    elif score > 0.2:
        if not hasBet:
            if r < 0.4:
                action = "bet"
            else:
                action = random.choice(["check", "fold"])
        else:
            if r < 0.5:
                action = "call"
            else:
                action = random.choice(["raise", "fold"])

    else:
        if not hasBet:
            if r < 0.2:
                action = "bet"
            else:
                action = random.choice(["check", "fold"])
        else:
            if r < 0.3:
                action = "raise"
            else:
                action = action = random.choice(["call", "fold"])
            
    return action   


#Evaluates score for flop, turn and river
def evaluate(hand, tableCards, noisy=False):
    cards = list(hand) + list(tableCards)

    if len(cards) <=5:
        return determine5HandStrength(cards)
    else:
        bestScore = 0
        for combo in combinations(cards, 5):
            score = determine5HandStrength(combo)
            if score > bestScore:
                bestScore = score

        return bestScore


def postBlinds(stage, dealerIndex, playerHands, tableCards, pot):
    gameComplete = False

    print(f"{stage}:")
    
    wait(1)

    print(f"The {stage} cards are:")

    if stage == "Flop":
        tableCards = dealFlop()

    elif stage == "Turn":
        tableCards = dealNextRound(tableCards)

    elif stage == "River":
        tableCards = dealNextRound(tableCards)


    wait(1)

    betPlaced = False
    bettingActive = True
    resetIndex = False
    lastBetter = None
    previousRaise = 0
    currentBet = 0

    i = 0
    checkedThisRound = 0

    while bettingActive:
        print("tests")
        minRaise = previousRaise+currentBet

        if players[(dealerIndex+3+i) % len(players)] == players[0] and not betPlaced and not players[0].getHasFolded():
            print(f"Current bet is ${currentBet}, and minimum raise is ${minRaise}")
            print("It is your turn to choose, what would you like to do:")
            print("1: Bet")
            print("2: Check")
            print("3: Fold")
            choice = 0
            while choice not in [1, 2, 3]:
                try:
                    choice = int(input("Enter Choice: "))
                except:
                    print("Please enter a correct option")

            if choice == 1:
                while True:
                    try:
                        amount = int(input("Enter bet amount: "))
                        if amount > 0:
                            previousRaise = amount
                            currentBet = amount
                            print(f"You bet ${amount}")
                            players[0].increaseChips(-amount)
                            betPlaced = True
                            resetIndex = True
                            players[0].increaseBetsPlaced(1)
                            pot += amount
                            break
                        else:
                            print(f"Please enter an amount thats greater than 0")
                    except ValueError:
                        print(f"Please enter an amount thats greater than 0")
            

            elif choice == 2:
                print("You have checked")
                checkedThisRound += 1

            else:
                print("You have folded")
                players[0].setHasFolded(True)

            


        elif players[(dealerIndex+3+i) % len(players)] == players[0] and not players[0].getHasFolded():
            choice = 0
            print(f"Current bet is ${currentBet}, and minimum raise is ${minRaise}")
            print("It is your turn to choose, what would you like to do:")
            print("1: Raise")
            print("2: Call")
            print("3: Fold")

            while choice not in [1, 2, 3]:
                try:
                    choice = int(input("Enter Choice: "))
                except:
                    print("Please enter a correct option")

            if choice == 1:
                print(f"What would you like to raise the current bet to (must be at least the current bet + the previous raise: {minRaise})")

                while True:
                    try:
                        amount = int(input("Enter raise: "))
                        if amount >= minRaise:
                            previousRaise = amount - currentBet
                            currentBet = amount
                            print(f"You raised to ${amount}")
                            players[0].increaseChips(-amount)
                            players[0].increaseBetsPlaced(1)
                            pot += amount
                            break
                        else:
                            print(f"Please enter an amount thats greater than or equal to {minRaise}")
                    except ValueError:
                        print(f"Please enter an amount thats greater than or equal to {minRaise}")

            elif choice == 2:
                print(f'You called on ${currentBet}')
                players[0].increaseChips(-currentBet)
                players[0].increaseBetsPlaced(1)
                pot += currentBet

            elif choice == 3:
                print("You have folded")
                players[0].setHasFolded(True)
            
        
        else:
            if players[(dealerIndex+3+i) % len(players)].getHasFolded() == False:
                action = postBlindActions(evaluate(playerHands[(dealerIndex+3+i) % len(players)], tableCards, noisy=True), betPlaced)
            else:
                action = "out"

            if action == "bet":
                amount = random.randint(1, 10)
                print(f'{players[(dealerIndex+3+i) % len(players)].getName()}, bet {amount}')
                players[(dealerIndex+3+i) % len(players)].increaseChips(-amount)
                previousRaise = amount
                currentBet = amount
                players[(dealerIndex+3+i) % len(players)].increaseBetsPlaced(1)
                betPlaced = True
                resetIndex = True
                pot += amount


            elif action == "raise":
                amount = random.randint(minRaise, minRaise+10)
                players[(dealerIndex+3+i) % len(players)].increaseChips(-amount)
                previousRaise = amount-currentBet
                currentBet = amount
                print(f'{players[(dealerIndex+3+i) % len(players)].getName()}, raised to ${currentBet}')
                players[(dealerIndex+3+i) % len(players)].increaseBetsPlaced(1)
                pot += amount


            elif action == "call":
                players[(dealerIndex+3+i) % len(players)].increaseChips(-currentBet)
                print(f'{players[(dealerIndex+3+i) % len(players)].getName()}, called on ${currentBet}')
                players[(dealerIndex+3+i) % len(players)].increaseBetsPlaced(1)
                pot += currentBet

            elif action == "fold":
                players[(dealerIndex+3+i) % len(players)].setHasFolded(True)
                print(f"{players[(dealerIndex+3+i) % len(players)].getName()} has folded")

            elif action == "check":
                print(f"{players[(dealerIndex+3+i) % len(players)].getName()} has checked")
                checkedThisRound += 1

        if resetIndex:
            lastBetter = (dealerIndex+3+i) % len(players)
            resetIndex = False

        i += 1

        activePlayers = [p for p in players if not p.getHasFolded()]

        print(len(activePlayers))

        if checkedThisRound == len(activePlayers):
            bettingActive = False


        if lastBetter is not None and (dealerIndex+3+i) % len(players) == lastBetter:
            bettingActive = False


        if len(activePlayers) == 1:
            bettingActive = False
            gameComplete = True
            
        wait(1)
            

    return tableCards, gameComplete, pot


#Starting the poker round
def startPoker():
    for p in players:
        p.setHasFolded(False)

    gameComplete = False
    pot = 0

    print("We will now begin the game")

    wait(1.5)

    dealer = random.choice(players)
    dealerIndex = players.index(dealer)

    print(f'The dealer is {dealer.getName()}')
    
    wait(1.5)

    print("Setup:")
    

    wait(1.5)
    #Small Blind
    print(f"The player to the left of the dealer ({players[(dealerIndex+1) % len(players)].getName()}) will place the small blind")
    if players[(dealerIndex+1) % len(players)] == players[0]:
        while True:
            try:
                sb = int(input("Please place a small blind ($1-5): "))
                if sb in range(1, 6):
                    break
                else:
                    print("Please enter a value from 1 - 5")
            except ValueError:
                print("Please enter a value from 1 - 5")
    else:
        sb = random.randint(1, 5)
    print(f'{players[(dealerIndex+1) % len(players)].getName()} has placed a Small Blind of {sb}$')
    pot += sb


    wait(1.5)
    #Big Blind
    print(f"The player 2 the left of the dealer ({players[(dealerIndex+2) % len(players)].getName()}) will place the big blind")
    if players[(dealerIndex+2) % len(players)] == players[0]:
        while True:
            try:
                bb = int(input("Please place a big blind (usually double the small blind) ($2-10): "))
                if bb in range(2, 11) and bb > sb:
                    break
                else:
                    print("Please enter a value from 2 - 10 and greater than the small blind")
            except ValueError:
                print("Please enter a value from 2 - 10 and greater than the small blind")
    else:
        bb = sb*2
    print(f'{players[(dealerIndex+2) % len(players)].getName()} has placed a Big Blind of {bb}$')
    pot += bb

    
    wait(1.5)
    #Pre Flop
    print("Pre Flop:")
    print("Your hole cards are: ")

    playerHands = [dealPreFlop(player.getName()) for player in players]

    for i in range(6):
        players[i].setCurrentHandScore(determineHandStrength(playerHands[i]))
    
    wait(1.5)
    print('The players starting to the left of the Big Blind will now chose what to do')
    
    previousRaise = bb
    currentBet = bb

    numFolded = 0

    if numFolded < 5:

        for i in range(6):

            minRaise = previousRaise+currentBet

            if players[(dealerIndex+3+i) % len(players)] == players[0]:
                print(f"Current bet is ${currentBet}, and minimum raise is ${minRaise}")
                print("It is your turn to choose, what would you like to do:")
                print("1: Raise")
                print("2: Call")
                print("3: Fold")
                choice = 0
                while choice not in [1, 2, 3]:
                    try:
                        choice = int(input("Enter Choice: "))
                    except:
                        print("Please enter a correct option")

                if choice == 1:
                    print(f"What would you like to raise the current bet to (must be at least the current bet + the previous raise: {minRaise})")
                    
                    while True:
                        try:
                            amount = int(input("Enter raise: "))
                            if amount >= minRaise:
                                previousRaise = amount - currentBet
                                currentBet = amount
                                print(f"You raised to ${amount}")

                                if players[(dealerIndex+3+i) % len(players)] == players[(dealerIndex+1) % len(players)]:
                                    players[0].increaseChips(-(amount-sb))
                                    pot += amount-sb

                                elif players[(dealerIndex+3+i) % len(players)] == players[(dealerIndex+2) % len(players)]:
                                    players[0].increaseChips(-(amount-bb))
                                    pot += amount-bb

                                else:
                                    players[0].increaseChips(-amount)
                                    pot += amount

                                players[0].increaseBetsPlaced(1)
                                break
                            else:
                                print(f"Please enter an amount thats greater than or equal to {minRaise}")
                        except ValueError:
                            print(f"Please enter an amount thats greater than or equal to {minRaise}")

                elif choice == 2:
                    print(f'You called on ${currentBet}')
                
                    if players[(dealerIndex+3+i) % len(players)] == players[(dealerIndex+1) % len(players)]:
                        players[(dealerIndex+3+i) % len(players)].increaseChips(-(currentBet-sb))
                        pot += currentBet-sb

                    elif players[(dealerIndex+3+i) % len(players)] == players[(dealerIndex+1) % len(players)]:
                        players[(dealerIndex+3+i) % len(players)].increaseChips(-(currentBet-bb))
                        pot += currentBet-bb

                    else:
                        players[(dealerIndex+3+i) % len(players)].increaseChips(-currentBet)
                        pot += currentBet

                    players[(dealerIndex+3+i) % len(players)].increaseBetsPlaced(1)

                elif choice == 3:
                    print("You have folded")
                    players[0].setHasFolded(True)
                    numFolded += 1



            else:
                action = preFlopBotAlg(players[(dealerIndex+3+i) % len(players)].getCurrentHandScore())

                if action == "raise":
                    amount = random.randint(minRaise, minRaise+10)

                    if players[(dealerIndex+3+i) % len(players)] == players[(dealerIndex+1) % len(players)]:
                        players[(dealerIndex+3+i) % len(players)].increaseChips(-(amount-sb))
                        pot += amount-sb
                    elif players[(dealerIndex+3+i) % len(players)] == players[(dealerIndex+2) % len(players)]:
                        players[(dealerIndex+3+i) % len(players)].increaseChips(-(amount-bb))
                        pot += amount-bb
                    else:
                        players[(dealerIndex+3+i) % len(players)].increaseChips(-amount)
                        pot += amount

                    previousRaise = amount-currentBet
                    currentBet = amount
                    print(f'{players[(dealerIndex+3+i) % len(players)].getName()}, raised to ${currentBet}')
                    players[(dealerIndex+3+i) % len(players)].increaseBetsPlaced(1)


                elif action == "call":
                    if players[(dealerIndex+3+i) % len(players)] == players[(dealerIndex+1) % len(players)]:
                        players[(dealerIndex+3+i) % len(players)].increaseChips(-(currentBet-sb))
                        pot += currentBet-sb

                    elif players[(dealerIndex+3+i) % len(players)] == players[(dealerIndex+1) % len(players)]:
                        players[(dealerIndex+3+i) % len(players)].increaseChips(-(currentBet-bb))
                        pot += currentBet-bb

                    else:
                        players[(dealerIndex+3+i) % len(players)].increaseChips(-currentBet)
                        pot += currentBet

                    print(f'{players[(dealerIndex+3+i) % len(players)].getName()}, called on ${currentBet}')
                    players[(dealerIndex+3+i) % len(players)].increaseBetsPlaced(1)


                elif action == "fold":
                    players[(dealerIndex+3+i) % len(players)].setHasFolded(True)
                    print(f"{players[(dealerIndex+3+i) % len(players)].getName()} has folded")
                    numFolded += 1

            wait(1.5)

    else:
        for i in range(6):
            if players[i].getHasFolded() == False:
                print(f"Everyone else has folded, therefore {players[i].getName()} wins a pot of {pot}")
                players[i].increaseChips(pot)
                gameComplete = True

    gameEnd = False

    if not gameComplete:

        tableCards, gameComplete, pot = postBlinds("Flop", dealerIndex, playerHands, "", pot)
    
    else:
        for i in range(6):
            if players[i].getHasFolded() == False:
                print(f"Everyone else has folded, therefore {players[i].getName()} wins a pot of {pot}")
                players[i].increaseChips(pot)
                gameEnd = True
                wait(0.5)
                break
    
    if not gameEnd:

        if not gameComplete:

            tableCards, gameComplete, pot = postBlinds("Turn", dealerIndex, playerHands, tableCards, pot)

        else:

            for i in range(6):
                if players[i].getHasFolded() == False:
                    print(f"Everyone else has folded, therefore {players[i].getName()} wins a pot of {pot}")
                    players[i].increaseChips(pot)
                    gameEnd = True
                    wait(0.5)
                    break

    if not gameEnd:

        if not gameComplete:

            tableCards, gameComplete, pot = postBlinds("River", dealerIndex, playerHands, tableCards, pot)

        else:

            for i in range(6):
                if players[i].getHasFolded() == False:
                    print(f"Everyone else has folded, therefore {players[i].getName()} wins a pot of {pot}")
                    players[i].increaseChips(pot)
                    gameEnd = True
                    wait(0.5)
                    break
    
    if not gameEnd:

        if not gameComplete:
            nonFoldedIndex = []

            for i in range(6):
                if players[i].getHasFolded() == False:
                    players[i].setCurrentHandScore(evaluate(playerHands[i], tableCards))
                    nonFoldedIndex.append(i)

            highestScore = 0
            winningIndex = 0

            for i in range(6):
                if i == nonFoldedIndex:
                    if players[i].getCurrentHandScore() > highestScore:
                        highestScore = players[i].getCurrentHandScore()
                        winningIndex = i

            wait(1)

            print("Showdown:")

            wait(0.5)

            print(f"The player with the winning hand was {players[winningIndex].getName()}")
            wait(0.5)
            if winningIndex == 0:
                print(f"Well done, you have won a pot of {pot}")
                players[0].increaseChips(pot)
            else:
                print(f"{players[winningIndex].getName()} has won a pot of {pot}")
                players[winningIndex].increaseChips(pot)

            wait(0.5)


        else:

            for i in range(6):
                if players[i].getHasFolded() == False:
                    print(f"Everyone else has folded, therefore {players[i].getName()} wins a pot of {pot}")
                    players[i].increaseChips(pot)
                    wait(0.5)
                    break

    print("That concludes this round of poker")

    
    for player in players:
        updateData(player)

    wait(2)

    startProgram()


#Play Game
def playGame():
    print("In this game there will be 6 players including yourself")

    if gamePlayed:
        print("Would you like to continue where you left off?")
        print("1: Yes")
        print("2: No")
        choice = 0
        while choice not in [1, 2]:
            try:
                choice = int(input("Enter Choice: "))
            except:
                print("Please enter a correct option")
        if choice == 1:
            print("Loading player data")
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

    wait(1)

    startProgram()
                

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

#Starts the program off
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
