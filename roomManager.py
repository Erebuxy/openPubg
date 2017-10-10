import os
import threading

import app

class RoomManager:
    '''A class that will run and manage all the play room'''

    def __init__(self, tManager):
        self.TextManager = tManager

    def createRoom(self, gameName):
        pass

    def addPlayer(self, id, roomId):
        pass

    def removePlayer(self, id, roomId):
        pass

    def runRoom(self, roomId):
        pass

    def stopRoom(self, roomId):
        pass

    def getCurrentRooms(self):
        pass
