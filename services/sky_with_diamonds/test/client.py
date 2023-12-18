from service import *
import sys
import os
import subprocess
from pwnlib.util.packing import *

host = 'localhost'
port = '3335'
ok = "ACK_OK"

s = getSocket(host, port)

#registration
def reg():
    os.system('clear')
    data = recvMessage(s)#receive username
    print data
    input  = raw_input('')
    sendMessage(s,input) #send username
    data = recvMessage(s) #receive pwd
    print data
    input  = raw_input('')
    sendMessage(s,input) #send pwd
    data = recvMessage(s) #receive status
    if (data!=ok): #error
        print data
        return -1
    else:
        os.system('clear')
        data = recvMessage(s) #receive confirm
        print data
        return 0

#login
def login():
    os.system('clear')
    data = recvMessage(s) # receive username
    print data
    input = raw_input('')
    sendMessage(s,input) #send username
    data = recvMessage(s) #receive pwd
    print data
    input = raw_input('')
    sendMessage(s,input) #send pwd
    data = recvMessage(s) # receive status
    if (data!=ok):
        print data
        return -1
    else:
        os.system('clear')
        data = recvMessage(s) #receive confirm
        print data
        return 0

#help
def help():
    os.system('clear')
    data = recvMessage(s) # receive what help you want?
    print data
    return 0

#exit
def exit():
    os.system('clear')
    data = recvMessage(s) #receive menu exit
    print data
    return -1
    
#insert_DIAMOND
def insert_diamond():
    os.system('clear')
    data = recvMessage(s) #receive login status
    if (data != ok):
        print data
        return -1
    else:
        data = recvMessage(s) #receive insert size
        print data
        input  = raw_input('')
        sendMessage(s,input) #send size
        data = recvMessage(s) #receive insert size
        print data
        input  = raw_input('')
        sendMessage(s,input) #send size
        data = recvMessage(s) #receive insert name
        print data
        input  = raw_input('')
        sendMessage(s,input) #send name
        data = recvMessage(s) #receive status
        if (data != ok):
            print data
            return -1
        else:
            os.system('clear')
            data = recvMessage(s) #receive confirm
            print data
            return 0

#view DIAMOND
def view_diamond():
    os.system('clear')
    data = recvMessage(s) #receive login status
    if (data != ok):
        print data
        return -1
    else:
        os.system('clear')
        data = recvMessage(s) #receive list DIAMOND
        print "Price  :  Size  :  Description"
        print "--------------------------------------"
        print data
        #print 'asd'
        return 0

while (True):
    #os.system('clear')
    data = recvMessage(s)#receive menu
    print data
    input  = raw_input('')
    sendMessage(s,input)#send command
    data = recvMessage(s)#receive status

    if (data!=ok):#error
        print data
        break
    else:    
        if (input == 'R' or input =='r'):
            #registration
            if reg():
                break
        elif (input == 'L' or input =='l'):
            #login
            if login():
                break
        elif (input == 'H' or input =='h'):
            #help
            if help():
                break
        elif (input == 'E' or input =='e'):
            #FIX ME
            #exit
            if exit():
                break
        elif (input == 'A' or input =='a'):
            #insert DIAMOND
            if insert_diamond():
                break
        elif (input == 'G' or input =='g'):
            #view DIAMOND
            if view_diamond():
                break
print "close"
closeSocket(s)




