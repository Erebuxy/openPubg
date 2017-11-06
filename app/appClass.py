class App(object):

    name = 'AppName'

    __textManager = None
    playerList = []

    def __init__(self):
        pass

    def setTextManager(self, tManager):
        ''' Set teh text manager '''
        self.__textManager = tManager

    def help(self):
        ''' Print the help message '''
        return ''

    def start(self):
        '''
        Run the app
        This method will execute the main logic of the app, including sending
        and receiving message through api and checking whether app should end
        '''

        raise NotImplementedError('App.run() not implemented')

    def canStart(self):
        ''' Check whether the app can start not '''
        raise NotImplementedError('App.canStart() not implemented')

    def addPlayer(self, playrId):
        '''
        Add a player to the current room
        Return True and success message if add successfully. Else, return false
        and error messages
        '''

        playerList.append(playerId)
        return True, ''

    def removePlayer(self, playerId):
        '''
        Remove a player from the room
        Return True and success message if add successfully. Else, return false
        and error messages
        '''

        raise NotImplementedError('App.removePlayer() not implemented')
