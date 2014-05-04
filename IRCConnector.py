import Connection
import IRCMessage

from collections import deque
from Queue import Queue
import socket
import threading
import time

class IRCConnection(Connection.Connection):
## private
    def __init__(self):
        super(IRCConnection,self).__init__()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(1)
        self._messageFactory = IRCMessage.IRCMessageFactory()

    def _readLineAndHeartbeat(self):
        c, s = '', ''
        while c != '\n':
            c = self._socket.recv(1)
            if c == '':
                break
            s += c
        line = s.strip('\r\n')

        if line.split(':')[0] == 'PING ':
            self._sendLine('PONG :%s' % line.split(':')[1])
            return self._readLineAndHeartbeat()

        return line

    def _sendLine(self,message):
        print "sending:",message
        self._socket.send(message + '\r\n')

    def _readIRCMessage(self):
        try:
            line = self._readLineAndHeartbeat()[1:]
        except:
            return None

        messageTime = time.time()
        return self._messageFactory.parseAndMakeMessage(messageTime,line)

    def _writeIRCMessage(self, messageType, destination, message):        
        self._sendLine("%s %s :%s"%(messageType, destination, message))

## public

    def run(self):
        while not self._stop:
            while True:
                message = self._readIRCMessage()
                if message: 
                    with self._incommingMutex:
                        self._incommingMessages.append(message)
                else:
                    break

            with self._outgoingMutex:
                print "outgoing",len(self._outgoingMessages)
                for msg in self._outgoingMessages:
                    self._writeIRCMessage(msg.code,msg.destination,msg.message)
                self._outgoingMessages.clear()
            
    def connectToRizon(self):
        self._socket.connect(("irc.rizon.net",6667))

        self._sendLine('USER radmobile 0 0 :radicool')
        self._sendLine('NICK radmobile 0')
        
        while True:
            try:
                response = self._readLineAndHeartbeat()
            except:
                continue
            message = response.split(":")[0]
            code = response.split(' ')[1]

            if code == '001':
                break
            else:
                continue

        self._sendLine('PRIVMSG NICKSERV :IDENTIFY radicool')
        #self._sendLine('JOIN #/g/spam')

