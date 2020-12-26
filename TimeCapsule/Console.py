import PyBear.Bear as Bear
import PyBear.TimeCapsule.Core as Core
import PyBear.Math.Cipher as Cipher

import os

os.system('cls')

while True:
    Key = input('Input Password: ')
    if Cipher.AESDecrypt('Y2VlZWM1M2MxY2I5MTQxYjczNTJlNTcwZmIxN2E1YWU=', Key) == 'Success':
        break
    print('Password Wrong!')

os.system('cls')

Bear.NewServer('ConsoleServer', Key, 'OWM4MjVjZmMyNWJjMzIwZmRjYjc3NzU2MTMwZjcyZGU=YTczYmZmZThmMjZhNDUzNzZkMTY5NDQ4ZGRiYzhmMzY=OGRiNjYwOThhNzYwZTRmYTdiN2E3ODZkYTJkNWVjNzI=YjA5N2VmZDU3YWJjYzNmYzI3MTIzMDJkZjA0NGE3Yjc=')

while(True):
    Input = input("Input Code: ")
    Result = Core.Cast(Input)
    if type(Result) == str:
        print(Result)
        input('Success. Press Enter To Continue...')
    elif type(Result) == list:
        for Item in Result:
            print(Item)
        input('Success. Press Enter To Continue...')
    elif type(Result) == dict:
        for List in Result:
            print(List, '\n')
            print(Result[List])

        input('Success. Press Enter To Continue...')
    else:
        input('Failed. Press Enter To Continue...')
    os.system('cls')