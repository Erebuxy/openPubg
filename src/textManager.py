import base64
import logging
from email.mime.text import MIMEText
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


LOCK = threading.Lock()

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = './client_secret.json'
APPLICATION_NAME = 'openPubg'

REMOVE_UNREAD = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}

class TextManager:
    ''' A class that will send, recieve and manage all the text message '''

    def __init__(self, worker=5, checkInterval=3):

        # Room Manager
        self.roomManager = None
        # Player Manager
        self.playerManager = None
        # Is room manager set
        self.__rManagerSet = False
        self.__pManagerSet = False

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

        # Set current number
        self.__waitQs = {}
        self.__queueNumber = 0

    def emailLogin(self):
        '''
        Login email through username and password
        Return True if login successfully. Else return False.
        '''

        self.__credentials = get_credentials()
        http = self.__credentials.authorize(httplib2.Http())
        self.__service = discovery.build('gmail', 'v1', http=http)

        self.__user = self.__service.users().getProfile(userId='me').execute()
        self.email = self.__user['emailAddress']
        logging.info('Logged in %s' %(self.email))
        print('Logged in %s' %(self.email))

        return True

    def setRoomManager(self, rManager):
        ''' Set the room manager '''
        self.roomManager = rManager
        self.__rManagerSet = True

    def setPlayerManager(self, pManager):
        ''' Set the player manager '''
        self.playerManager = pManager
        self.__pManagerSet = True

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
            self.checkMessage()
            time.sleep(self.checkInterval)

    def __parseWorker(self):
        ''' Worker that parse and execute receuved text in queue '''
        while self.__running:
            message = self.__q.get()
            self.parseMessage(message)
            self.__q.task_done()

    def checkMessage(self):
        ''' Check and pull new messages '''
        try:
            with LOCK:
                # Get all unread message
                unreadMsg = self.__service.users().messages().list(userId='me',
                                                                   labelIds=['UNREAD']).execute()
            # If any
            if unreadMsg['resultSizeEstimate'] != 0:
                for msg in unreadMsg['messages']:
                    msgId = msg['id']
                    with LOCK:
                        # Get unread message
                        message = self.__service.users().messages().get(userId='me',
                                                                        id=msgId).execute()
                        # Add message to queue
                        self.__q.put_nowait(message)
                        # Remove unread label
                        self.__service.users().messages().modify(userId='me', id=msgId,
                                                                 body=REMOVE_UNREAD).execute()
        except:
            pass

    def sendMessage(self, target, text):
        '''
        Send text message to user
        Return message resource if send successfully. Else return None.
        '''
        if text.strip() == '':
            return

        # Create thet MIMEText
        message = MIMEText(text)
        message['to'] = target
        message['from'] = self.email
        rawMessage ={'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}

        try:
            with LOCK:
                message = (self.__service.users().messages().send(userId='me',
                                                                  body=rawMessage).execute())
            logging.info('Sent "%s" to %s' %(text, target))
            print('Sent "%s" to %s' %(text, target))
            return message
        except:
            logging.warning('Failed to send "%s" to %s' %(text, target))
            print('Failed to send "%s" to %s' %(text, target))
            return None

    def parseMessage(self, message):
        ''' Parse the received message '''
        msg = message['snippet'].lower().strip()
        if len(msg) == 0:
            return
        sender = getSender(message)
        logging.info('Parser received "%s" from %s' %(msg, sender))
        print('Parser received "%s" from %s' %(msg, sender))

        # If the player is new
        if not self.playerManager.havePlayer(sender):
            self.playerManager.addPlayer(sender)
            task = {'name': 'namePlayer', 'value': message}
            self.playerManager.setTask(sender, task)
            self.sendMessage(sender, 'Welcome to openPubg!\nYou are new here. '\
                                     'Please tell us your name')

        else:
            # Get the current task of the sender
            task = self.playerManager.getTask(sender)

            # If there is no other task
            if task is None:
                sMsg = msg.split()
                # If player ask to create a room
                if sMsg[0] == 'create':
                    self.__do_create(sender, sMsg)
                # If player want to start a game
                elif sMsg[0] == 'start':
                    self.__do_start(sender)
                # If player want to join a game
                elif sMsg[0] == 'join':
                    self.__do_join(sender, sMsg)
                # If player wants to quit the game
                elif sMsg[0] == 'quit':
                    self._do_quit(sender)
                # If command unknown
                else:
                    self.sendMessage(sender, 'Command unknown')

            # If task is rename new player
            elif task['name'] == 'namePlayer':
                self.playerManager.setName(sender, msg)
                self.sendMessage(sender, 'Nice to meet you, %s.' %(msg))
                if task['value'] != None:
                    self.__q.put_nowait(task['value'])
            # If task is vote
            elif task['name'] == 'vote':
                self.__do_vote(sender, msg, task)

    def doVote(self, targets, message, options=set(['yes', 'no'])):
        ''' Start a vote '''

        # Create a queue to retrive the answer
        with LOCK:
            index = self.__queueNumber
            self.__queueNumber += 1

        self.__waitQs[index] = Queue()
        ans = {}
        for i in options:
            ans[i] = 0

        # Send messages to each target
        task = {'name': 'vote', 'value': options, 'index': index}
        for t in targets:
            self.sendMessage(t, message)
            # Set the task for each target
            self.playerManager.setTask(t, task)

        # Wait for the answer
        for i in range(len(targets)):
            res = self.__waitQs[index].get()
            ans[res] += 1
        del self.__waitQs[index]

        return ans

    def doQA(self, target, message, options=set(['yes', 'no'])):
        ''' Start a QA '''

        # Create a queue to retrive the answer
        with LOCK:
            index = self.__queueNumber
            self.__queueNumber += 1

        self.__waitQs[index] = Queue()

        # Send messages to each target
        task = {'name': 'vote', 'value': options, 'index': index}
        self.sendMessage(target, message)
        # Set the task for each target
        self.playerManager.setTask(target, task)

        # Wait for the answer
        res = self.__waitQs[index].get()
        del self.__waitQs[index]

        return res

    def close(self):
        ''' Close text manager '''
        self.__running = False
        print('Text Manager Shutdown')

    def __do_create(self, sender, sMsg):
        ''' Handle creating a room '''
        if len(sMsg) < 2:
            self.sendMessage(sender, 'Please resend the commnad with game name')
        roomId = self.roomManager.createRoom(sMsg[1])
        if roomId >= 0:
            self.sendMessage(sender, 'Room %d created! Reply "start" when you '
                                     'are ready' %(roomId))
            res, msg = self.roomManager.addPlayer(sender, roomId)
            if not res:
                self.sendMessage(sender, msg)
        else:
            self.sendMessage(sender, 'Sorry, can\'t find game. Please check your '\
                                     'speeling.')

    def __do_start(self, sender):
        ''' Handle stating a room '''
        roomId = self.playerManager.getRoomId(sender)
        res, msg = self.roomManager.startRoom(roomId)
        if not res:
            self.sendMessage(sender, msg)

    def __do_vote(self, sender, msg, task):
        ''' Handle vote reply '''
        if msg in task['value']:
            self.__waitQs[task['index']].put(msg)
        else:
            self.playerManager.setTask(sender, task)
            self.sendMessage(sender, 'Invalid vote. Please revote')

    def __do_join(self, sender, sMsg):
        ''' Handle joining a room '''
        res, msg = self.roomManager.addPlayer(sender, int(sMsg[1]))
        self.sendMessage(sender, msg)

    def _do_quit(self, sender):
        '''Handle quitting the game'''
        roomId = self.playerManager.getRoomId(sender)
        res, msg = self.roomManager.removePlayer(sender, roomId)
        self.sendMessage(sender, msg)

def getSender(message):
    ''' Get the sender of a message '''
    for i in message['payload']['headers']:
        if i['name'] == 'From':
            return i['value']

# Source: https://developers.google.com/gmail/api/quickstart/python
def get_credentials():
    '''Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    '''
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
        logging.info('Storing credentials to ' + credential_path)
        print('Storing credentials to ' + credential_path)
        print()
    return credentials
