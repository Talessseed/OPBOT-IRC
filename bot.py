import sys 
import socket 
import time
import string
import codecs
HOST = "lucn.fr"
PORT = 6667 
NICK = "GlaDOS"
PASS = "AuTrUcHe"
CHANNEL = "start"
readbuffer = ""

sentencesDict = {"Bonjour GlaDOS": "Hi", "GlaDOS": "Bonjour :)", "Qui est tu GlaDOS ?": "Je suis ton pere",
                 ":P": "::P", "Qui est GlaDOS ?" : "You monster !", "Illuminati" : "confirmed", "Salut GlaDOS": "Bonjour"}
opDict = {"Mwa":'+o',"Talesseed":'+o',"Lagc":'+h'}

def anwser(msg):
    if msg in sentencesDict:
        return sentencesDict[msg]
    
def send(msg, chan = CHANNEL, mode = "PRIVMSG"):
    s.send(bytes("%s #%s %s \r\n" % (mode, chan, msg), "UTF-8"))

#SETUP
while 1:
    user = ''
    message = ''
    
    s=socket.socket( ) 
    s.connect((HOST, PORT))
    s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
    s.send(bytes("NICK "+ NICK +"\r\n", "UTF-8")) 
    s.send(bytes("USER %s %s %s :%s\r\n" %(NICK,NICK,NICK,NICK), "UTF-8"))
    
    while 1:
        readbuffer = readbuffer+s.recv(1024).decode("UTF-8")
        temp = str.split(readbuffer, "\n")
        readbuffer=temp.pop( )
        
        for line in temp:
            line = str.rstrip(line)
            line = str.split(line)
            #print(line)
            if(line[0] == "PING"):
                s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
        
        if line[1]=='MODE':
            break
        
    s.send(bytes("JOIN #%s \r\n" % CHANNEL, "UTF-8"))
    
    fichier = codecs.open("log%s.txt"%(time.time()), "w", encoding='utf-8')
    
    done = False
    
    #MAIN LOOP
    while not done: 
        readbuffer = readbuffer+s.recv(1024).decode("UTF-8") 
        temp = str.split(readbuffer, "\n") 
        readbuffer=temp.pop( )
        
        for line in temp: 
            line = str.rstrip(line) 
            line = str.split(line)
            
            if len(line)>2 and line[2]!=NICK:
                user = str(str(line[0]).split("!")[0])[1:]
                message = (" ".join(line[3:]))
                action = (line[1])
                
                if len(message) > 0 and message[0] == ':':
                    message = message[1:]
                
                if len(line) > 3 and line[3][2:] == "ACTION":
                    msgToPrint = "(%s) %s %s" %(action, user, message[8:])
                elif action == 'NICK':
                    msgToPrint = "%s -> %s" %(user, line[2][1:])
                elif action == 'MODE':
                    pointedUser = line[-1]
                    if pointedUser == line[3]:
                        pointedUser = line[2]
                    msgToPrint = "%s was %s by %s" %(pointedUser, line[3], user)
                elif action == 'JOIN' and user in opDict:
                    send("%s %s"%(opDict[user], user), chan = "start", mode = "MODE")
                    #s.send(bytes("%s #%s %s \r\n" % (mode, chan, msg), "UTF-8"))
                else:
                    msgToPrint = "(%s) <%s> %s" %(action, user, message)
                
                print(msgToPrint)
                
                if message == 'save':
                    fichier.close()
                    send("/quit")
                    done = True
                    break
                elif message == 'say':
                    with codecs.open('data.txt', 'r', encoding='utf-8') as saveFile:
                        for line in saveFile:
                            line = line[:-1]
                            send(line)
                            msg = "(PRIVMSG) <%s> %s" %(NICK, str(line))
                            fichier.write(msg)
                            fichier.write("\n")
                            print(msg)
                else:
                    fichier.write(msgToPrint)
                    fichier.write("\n")
                
            if(line[0] == "PING"): 
                s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
            
            if( len(line)>2 and line[2] == "#%s"% CHANNEL):
                if message in sentencesDict:
                    reponse = anwser(message)
                    send(reponse)
                    msgToPrint = "(PRIVMSG) <%s> %s" %(NICK, reponse)
                    fichier.write(msgToPrint)
                    fichier.write("\n")
                    print(msgToPrint)
                
    fichier.close()
