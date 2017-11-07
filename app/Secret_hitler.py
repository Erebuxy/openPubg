def check_ready():

    str = raw_input("Are u ready for the game?(Y/N): ");
    if str == "Y":
        print("Ready now. Waiting for other players...")
    if str == "N":
        print("OK, we are waiting for u...")

def Secret_Hitler():
    print("===============")
    print("Secret_Hitler")
    print("===============")
    check_ready()




Secret_Hitler()
