import email
import getpass
import httplib2
import os
from queue import Queue
import threading
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = './client_secret.json'
APPLICATION_NAME = 'openPubg'

REMOVE_UNREAD = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}

class TextManager:
    ''' A class that will send, recieve and manage all the text message '''

    def __init__(self, worker=2, checkInterval=5):
        # Room Manager
        self.roomManager = None
        # Is room manager set
        self.__rManagerSet = False

        # The interval for checking emails (in s)
        self.checkInterval = checkInterval

        # Server
        self.__credentials = None
        self.__server = None

        # Config for number of worker
        self.workerNum = worker
        # List of all the current worker
        self.__workerList = []
        # Queue
        self.__q = Queue()

        # If text manager running
        self.__running = False

    def emailLogin(self):
        '''
        Login email through username and password
        Return True if login successfully. Else return False.
        '''

        self.__credentials = get_credentials()
        http = self.__credentials.authorize(httplib2.Http())
        self.__service = discovery.build('gmail', 'v1', http=http)

        return True

    def setRoomManager(self, rManager):
        ''' Set the room manager '''
        self.roomManager = rManager
        self.__rManagerSet = True

    def run(self):
        ''' Create all the workers and constantly checking email '''
        self.__running = True

        # Start workers in multithreading
        for _ in range(self.workerNum):
            self.__workerList.append(threading.Thread(target=self.__parseWorker))
            self.__workerList[-1].daemon = True
            self.__workerList[-1].start()

        # Constantly check email
        while self.__running:
            self.checkEmail()
            time.sleep(self.checkInterval)

    def __parseWorker(self):
        ''' Worker that parse and execute receuved text in queue '''
        while self.__running:
            message = self.__q.get()
            self.parseMessage(message)

    def checkMessage(self):
        ''' Check and pull new messages '''
        # Get all unread message
        unreadMsg = self.__service.users().messages().list(userId='me',
                                                           labelIds=['UNREAD']).execute()
        # If any
        if unreadMsg['resultSizeEstimate'] != 0:
            for msg in unreadMsg['messages']:
                msgId = msg['id']
                # Get unread message
                message = self.__service.users().messages().get(userId='me',
                                                                id=msgId).execute()
                # Add message to queue
                self.__q.put_nowait(message)
                # Remove unread label
                self.__service.users().messages().modify(userId='me', id=msgId,
                                                         body=REMOVE_UNREAD).execute()

    def sendMessage(self, targets, txt):
        ''' Send text message to user '''
        pass

    def parseMessage(self, message):
        ''' Parse the received message '''
        print(message['snippet'])
        pass

    def doVote(self, targets, options=set(['yes', 'no'])):
        ''' Start a vote '''
        pass

    def close(self):
        ''' Close text manager '''
        self.__running = False
        print('Text Manager Shutdown')

# Source: https://developers.google.com/gmail/api/quickstart/python
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('./')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, None)
        print('Storing credentials to ' + credential_path)
        print()
    return credentials
