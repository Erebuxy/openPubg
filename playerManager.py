import os

class Player:
    '''A player class that stores the user name, and phone number'''

    def __init__(self, id):
        self.name = ''
        self.phoneNumber = id
        self.task = None
        self.roomId = None


class PlayerManager:
    '''A class that will store and manager all the user profile'''

    def __init__(self):
        self.mainDict = {}

    def addPlayer(self, id):
        ''' Add a player to the dictionary '''
        self.mainDict[id] = Player(id)

    def setName(self, id, name):
        ''' Set the name of a player '''
        self.mainDict[id].name = name

    def getName(self, id):
        ''' Get the current task of a player '''
        return self.mainDict[id].name

    def setRoomId(self, id, roomID):
        ''' Set the current room ID of a player '''
        self.mainDict[id].roomId = roomID

    def getRoomId(self, id):
        ''' Get the current room ID of a player '''
        return self.mainDict[id].roomId

    def setTask(self, id, task):
        ''' Set the current task of a player '''
        self.mainDict[id].task = task

    def getTask(self, id):
        ''' Get the current task of a player and set it to None'''
        task = self.mainDict[id].task
        self.mainDict[id].task = None
        return task

    def havePlayer(self, id):
        ''' Check whether a player in the dictionary '''
        return (id in self.mainDict)
