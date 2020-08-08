import threading

class BruteRegisterThreading (threading.Thread):
    def __init__(self, threadID, name, toolkit, targetAccount, beginCode, endCode):
        threading.Thread.__init__(self)
        self.name = name
        self.threadID = threading
        self.name = name
        self.targetAccount = targetAccount
        self.beginCode = beginCode
        self.endCode = endCode
        self.toolkit = toolkit

    def run(self):
        print ("Starting " + self.name)
        print ("Brute register with code:", self.beginCode, self.endCode)
        self.toolkit.bruteRegister(self.targetAccount, self.beginCode, self.endCode)
        print "Exiting " + self.name

