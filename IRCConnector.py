# local imports
import IRCMessage
# module imports
# language imports
import socket

class IRCConnector:

## private
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

## public

    def readIRCMessage(self):
        line = self._readLineAndHeartbeat()[1:]
        return self._messageFactory.parseAndMakeMessage(line)

    def writeIRCMessage(self, messageType, destination, message):        
        self._sendLine("%s %s :%s"%(messageType, destination, message))

    def connectToRizon(self):
        self._socket.connect(("irc.rizon.net",6667))

        self._sendLine('USER radmobile 0 0 :radicool')
        self._sendLine('NICK radmobile 0')
        
        while True:
            response = self._readLineAndHeartbeat()
            message = response.split(":")[0]
            code = response.split(' ')[1]

            if code == '001':
                break
            elif code == '433':
                nick(_nickname + '_')
            else:
                continue

        self._sendLine('PRIVMSG NICKSERV :IDENTIFY radicool')
        self._sendLine('JOIN #/g/spam')

    
# /IRCConnector
