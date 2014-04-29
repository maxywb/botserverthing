
import IRCConnector
import time
import sys
import re


def testIRCBot():
    con = IRCConnector.IRCConnector()
    con.connectToRizon()
    god = "oatzhakok!~meatwad@this.is.the.end"
    while True:
        message = con.readIRCMessage()
        if message.code == "PRIVMSG" :
            if message.source == god:
                if message.destination == "radmobile":
                    # private chat
                    print "pm"
                    con.writeIRCMessage("PRIVMSG","oatzhakok","hi oatzy!")
                else:
                    scanner = re.Scanner([
                            (r"radmobile: go away.*", lambda scanner,token:con.writeIRCMessage("PRIVMSG",message.destination,"fuck off"))
                            ])
                    results,remainder = scanner.scan(message.message)
                    

                    




def goAway(scanner, token,other): 
    print "goAway:",token

def testCallback():
    other= 12
    scanner = re.Scanner([
            (r"go away.*", lambda scanner,token:"%d"%other)
            ])
    results,remainder = scanner.scan("go away to hell")
    
    print results[0]
    print remainder



if __name__ == "__main__":
    testIRCBot()
