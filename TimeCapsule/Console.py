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

print('Login Success...')
input("Press Enter To Continue ...")
os.system('cls')

Bear.NewServer('ConsoleServer', Key, 'OWM4MjVjZmMyNWJjMzIwZmRjYjc3NzU2MTMwZjcyZGU=YTczYmZmZThmMjZhNDUzNzZkMTY5NDQ4ZGRiYzhmMzY=OGRiNjYwOThhNzYwZTRmYTdiN2E3ODZkYTJkNWVjNzI=YjA5N2VmZDU3YWJjYzNmYzI3MTIzMDJkZjA0NGE3Yjc=')

def AdditionHandler(Explain):
    return input(Explain+': ')
Core.SetAdditionHandler(AdditionHandler)

while(True):
    Input = input("Code: ")
    if Bear.CatchResult(Core.Cast(Input)):
        input('Success. Press Enter To Continue...')
    else:
        input('Failed. Press Enter To Continue...')
    os.system('cls')