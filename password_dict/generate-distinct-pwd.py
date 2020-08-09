import os

def createDistinctPassList():
    passwordList = []
    distinctPwdFile=open('distinct-pwd.txt',  "w", encoding="utf-8")
    for filename in os.listdir('./'):
        print ('Read passwords from', filename)
        dict_file=open(os.path.join('./', filename), 'r', encoding='utf8', errors='ignore')
        for line in dict_file.readlines():
            pwd = line.strip()
            if len(pwd) >=6:
                if pwd in passwordList:
                    pass
                else:
                   passwordList.append(pwd)
                   distinctPwdFile.write(str(pwd))
                   distinctPwdFile.write('\n')

    print ('Collected common passwords:', len(passwordList))
    
createDistinctPassList()