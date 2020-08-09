import threading
import os

class RegisterRangeThreading(threading.Thread):
    def __init__(self, threadID, name, toolkit, beginAccount, endAccount):
        threading.Thread.__init__(self)
        self.name = name
        self.threadID = threading
        self.name = name
        self.toolkit = toolkit
        self.begin = beginAccount
        self.end = endAccount
    
    def run(self):
        print ("Starting " + self.name)
        print ("Register acount range between:", self.begin, self.end)
        self.toolkit.registerRange(self.begin, self.end)
        print ("Exiting " + self.name)