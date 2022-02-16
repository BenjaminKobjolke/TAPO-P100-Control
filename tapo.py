#!/usr/bin/python

import sys
from PyP100 import PyP100

if len(sys.argv) < 4:
    print('add username, password, ip and on/off as arguments')
    sys.exit(1)

p100 = PyP100.P100(sys.argv[3], sys.argv[1], sys.argv[2]) #Creating a P100 plug object

p100.handshake() #Creates the cookies required for further methods
p100.login() #Sends credentials to the plug and creates AES Key and IV for further methods

# get command line parameter on or off

if sys.argv[4] == "on":
    p100.turnOn()
elif sys.argv[4] == "off":
    p100.turnOff()

