import cmd
import sys

class openPubgShell(cmd.Cmd):
    '''
    A simple command line interface for the openPubg server
    The user can create, manage, delete rooms or players through
    command
    '''

    intro = 'Welcome to the openPubg Shell\n'
    prompt = 'openPubg>> '
    file = None

    def setRoomManager(self, rManager):
        self.roomManger = rManager

    def do_echo(self, arg):
        ''' Echo '''
        print(arg)

    def do_list(self):
        ''' List all current rooms '''
        pass

    def do_stop(self, arg):
        ''' Stop a current room '''
        pass

    def do_quit(self, arg):
        return True
