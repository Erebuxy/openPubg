
from app.appClass import App

class HelloWorld(App):

    name = 'HelloWorld'

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

        msg = 'Hello World!\n'
        self.textManager.sendMessage(self.playerList[0], msg)

    def canStart(self):
        ''' Check whether the app can start not '''
        if len(self.playerList) > 0:
            return True, ''
        return False, ''
