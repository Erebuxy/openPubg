import os
from queue import Queue

class TextManager:
    ''' A class that will send, recieve and manage all the text message '''

    def __init__(self):
        self.roomManager = None
        self.__rManagerSet = False

    def setRoomManager(self, rManager):
        ''' Set the room manager '''
        self.roomManager = rManager
        self.__rManagerSet = True

    def run(self):
        '''
        '''

        pass

    def checkTxt(self):
        ''' Check the inbox '''
        pass

    def sendTxt(self, targets, txt):
        ''' Send text message to user '''
        pass

    def parseTxt(self, txt):
        ''' Parse the receuved text '''
        pass

    def doVote(self, targets, options=set(['yes', 'no'])):
        ''' Start a vote '''
        pass
