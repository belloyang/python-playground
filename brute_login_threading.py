import threading
import os

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
        targetPwd = self.toolkit.bruteForceLogin(self.targetAccount, self.beginIndex, self.endIndex)
        if targetPwd != "":
            print ("Password found, exit application", targetPwd)
            os._exit(0)
        else:
            print ("Password not found between indice", self.beginIndex, self.endIndex)
        print ("Exiting " + self.name)