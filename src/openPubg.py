#!/usr/bin/python3

import argparse
import logging
import os
import sys
import threading

from openPubgShell import openPubgShell
from roomManager import RoomManager
from textManager import TextManager
from playerManager import PlayerManager


parser = argparse.ArgumentParser()
parser.add_argument('thread', type=int, default=5, nargs='?',
                    help='The number of thread to run (default: 5)')

args = parser.parse_args()


def main():

    # Initiate the text manager
    tManager = TextManager(worker=args.thread)
    if not tManager.emailLogin():
        return
    # Initiate the player manager
    pManager = PlayerManager()
    # Initiate the room manager
    rManager = RoomManager(tManager, pManager)
    # Pass the room manager and player manager to text manager
    tManager.setRoomManager(rManager)
    tManager.setPlayerManager(pManager)

    # Initiate shell
    shell = openPubgShell()
    shell.setRoomManager(rManager)
    shell.setTextManager(tManager)

    # Start multithreading
    shellThread = threading.Thread(target=shell.cmdloop)
    textThread = threading.Thread(target=tManager.run)
    textThread.daemon = True

    shellThread.start()
    textThread.start()

    # Block til shell end
    shellThread.join()


if __name__ == '__main__':
    main()
