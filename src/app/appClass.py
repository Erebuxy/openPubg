class App(object):

    name = 'AppName'

    def __init__(self, tManager):
        self.textManager = tManager
        self.playerList = []
        self.__running = False

    def help(self):
        ''' Print the help message '''
        return ''

    def start(self):
        ''' Wrapper for __start '''

        self.__running = True
        res = self._start()
        self.__running = False

        return res

    def _start(self):
        '''
        Run the app
        This method will execute the main logic of the app, including sending
        and receiving message through api and checking whether app should end
        '''

        raise NotImplementedError('App.__start() not implemented')

    def canStart(self):
        ''' Check whether the app can start not '''
        raise NotImplementedError('App.canStart() not implemented')

    def addPlayer(self, playerId):
        '''
        Add a player to the current room
        Return True and success message if add successfully. Else, return false
        and error messages
        '''

        self.playerList.append(playerId)
        return True, ''

    def removePlayer(self, playerId):
        '''
        Remove a player from the room
        Return True and success message if add successfully. Else, return false
        and error messages
        '''

        raise NotImplementedError('App.removePlayer() not implemented')
