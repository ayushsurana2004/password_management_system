import random  # used to import random values
import time    # used to import time related values
import os      # used to check path existence
import platform    # used to check platform we are using
import getpass
import pwinput # used to print '*' when password is typed to hide it
import pyperclip as pc     # it provides copying to clipboard and paste it


accLoop = True
asciiNums = []

def createAccount():
    print('Are you sure? Creation of a new account wipes all data of the previous account.')
    time.sleep(2)
    confirm = input('Type out: "New Account" (case-sensitive) in order to create a new account\n')
    if confirm != 'New Account':
        clearConsole()
        return
    else:
        clearConsole()
        if os.path.exists('MasterPass.txt') is True:
          os.remove('MasterPass.txt')
        if os.path.exists('UserPassData.txt') is True:
          os.remove('UserPassData.txt')
        while True:
            newPass = pwinput.pwinput('Input the new Master Password for the new account:\n')
            clearConsole()
            confirm = pwinput.pwinput('Confirm the Master Password by typing the same one again:\n')
            if newPass == confirm:
                mPass = open('MasterPass.txt', 'w')
                mPass.write(encrypt(newPass))
                passDataSetup = open('UserPassData.txt', 'w')
                passDataSetup.write('7b567d27')  # {} 
                print('Success! New account created.')
                time.sleep(2)
                clearConsole()
                break
            else:
                clearConsole()
                print('The passwords do not match up.')
                continue

def encrypt(data):
    asciiList = []
    for i in data:
        asciiList.append(hex(ord(i)).removeprefix('0x'))
        asciiList.append(chr(random.randint(65, 122)))
        asciiList.append(chr(random.randint(65, 122)))
    encryptData = ''.join(asciiList)
    return str(encryptData)
   
def decrypt(data):
    data = list(str(data)) 
    junk = False
    realData = []
    decryptedData = ''
    while len(data) > 0: 
        if junk == False:
            realData.append(data[0])
            realData.append(data[1])
            data.pop(0)
            data.pop(0)
            junk = True
        else:
            data.pop(0) 
            data.pop(0) 
            junk = False
    while len(realData) > 0:
        asciiHex = realData[0] + realData[1] 
        asciiVal = chr(int(asciiHex, 16)) 
        decryptedData = str(f'{decryptedData}{asciiVal}') 
        realData.pop(0) 
        realData.pop(0)
    return str(decryptedData)

def mainMenu():
  while True:
    clearConsole()
    menuSelection = str(input('''What would you like to do?
    [1] Create new entry
    [2] View an entry
    [3] Delete an entry
    [4] Exit
    '''))
    if menuSelection not in {'1', '2', '3', '4'}:
      print('Invalid input')
      time.sleep(1.5)
      continue
    elif menuSelection == '1':
      return 'new'
    elif menuSelection == '2':
      return 'view'
    elif menuSelection == '3':
      return 'del'
    else:
      clearConsole()
      exit()
 
def clearConsole():
  operatingSystem = platform.system()
  if operatingSystem == 'Windows':
    return os.system('cls')
  else:
    return os.system('clear')

def openPassData():
  passDataRead = open('UserPassData.txt', 'r')
  passData = passDataRead.read() 
  passData = decrypt(passData) 
  passDataRead.close() 
  return eval(passData) 

clearConsole()
while True: 
    newAcc = input('Are you a new user?\n[Y] Yes, I am a new user\n[N] No, I am not a new user\n').lower()
    if newAcc not in {'y', 'n'}:
        print('Invalid Input')
        time.sleep(1)
        clearConsole()
        continue
    if newAcc == 'y':
        createAccount()
        continue
    if newAcc == 'n':
        if os.path.exists('MasterPass.txt') == True: 
          break
        else:
          clearConsole()
          print("There is no existing account. Please create a new account to proceed")
          time.sleep(3)
          clearConsole()
          continue

clearConsole()
while True:
  passInput = pwinput.pwinput('Please input the Master Password:\n')
  if passInput == decrypt(open('MasterPass.txt', 'r').read()): 
    clearConsole()
    print('Logging in')
    time.sleep(0.5)
    clearConsole()
    print('Logging in.')
    time.sleep(0.5)
    clearConsole()
    print('Logging in..')
    time.sleep(0.5)
    clearConsole()
    print('Logging in...')
    time.sleep(0.5)
    clearConsole()
    break
  else:
    print('Incorrect password, please try again.')
    time.sleep(1)
    clearConsole()

while True:
  menuSelect = mainMenu() 
  clearConsole()
  if menuSelect == 'new': 
    passDict = openPassData() 
    while True:
      websiteInput = input('What Website is the password for?\n').lower()
      if websiteInput in passDict:
          print(f'The website {websiteInput} already has an input. If you would like to edit it, delete it and create a new one')
          time.sleep(3)
          break
      websiteUsername = input(f'What is the Username for {websiteInput}?\n')
      websitePassword = pwinput.pwinput(f'What is the Password for {websiteInput}?\n')
      newPassDict = {'website' : websiteInput,
                    'username' : websiteUsername,
                    'password' : websitePassword} 
      passDict[websiteInput] = newPassDict
      passDataWrite = open('UserPassData.txt', 'w')
      passDataWrite.write(encrypt(str(passDict)))
      print('Password data saved!')
      time.sleep(2)
      passDataWrite.close()
      break
  if menuSelect == 'view': 
    passDict = openPassData() 
    websiteList = []
    for i in passDict:
       websiteList.append(i)
    while True:
      clearConsole()    
      print('Select one:') 
      num=0
      for website in websiteList: 
        print(f'[{num+1}] {website}')
        num=num+1
      print('[B] Go back')
      menuSelect = input().lower()
      if menuSelect == 'b': 
        break
      try: 
         menuSelect = int(menuSelect)
      except ValueError:
         print('Invalid input')
         continue
      if menuSelect > len(websiteList) or menuSelect < 1: 
        print('Invalid Input')
        continue
      else:
        clearConsole()
        websitePassReq = websiteList[menuSelect-1]
        username = passDict[websitePassReq]['username'] 
        password = passDict[websitePassReq]['password'] 
        pc.copy(password) 
        print(f'Website: {websitePassReq}\nUsername: {username}\nPassword: Copied to clipboard') 
        print('Click enter when you are finished')
        getpass.getpass('') 
        break
  if menuSelect == 'del': 
    passDict = openPassData() 
    websiteList = [] 
    for i in passDict:
       websiteList.append(i) 
    while True:
      print('Select one to delete:') 
      num = 0
      for website in websiteList:  
        print(f'[{num+1}] {website}')
        num = num + 1
      print('[B] Go back')
      menuSelect = input().lower()
      if menuSelect == 'b': 
        goBack = True 
        break
      goBack = False
      try:  
         menuSelect = int(menuSelect)
      except ValueError:
        print('Invalid input')
        time.sleep(1)
        continue
      if menuSelect > len(websiteList) or menuSelect < 1: 
        print('Invalid Input')
        time.sleep(1)
        continue
      else:
        break
    if goBack == False:
      confirm = input('Are you sure you want to delete this? This action can not be undone.\n(Type "Yes" to confirm)\n') 
      if confirm != 'Yes': 
        print('Aborting...')
        time.sleep(2)
      else:
        websitePassDel = websiteList[menuSelect-1] 
        del passDict[websitePassDel] 
        passDataWrite = open('UserPassData.txt', 'w') 
        passDataWrite.write(encrypt(str(passDict))) 
        passDataWrite.close() 
        print('Entry Deleted!')
        time.sleep(2)