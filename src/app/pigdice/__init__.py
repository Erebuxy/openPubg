import random

from app.appClass import App

class PigDice(App):

    name = 'PigDice'

    def __init__(self, tManager):
        self.textManager = tManager
        self.playerList = []
        self.__running = False

    def help(self):
        ''' Print the help message '''
        return ''

    def isRunning(self):
        ''' Return whether the program is running '''
        return self.__running

    def _start(self):
        '''
        Run the app
        This method will execute the main logic of the app, including sending
        and receiving message through api and checking whether app should end
        '''

        # Send the basic information to the user and ask who start first
        msg = 'Welcome to the game of Pig. To win, '\
        'be the player with the most points at the end '\
        'of the game. The game ends at the end of a round '\
        'where at least one player has 25 or more points '\
        'On each turn, you may roll the die as many times '\
        'as you like to obtain more points. However, if '\
        'you get 1, your turn is over, and you do not obtain '\
        'any points that turn.'
        self.textManager.sendMessage(self.playerList[0], msg)
        self.textManager.sendMessage(self.playerList[1], msg)

        # Ask user for each move
        p1 = 0
        p2 = 0
        while p1 < 25 and p2 < 25:
            msg = ''
            msg += "Player 1 points: " + str(p1) + '\n'
            msg += "Player 2 points: " + str(p2)
            self.textManager.sendMessage(self.playerList[0], msg)
            self.textManager.sendMessage(self.playerList[1], msg)
            r = self.take_turn(0)
            p1 += r
            msg = ''
            msg += "Player 1 points: " + str(p1) + '\n'
            msg += "Player 2 points: " + str(p2)
            self.textManager.sendMessage(self.playerList[0], msg)
            self.textManager.sendMessage(self.playerList[1], msg)
            r = self.take_turn(1)
            p2 += r

        # Return the results
        msg = ''
        msg += "The game is over\n"
        msg += "Player 1 points: " + str(p1) + '\n'
        msg += "Player 2 points: " + str(p2)
        self.textManager.sendMessage(self.playerList[0], msg)
        self.textManager.sendMessage(self.playerList[1], msg)
        if p1>p2:
            msg = "Player 1 is the winner"
            self.textManager.sendMessage(self.playerList[0], msg)
            self.textManager.sendMessage(self.playerList[1], msg)
        elif p2>p1:
            msg = "Player 2 is the winner"
            self.textManager.sendMessage(self.playerList[0], msg)
            self.textManager.sendMessage(self.playerList[1], msg)
        else:
            msg = "Tie game"
            self.textManager.sendMessage(self.playerList[0], msg)
            self.textManager.sendMessage(self.playerList[1], msg)

    def canStart(self):
        ''' Check whether the app can start not '''
        if len(self.playerList) == 2:
            return True, ''
        return False, 'Don\'t have enough player'

    def addPlayer(self, playerId):
        '''
        Add a player to the current room
        Return True and success message if add successfully. Else, return false
        and error messages
        '''

        if len(self.playerList) < 2:
            self.playerList.append(playerId)
            return True, ''
        return False, 'Only two player allowed'

    def take_turn(self, player):
        ''' Handle each player's turn '''
        point = 0
        keep_rolling = 1
        msg = "It's your turn\n"
        msg += "send y to begin"
        y = self.textManager.doQA(self.playerList[player], msg, ['y'])
        while keep_rolling == 1:
            r = roll_die(6)
            msg = "You got " + str(r)
            self.textManager.sendMessage(self.playerList[player], msg)
            if r == 1:
                point = 0
                keep_rolling = 0
            else:
                point += r
                msg = "Your total is " + str(point) + '\n'
                msg += "do you want to continue? y=yes n=no"
                y = self.textManager.doQA(self.playerList[player], msg, ['y', 'n'])
                if y == 'y':
                    keep_rolling = 1
                else:
                    keep_rolling = 0
        msg = "your turn is over"
        self.textManager.sendMessage(self.playerList[player], msg)
        return point

def roll_die(sides):
    r = random.randrange(1, sides+1)
    return r
