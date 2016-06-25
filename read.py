import string
import pyowm
from time import gmtime, strftime
from mysocket import sendMessage
import datetime

def check_ping(line):
    if "PING" in line:
       line = line.replace("PING","PONG") 
    return line

def get_user(line):
    separate = line.split(":")
    user = separate[1].split("!")[0]
    return user


def get_msg(line):
    return line.split(":")[2]

def get_time():
   now = datetime.datetime.now()     
   #return "The time is: %d:%d in Oslo"%(now.hour,now.minute)  
   return  "The current time is: " + strftime("%H:%M:%S") +" KKona"

def get_temp(line):
    if len(line.split()) <= 1: 
        city = "Oslo"
    else: city = line.split()[1]
    owm = pyowm.OWM("b217f6716e88062baafd714981051139")
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    temp = w.get_temperature("celsius")["temp"]
    return "The average temperature in " + city + " is " + str(temp) + "C"
