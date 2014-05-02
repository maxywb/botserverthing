import Connection
import IRCConnector
import IRCMessage
import MessageWatcher

import time
import sys
import re
import threading
import signal

def killSignal(signal,frame):
    for thread in threads:
        print type(thread)
        thread.join()
    sys.exit(0)

if __name__ == "__main__":
    threads = []
    signal.signal(signal.SIGINT,killSignal)

    print "start connection"
    con = IRCConnector.IRCConnection()
    con.connectToRizon()
    con.start()
    threads.append(con)
    
    print "start watcher"
    bot = MessageWatcher.MessageWatcher(con)
    bot.start()
    threads.append(bot)
    
    signal.pause()
