from random import randint

from app.appClass import App
from app.tictactoe.board import Board, HUMAN, COMPUTER

class TicTacToe(App):

    name = 'TicTacToe'
    playerList = []

    def __init__(self, tManager):
        self.textManager = tManager
        self.__running = False

    def help(self):
        ''' Print the help message '''
        return ''

    def isRunning(self):
        ''' Return whether the program is running '''
        return self.__running

    def start(self):
        '''
        Run the app
        This method will execute the main logic of the app, including sending
        and receiving message through api and checking whether app should end
        '''
        if self.__running:
            Return
        self.__running = True

        # Send the basic information to the user and ask who start first
        msg = ' -------------------------------------\n'\
              '|    0,0     |    0,1     |   0,2     |\n'\
              ' -------------------------------------\n'\
              '|    1,0     |    1,1     |   1,2     |\n'\
              ' -------------------------------------\n'\
              '|    2,0     |    2,1    |    2,2     |\n'\
              ' -------------------------------------\n'\
              'The above is the board.\n'\
              'The numbers inside represent the block index\n'\
              '(X,Y) eg. (0,1) X = 0, Y = 1\n\n'\
              'Choose who should start the game first?\n'\
              '              1) You\n'\
              '              2) Super Computer\n'\
              '              0) Exit game, but return later'
        self.textManager.sendMessage(self.playerList[0], msg)
        number = self.textManager.doQA(self.playerList[0], '', ['1', '2', '0'])

        board = Board()

        if number == '1':
            msg = 'Ok, you will start the game first!\n\n'
            board.player_starts(HUMAN)
            msg += getBoard(board)
        elif number == '2':
            msg = 'Computer starts the game\n\n'
            board.player_starts(COMPUTER)
            board.put(randint(0, 2), randint(0, 2), COMPUTER)
            msg += getBoard(board)
        else:
            return

        self.textManager.sendMessage(self.playerList[0], msg)

        # Ask user for each move
        while board.get_winner() == None:
            print
            if board.player_turn() == HUMAN:
                x = self.textManager.doQA(self.playerList[0],
                                          'Now is your turn.\nEnter X coord starting from 0 to 2: ',
                                          ['1', '2', '0'])
                y = self.textManager.doQA(self.playerList[0],
                                          'Enter Y coord starting from 0 to 2: ',
                                          ['1', '2', '0'])
                x = int(x)
                y = int(y)

                while not board.can_put(x, y):
                    msg = "This is reserved place. Choose another one!"
                    self.textManager.sendMessage(self.playerList[0], msg)

                    x = self.textManager.doQA(self.playerList[0],
                                              'Now is your turn.\nEnter X coord starting from 0 to 2: ',
                                              ['1', '2', '0'])
                    y = self.textManager.doQA(self.playerList[0],
                                              'Enter Y coord starting from 0 to 2: ',
                                              ['1', '2', '0'])
                    x = int(x)
                    y = int(y)
            else:
                move = board.get_best_move()
                x = move[0]
                y = move[1]

            board.put(x, y, board.player_turn())
            msg = getBoard(board)
            self.textManager.sendMessage(self.playerList[0], msg)

        # Return the results
        if board.get_winner() == COMPUTER:
            self.textManager.sendMessage(self.playerList[0], 'Computer win.')
        elif board.get_winner() == HUMAN:
            self.textManager.sendMessage(self.playerList[0], 'You win!')
        else:
            self.textManager.sendMessage(self.playerList[0], 'Draw.')

        self.__running = False

    def canStart(self):
        ''' Check whether the app can start not '''
        if len(self.playerList) != 0:
            return True, ''
        return False, 'Don\'t have enough player'

    def addPlayer(self, playerId):
        '''
        Add a player to the current room
        Return True and success message if add successfully. Else, return false
        and error messages
        '''
        if len(self.playerList) == 0:
            self.playerList.append(playerId)
            return True, ''
        return False, 'Only one player allowed'

def humanize_coord(coord):
    if coord == HUMAN:
        return 'O'
    elif coord == COMPUTER:
        return 'X'
    else:
        return ' '

def getBoard(board):
    s = ''
    for x in range(board.max_width):
        s += '-------------------------------\n'
        s += '|    %s    |    %s    |    %s    |\n' % \
             (humanize_coord(board.board[x][0]),
              humanize_coord(board.board[x][1]),
              humanize_coord(board.board[x][2]))
    s += '-------------------------------\n'
    return s
