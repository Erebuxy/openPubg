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

    def createRoom(self, appName):
        '''
        Create a room for given game type and return the room number.
        Return -1 if the given game doesn't exist
        '''

        if app.haveApp(appName):
            self.current_number += 1
            self.roomDict[self.current_number] = app.createApp(appName, self.textManager)
            return self.current_number

        return -1

    def addPlayer(self, id, roomId):
        ''' Add a player to a room '''
        if self.playerManager.getRoomId(id) is not None:
            return False, 'Player is currently in another game room. Please '\
                          'leave the room before joinning.'
        if roomId not in self.roomDict:
            return False, 'Invalid room ID'
        res, msg = self.roomDict[roomId].addPlayer(id)
        if res:
            self.playerManager.setRoomId(id, roomId)
            return True, ('Joined room %d' %roomId)
        else:
            return False, msg

    def removePlayer(self, id, roomId):
        ''' Remove a player from his/her current room '''
        if roomId is None:
            return False, 'User is not in any room currently'
        if roomId not in self.roomDict:
            return False, 'Invalid room ID'
        if self.roomDict[roomId].isRunning():
            return False, 'Can\'t leave the room while game is running'

        self.roomDict[roomId].playerList.remove(id)
        self.playerManager.setRoomId(id, None)

        if len(self.roomDict[roomId].playerList) == 0:
            del self.roomDict[roomId]

        return True, 'You have been removed from the room'


    def startRoom(self, roomId):
        ''' Start a room '''
        if roomId not in self.roomDict:
            return False, 'Invalid room ID'
        if self.roomDict[roomId].isRunning():
            return False, 'The current game is running'

        res, msg = self.roomDict[roomId].canStart()
        if not res:
            return False, msg
        self.roomDict[roomId].start()

        msg = 'Game exited. Please reply "quit" to leave the room, and replay '\
              '"start" to restart the game.'
        for player in self.roomDict[roomId].playerList:
            self.textManager.sendMessage(player, msg)

        return True, ''

    def getCurrentRooms(self):
        ''' Return all the current room '''
        l = []
        for i in self.roomDict:
            l.append((i, self.roomDict[i].name))

        return l

    def close(self):
        ''' Prepare to close the room manager '''
        print('Room Manager Shutdown')
