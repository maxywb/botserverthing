
class IRCMessage:
    def __init__(self,source,code,dest,message):
        self.source = source
        self.code = code
        self.destination = dest
        self.message = message
    def __str__(self):
        return "%s %s %s %s"%(self.source,self.code,self.destination,self.message)

class IRCServerMessage:
    def __init__(self,server,code,other):
        self.server = server
        self.code = code
        self.other = other


class IRCMessageFactory:
    def makeServerMessage(self,messageFields):
        return IRCServerMessage(messageFields[0],messageFields[1],messageFields[2:])


    def makeMessage(self,header,message):
        source = header[0]
        code = header[1]
        dest = header[2]
        return IRCMessage(source,code,dest,message)


    def parseAndMakeMessage(self,rawMessage):

        fields = rawMessage.split(":")
        header = fields[0].split(" ")

        if len(fields) >= 3:
            return self.makeServerMessage(header)
        else:
            return self.makeMessage(header,fields[-1])
        

        
