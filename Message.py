
class Message:
    def __init__(self,time,source,code,dest,message):
        self.time = time
        self.source = source
        self.code = code
        self.destination = dest
        self.message = message
    def __str__(self):
        return "%s %s %s %s"%(self.source,self.code,self.destination,self.message)

class IRCMessageFactory:

    def parseAndMakeMessage(self,time,rawMessage):

        fields = rawMessage.split(":")

        header = fields[0].split(" ")
        source = header[0]
        code = header[1]
        dest = header[2]
        message = fields[1:]
        return Message(time,source,code,dest,":".join(message))
