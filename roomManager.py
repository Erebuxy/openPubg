import os
import threading

import app

class RoomManager:
    ''' A class that will run and manage all the play room '''

    def __init__(self, tManager, pManager):
        self.textManager = tManager
        self.playerManager = pManager

        self.current_number = 0

        self.roomDict = {}

    def createRoom(self, gameName):
        '''
        Create a room for given game type and return the room number.
        Return -1 if the given game doesn't exist
        '''

        if gameName == 'tictactoe':
            self.current_number += 1
            self.roomDict[self.current_number] = app.TicTacToe(self.textManager)
            return self.current_number

        return -1

    def addPlayer(self, id, roomId):
        ''' Add a player to a room '''
        if self.playerManager.getRoomId(id) is not None:
            return False, 'Player is currently in a game room'
        if roomId in self.roomDict:
            res, msg = self.roomDict[roomId].addPlayer(id)
            if res:
                self.playerManager.setRoomId(id, roomId)
                return True, ''
            else:
                return False, msg

    def startRoom(self, roomId):
        ''' Start a room '''
        if roomId not in self.roomDict:
            return False, 'Invalid room ID'
        if self.roomDict[roomId].__running:
            return False, 'The current game is running'
        
        self.roomDict[roomId].start()
        return True, ''

    def removePlayer(self, id, roomId):
        pass

    def stopRoom(self, roomId):
        pass

    def getCurrentRooms(self):
        pass

    def close(self):
        pass
        print('Room Manager Shutdown')

class Room:

    def __init__(self):
        pass
