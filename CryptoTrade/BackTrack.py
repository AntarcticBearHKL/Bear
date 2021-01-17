from PyBear.System.Chronus import Date
from PyBear.System.Chronus import Sleep
from PyBear.System import File
import Core as Core
import talib
import numpy
import json

Reload = 0
StartPoint = 0
Offset = 3
Period = 0

def ThinkThink(TimePoint):
    if Core.Data['MACD'][TimePoint-2] * Core.Data['MACD'][TimePoint-1] < 0:
        if Core.Data['MACD'][TimePoint-1] > 0 and Core.Long[-1][0] != 0:
            Core.Long.append([0, Core.Data['TimeStamp'][TimePoint], 
            Core.Data['OpenPrice'][TimePoint]])

        elif Core.Data['MACD'][TimePoint-1] < 0 and Core.Short[-1][0] != 0:
            Core.Short.append([0, Core.Data['TimeStamp'][TimePoint], 
            Core.Data['OpenPrice'][TimePoint]])

    if Core.Data['MACDIN'][TimePoint-2] * Core.Data['MACDIN'][TimePoint-1] < 0:
        if Core.Data['MACDIN'][TimePoint-1] < 0 and Core.Long[-1][0] == 0:
            Profit.append(Data['OpenPrice'][TimePoint] - Long[-1][2])
            Long.append([1, Data['TimeStamp'][TimePoint], Data['OpenPrice'][TimePoint]])
        elif Data['MACDIN'][TimePoint-1] > 0 and Long[-1][0] == 0:
            Profit.append(Data['OpenPrice'][TimePoint] - Short[-1][2])
            Short.append([1, Data['TimeStamp'][TimePoint], Data['OpenPrice'][TimePoint]])  

if Reload:
    Core.Price()
else:
    Core.DataLoad(r'C:\Users\Happy\Desktop\BackTrack.txt')

Core.EMA()
Core.MACD()

for Counter in range(len(Core.Data['TimeStamp'])):
    ItemNum = 0
    for Item in Core.Data:
        ItemNum += 1
        if Core.Data[Item][Counter] == None:
            StartPoint+=1
            break
    if ItemNum == len(Core.Data):
        break

while (StartPoint+Offset+Period)<len(Core.Data['TimeStamp']):
    ThinkThink(StartPoint+Offset+Period)
    Period += 1

'''
for II in Long[-6:]:
    print(II)
'''

print(Core.Profit[-20:])
print(numpy.mean(Profit))
TradeTimes = ((len(Long)-1)/2) + ((len(Short)-1)/2)
print(int(TradeTimes))

'''
St = -50
En = -40
while St<=En:
    print(Data['TimeStamp'][St])
    print(Data['MACDIN'][St])
    St+=1
'''

print(len(Core.Data['TimeStamp']))
input()