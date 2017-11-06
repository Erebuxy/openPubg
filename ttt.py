def welcome_message():
    print("=========================")
    print("Welcome to the OpenPUBG")
    print("Tic Tac Toe")
    print("=========================")


def Show_the_rule():
    print (" -------------------------------")
    print ("|    0     |    1     |   2     |")
    print (" -------------------------------")
    print ("|    3     |    4     |   5     |")
    print (" -------------------------------")
    print ("|    6     |    7    |    8     |")
    print (" -------------------------------")
    print("The above is the board.")
    print("The numbers inside represent the block index")
    print("Just Type it")
    str = raw_input("Are u ready for the game?(Y/N): ")
    if str == "Y" or str == "y":
        print("Now start the game...")
        Start_the_game()
    elif str == "N" or str == "n":
        print("Exiting the game...")


def check_valid(index, data,counter):
    if index in data:
        print("The block is occupied")
        return counter
    else:
        print("success...")
        data.append(index)
        temp = counter + 1
        return temp


def Start_the_game():
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    counter = 0
    while (counter < 9):
        index = raw_input("your turn(enter a valid number(0-8)):")
        if 0 <= index <10:
            print("counter%s", counter)
            counter = check_valid(index, data, counter)
        else:
            print("pls enter a valid number(0-8)")
            


welcome_message()
Show_the_rule()
