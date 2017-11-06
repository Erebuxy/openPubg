from sys import exit
from random import randint
from board import Board, HUMAN, COMPUTER


def humanize_coord(coord):
    if coord == HUMAN:
        return 'O'
    elif coord == COMPUTER:
        return 'X'
    else:
        return ' '

def print_board(board):
    for x in range(board.max_width):
        print ("-------------------------------")
        print ("|         |         |         |")
        print ("|    %s    |    %s    |    %s    |" % \
            (humanize_coord(board.board[x][0]), humanize_coord(board.board[x][1]), humanize_coord(board.board[x][2])))
        print ("|         |         |         |")
    print ("-------------------------------")

print ("=============")
print ("  Tic Tac Toe   ")
print ("=============")
print

number = None
while not number in ["1", "2", "0"]:
    print (" -------------------------------------")
    print ("|    0,0     |    0,1     |   0,2     |")
    print (" -------------------------------------")
    print ("|    1,0     |    1,1     |   1,2     |")
    print (" -------------------------------------")
    print ("|    2,0     |    2,1    |    2,2     |")
    print (" -------------------------------------")
    print("The above is the board.")
    print("The numbers inside represent the block index")
    # print("Just Type it")
    print("(X,Y) eg. (0,1) X = 0, Y = 1")
    print ("Choose who should start the game first?")
    print
    print ("              1) You")
    print ("              2) Super Computer")
    print
    print ("              0) Exit game, but return later")
    print
    if number == None:
        number = input("Enter number")
    else:
        number = input("only numbers are allowed: ")
    print

board = Board()

if number == "1":
    print ("Ok, you will start the game first!")
    print
    board.player_starts(HUMAN)
    print_board(board)
elif number == "2":
    print ("Computer starts the game")
    print
    board.player_starts(COMPUTER)
    board.put(randint(0, 2), randint(0, 2), COMPUTER)
    print_board(board)
else:
    exit(0)

while board.get_winner() == None:
    print
    if board.player_turn() == HUMAN:
        x = int(input("Now is your turn. Enter X coord starting from 0 to 2: "))
        y = int(input("                  Enter Y coord starting from 0 to 2: "))
        print
        while x not in [0, 1, 2] or y not in [0, 1, 2] or not board.can_put(x, y):
            first = False
            if x not in [0, 1, 2] or y not in [0, 1, 2]:
                print ("invalid coords. Please try again.")
            else:
                print ("This is reserved place. Choose another one!")
            print
            x = int(input("Enter X coord starting from 0 to 2: "))
            y = int(input("Enter Y coord starting from 0 to 2: "))
            print
    else:
        print ("Computer thinking...")
        print
        move = board.get_best_move()
        x = move[0]
        y = move[1]

    board.put(x, y, board.player_turn())
    print_board(board)

print
if board.get_winner() == COMPUTER:
    print ("Computer win.")
elif board.get_winner() == HUMAN:
    print ("You win.")
else:
    print ("Draw!")

print
input("Game ended, hope you will return back for more. Press ENTER to close...")
