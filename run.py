from mysocket import openSocket, sendMessage
from initialize import joinRoom
from settings import ADMIN, LOL_API
from leaguerank import get_summoner_league
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
        if "!time".lower() in line:
            sendMessage(s,read.get_time()) 
		#Get temperature of given city
        if "!temp".lower() in line:
            sendMessage(s,read.get_temp(msg))
        if "!rank".lower() in line:
            LeagueRank = get_summoner_league(LOL_API)
            sendMessage(s,LeagueRank.getLeagueRank(msg))
