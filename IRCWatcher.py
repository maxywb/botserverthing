god = "oatzhakok!~meatwad@this.is.the.end"
import Watcher
import Connection
import IRCConnector
import IRCMessage
import time
import sys
import re
import threading

## helpers

def isMessageToMe(message):
    if message.code == "PRIVMSG" and message.source == god:
        return message.destination == "radmobile" or message.message.find("radmobile") == 0

def simpleMessageCallback(connection,destination,message):
    msgTime= time.time()
    source = ""
    code = "PRIVMSG"
    
    message = IRCMessage.IRCMessage(msgTime,source,code,destination,message)

    connection.takeMessages((message))


class IRCWatcher(Watcher.Watcher):
## private
    def __init__(self,con):
        super(IRCWatcher,self).__init__()
        self._connection = con
        self._lastMessageTime = 0

## public
    def run(self):
        while not self._stop:
            messages = self._connection.getMessages(self._lastMessageTime)
            for message in messages:
                if message.time > self._lastMessageTime:
                    self._lastMessageTime = message.time
                self.doCallbacks(message)

    def doCallbacks(self,message):
        if isMessageToMe(message):
            source = "oatzhakok"
            destination = message.destination
            print message
            if destination == "radmobile":
                # the outbound destination is the source of this message
                destination,source = source,destination
            scanner = re.Scanner([
                    (r"radmobile.? go away", lambda scanner,token:\
                         simpleMessageCallback(self._connection,destination,\
                                                   "fuck off")),
                    (r"radmobile.? say .*", lambda scanner,token:\
                         simpleMessageCallback(self._connection,destination,\
                                                   "".join(token.split(\
                                            "say ")[1:])))
                    ])
            scanner.scan(message.message)
