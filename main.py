from eaw_toolkit import EAW_ToolKit
import sys
from os import path


# Main Process
global toolkit 
global configFilename
toolkit = EAW_ToolKit('')
configFilename='config.txt'

def listCommands():
    print ("Usage:  main.py [option] [params...]")
    print (" Option: ")
    print (" -c or --config")
    print (" => parameters: [host]")
    print (" -l or --login")
    print (" => parameters: [acount] [password]")
    print (" -r or --register")
    print (" => parameters: [acount] [password]")
    print (" -ft or --find-target")
    print (" => parameters: none")
    print (" -rr or --register-range")
    print (" => parameters: [begin] [end]")
    print (" -bl or --brute-login")
    print (" => parameters: [account]")
    print (" -br or --brute-register")
    print (" => parameters: [account] [begin-code] [end-code]")


def configHost(host):
    configFile=open(configFilename, 'w')
    configFile.write(host)
    print ('Saving host:' + host)

# Read config host
def readConfig():
    if path.exists(configFilename):
        configFile=open(configFilename, 'r')
        host = configFile.readline()
        if host != '':
            print ('Create toolkit for host:'+ host)
            toolkit.host = host
        else:
            print ('host is not configured:')
            print ("[-c or --config] [host]")
            exit(1)
    else:
        print ('host is not configured:')
        print ("[-c or --config] [host]")
        exit(1)


# Read arguments
if len(sys.argv) <=1 :
    listCommands()
else:
    if sys.argv[1]=='-h' or sys.argv[1]=='--help':
        listCommands()
    elif sys.argv[1]=='-c' or sys.argv[1]=='--config':
        if len(sys.argv) < 3 :
            print ("Missing arguments:")
            print (" [-c or --config] [host] ") 
        else:
            configHost(str(sys.argv[2]))
    elif sys.argv[1]=='-l' or sys.argv[1]=='--login':
        if len(sys.argv) < 4 :
            print ("Missing arguments:")
            print (" [-l or --login] [acount] [password]") 
        else:
            readConfig()
            toolkit._login(str(sys.argv[2]),str(sys.argv[3]))
    elif sys.argv[1]=='-r' or sys.argv[1]=='--register':
        if len(sys.argv) < 4 :
            print ("Missing arguments:")
            print (" [-r or --register] [acount] [password]") 
        else:
            readConfig()
            toolkit._register(str(sys.argv[2]),str(sys.argv[3]))
    elif sys.argv[1]=='-ft' or sys.argv[1]=='--find-target':
        readConfig()
        toolkit.findTargetAccount()
    elif sys.argv[1]=='-rr' or sys.argv[1]=='--register-range':
        if len(sys.argv) < 4 :
            print ("Missing arguments:")
            print (" [-rr or --register-range] [begin] [end]") 
        else:
            readConfig()
            toolkit.registerRange(str(sys.argv[2]),str(sys.argv[3]))
    elif sys.argv[1]=='-bl' or sys.argv[1]=='--brute-login':
        if len(sys.argv) < 3 :
            print ("Missing arguments:")
            print (" [-bl or --brute-login] [acount]") 
        else:
            readConfig()
            toolkit.bruteForceLogin(str(sys.argv[2]))
    elif sys.argv[1]=='-br' or sys.argv[1]=='--brute-register':
        if len(sys.argv) < 5 :
            print ("Missing arguments:")
            print (" [-br or --brute-register] [acount] [begin] [end]") 
        else:
            readConfig()
            toolkit.bruteRegister(str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))
    else:
        print ('Invalid Input')
        listCommands()

