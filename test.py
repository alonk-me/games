import random
import operator as op
from functools import reduce
from statistics import mode
total_dice = []  # create a list to store all the dice from all the players
player_list = [] #create a list to store all player names
last_bet = 0 # global variable used to store the last players bet
last_position = 0 # global variable used to store the last players position
last_player = None # # global variable used to store the last player object

def ncr(n, r):  # n = number of dice , r number of success
    r = min(r, n - r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer / denom

def p(t, r):  # r = number of successes, t = number of dice
    return ncr(t, r) * (1 / 6) ** r * (1 - (1 / 6)) ** (t - r)
    # number of combinations

def dice_chance(a, b):   # a = amount of dice calculated , b = amount of success requested
    probability = 0
    for i in range(b, a + 1):
        probability += (p(a, i))
    return probability
    # calculate the probability of success

class Player(object):
    player_bet = None
    player_position = None
    hand = None
    chance = None
    name = None
    bullshit = None
    dice = 5
    def __init__(self,i):
        self.name = i
    def player_hand(self):                   #creates random hand
        self.hand = [random.randrange(1, 7) for i in range(self.dice)]
        total_dice.extend(self.hand)
    def player_response(self):  #each player turn
        reloop = 0
        while reloop == 0:
            respone = input(str(self.name) + ' would you like to bet or call bullshit:') # sees what the player wants to do
            if respone == "bet":
                print(self.hand)
                self.player_bet = int(input('dice amount:'))  #takes in player guess
                self.player_position = int(input('dice position:'))
                if self.player_bet < last_bet: #makes sure the player is following the rules of the bets
                    print("You have to raise the stakes, please select a higher bet or a higher position then the previous player")
                elif self.player_bet == last_bet and self.player_position <= last_position:
                    print("please select a higher position then the previous player")
                elif self.player_position > 6 or self.player_position < 1:
                    print("please choose a number between 1 to 6") # makes sure the position makes sense
                else:
                    reloop += 1
            elif respone == "bullshit": #records bullshit
                self.bullshit = True
                reloop += 1
            else:
                print("please choose bet or bullshit")
    def player_statistics(self):  #odds to win
        self.chance = dice_chance(len(total_dice), self.player_bet)
        print(self.chance)



class GameMaster(object):
    current_bet = None
    current_position = None
    last_player = None
    plist = {}  #dictinary containing player names as keys and player object as values
    num_players = None
    challenging_player = None
    def __init__(self):
        pass

    def player_names(self):   # count how many people are playing
        relooper = 0 # looping agent
        stin = None # user input
        while relooper == 0:  ### need to add a checkr to make sure all the names are diffrent
            stin = input("how many players are playing:") #makes sure the input is string
            try:
                int(stin)
                relooper += 1

            except:
                print("please enter a digit")
        self.num_players = int(stin)
        for i in range(self.num_players):  # create a list with all the players name
            name = input("insert player name:")
            player_list.append(name)


        for i in player_list: # initilize player objects determined by amount of players
            p = Player(i)
            self.plist[i] = p

    def player_hand(self):   # intilize all players hands
        for pname in self.plist:
            self.plist[pname].player_hand()
    def round_loser(self): #decide on round loser
        print(total_dice)
        global last_position
        global last_bet
        s = total_dice.count(last_position) # amount of times the position actually appears in the dice
        joker = total_dice.count(1)
        print(str(s + joker) + ' times')  ### error: one is an exception to the counting method
        if s + joker >= last_bet:   # checks if the player that called bullshit was wrong
            print(self.challenging_player.name + ' loses')
            self.challenging_player.dice -= 1  #takes out a dice from the loser stack
            if self.challenging_player.dice == 0:
                self.plist.pop(self.challenging_player.name) # takes out the loser from the game if he is out of dice

        else:
            print(self.last_player.name + ' was bullshiting')
            self.last_player.dice -= 1 #takes out a dice from the loser stack
            if self.last_player.dice == 0:
                self.plist.pop(self.last_player.name) # takes out the loser from the game if he is out of dice
        last_bet = 0
        last_position = 0
        total_dice.clear()

    def round(self): #initiate betting round
        end_round = False
        while end_round == False:
            for pname in self.plist:
                self.plist[pname].player_response()

                if self.plist[pname].bullshit == True:  # ends round when bullshit is called
                    end_round = True
                    self.challenging_player = self.plist[pname]
                    self.plist[pname].bullshit = None

                    break

                else:  #saves the last position, amount, player object
                    global last_position
                    global last_bet
                    last_bet = self.plist[pname].player_bet
                    last_position = self.plist[pname].player_position
                    self.plist[pname].player_statistics() #shows the odds to win
                    self.last_player = self.plist[pname]

    def repeter(self):
        gamemaster.player_names()
        duration = len(self.plist.keys())
        while duration > 1:
            gamemaster.player_hand()
            gamemaster.round()
            gamemaster.round_loser()
            duration = len(self.plist.keys())
            if input(':') == 'stop':
                break
        for key in self.plist:
            print(key + ' wins')

gamemaster = GameMaster()
gamemaster.repeter()






