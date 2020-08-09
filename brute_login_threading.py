import threading

class BruteLoginThreading(threading.Thread):
    def __init__(self, threadID, name, toolkit, targetAccount, beginIdx, endIdx):
        threading.Thread.__init__(self)
        self.name = name
        self.threadID = threading
        self.name = name
        self.targetAccount = targetAccount
        self.toolkit = toolkit
        self.beginIndex = beginIdx
        self.endIndex = endIdx
    
    def run(self):
        print ("Starting " + self.name)
        print ("Brute login with passwords from indice:", self.beginIndex, self.endIndex)
        self.toolkit.bruteRegister(self.targetAccount, self.beginIndex, self.endIndex)
        print ("Exiting " + self.name)