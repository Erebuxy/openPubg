import cmd
import logging
import sys

class openPubgShell(cmd.Cmd):
    '''
    A simple command line interface for the openPubg server
    The user can create, manage, delete rooms or players through
    command
    '''

    intro = 'Welcome to the openPubg Shell\n'
    prompt = 'openPubg>> \n'
    file = None

    def setRoomManager(self, rManager):
        self.roomManager = rManager

    def setTextManager(self, tManager):
        self.textManager = tManager

    def do_echo(self, arg):
        ''' Echo '''
        print(arg)

    def do_list(self, arg):
        ''' List all current rooms '''
        l = self.roomManager.getCurrentRooms()
        print('%d rooms running' %(len(l)))
        for i in l:
            print(i[0], i[1])

    def do_send(self, arg):
        ''' Send message to user '''
        email = input('Please enter email: ')
        text = input('Please enter message: ')

        message = self.textManager.sendMessage(email, text)

        if message is None:
            print('Send message failed')
        else:
            print('Send message with id %s' %(message['id']))

    def do_info(self, arg):
        ''' Show logging info '''
        logging.basicConfig(level=logging.INFO)

    def do_quit(self, arg):
        self.roomManager.close()
        self.textManager.close()
        return True
