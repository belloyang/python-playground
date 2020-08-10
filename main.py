from eaw_toolkit import EAW_ToolKit
import sys
from os import path
import enum
from brute_register_threading import BruteRegisterThreading
from brute_login_threading import BruteLoginThreading
from register_range_threading import RegisterRangeThreading


if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

global BruteRegister
global BruteLogin
global RegisterRange
BruteRegister = 'BruteRegister'
BruteLogin = 'BruteLogin'
RegisterRange = 'RegisterRange'

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
    print (" -t or --thread")
    print ("=> parameters: [TaskName] [num of threads] [account] [begin] [end]")
    print ("      [Taskname]: BruteRegister, BruteLogin ([begin] [end] can be ommited) or RegisterRange")


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
            toolkit.readOrCreatePassList()
            toolkit.bruteForceLogin(str(sys.argv[2]))
    elif sys.argv[1]=='-br' or sys.argv[1]=='--brute-register':
        if len(sys.argv) < 5 :
            print ("Missing arguments:")
            print (" [-br or --brute-register] [acount] [begin] [end]") 
        else:
            readConfig()
            toolkit.bruteRegister(str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))
    elif sys.argv[1]=='-t' or sys.argv[1]=='--thread':
        if len(sys.argv) < 3 :
            print ("Missing arguments:")
            print (" [-t or --thread] [TaskName] [num of threads] [account] [begin] [end]")
            print ("      [Taskname]: BruteRegister, BruteLogin ([begin] [end] can be ommited) or RegisterRange") 
        else:
            task = str(sys.argv[2])
            if (task == BruteRegister) and len(sys.argv) < 7:
                print ("Missing arguments:")
                print (" [-t or --thread] [BruteRegister] [num of threads] [account] [begin] [end]")
                exit(1)
            elif (task == RegisterRange) and len(sys.argv) < 6:
                print ("Missing arguments:")
                print (" [-t or --thread] [RegisterRange] [num of threads] [begin] [end]")
                exit(1)
            elif task == BruteLogin and len(sys.argv) < 5:
                print ("Missing arguments:")
                print (" [-t or --thread] [BruteLogin] [num of threads] [account]")
                exit(1)
            else:
                readConfig()
                nThread = int(sys.argv[3])
                if task == RegisterRange:
                    beginAccount = int(sys.argv[4])
                    endAccount = int(sys.argv[5])
                else:
                    account= str(sys.argv[4])
                    if task == BruteRegister:
                        beginCode = int(sys.argv[5])
                        endCode = int(sys.argv[6])
            
            if task == BruteRegister:
                workload = int((endCode - beginCode) / nThread)
                begin = beginCode
                end = min(begin + workload, endCode)
                idx = 0
                while begin < endCode:
                    BruteRegisterThreading(idx, 'thread'+str(idx), toolkit, account, begin, end).start()
                    begin = end
                    end = min(begin + workload, endCode)
                    idx +=1
            elif task == BruteLogin:
                toolkit.readOrCreatePassList()
                numOfPwd = len(toolkit.passwordList)
                workload = int(numOfPwd / nThread)
                begin = 0
                end = begin + workload
                idx=0
                while begin < numOfPwd:
                    BruteLoginThreading(idx, 'thread' + str(idx), toolkit, account, begin, end).start()
                    begin = end
                    end = min(begin + workload, numOfPwd)
                    idx +=1
                
            elif task == RegisterRange:
                workload = int((endAccount - beginAccount)/nThread)
                begin = beginAccount
                end = beginAccount + workload
                idx=0
                while begin < endAccount:
                    RegisterRangeThreading(idx, 'thread' + str(idx), toolkit, begin, end).start()
                    begin = end
                    end = min(begin + workload, endAccount)
                    idx +=1
            else:
                print ('Incorrect TaskName: BruteRegister, BruteLogin or RegisterRange')


    else:
        print ('Invalid Input')
        listCommands()

