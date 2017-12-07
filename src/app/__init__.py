from app.appClass import App
from app.tictactoe import TicTacToe
from app.pigdice import PigDice
from app.helloworld import HelloWorld


app_dict = {'tictactoe': TicTacToe, 'pigdice': PigDice, 'helloworld': HelloWorld}

def haveApp(appName):
    ''' Check whether the app exist '''
    return appName in app_dict

def createApp(appName, textManager):
    ''' Create the app '''
    if not haveApp(appName):
        return None

    return app_dict[appName](textManager)
