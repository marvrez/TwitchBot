from mysocket import openSocket, sendMessage
from initialize import joinRoom
from settings import ADMIN
import read
s = openSocket()
joinRoom(s)

readbuffer = ""
while True:
    readbuffer = readbuffer + s.recv(1024).decode()
    temp = readbuffer.split("\n")
    readbuffer = temp.pop()

    for line in temp:
        print(line)
        if "PING" in line:
            s.send(line.replace("PING","PONG").encode())
            continue
        user,msg  = read.get_user(line), read.get_msg(line)
        print (user + ": " + msg)

############### COMMANDS ############################ 

		#Get local time
        if "!time" in line:
           sendMessage(s,read.get_time()) 
		#Get temperature of given city
        if "!temp" in line:
           sendMessage(s,read.get_temp(msg))
        if "!end" in line and user == ADMIN:
            test = True #steng bot dersom !end brukes
