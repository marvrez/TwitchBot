from mysocket import openSocket, sendMessage
import string

def joinRoom(s):
    readbuffer = ""
    loading = True

    while loading:
        readbuffer = readbuffer + s.recv(1024).decode()
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()

        for line in temp:
            print(line)
            loading =  loadingComplete(line)
    sendMessage(s,"Successfully joined the chat!")

def loadingComplete(line):
    if("End of /NAMES list" in line):
        return False
    else:
        return True
