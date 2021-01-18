from PyBear.System.Chronus import Date
from PyBear.System.Chronus import Sleep
from Core import CoreSystem
import numpy
Reload = 1
StartPoint = 0
Offset = 3
Period = 0

Core = CoreSystem()

def ThinkThink(TimePoint):
    if Core.D['MACD'][TimePoint-2] * Core.D['MACD'][TimePoint-1] < 0:
        if Core.D['MACD'][TimePoint-1] > 0 and Core.Long[-1][0] != 0:
            Core.Long.append([0, Core.D['TimeStamp'][TimePoint], 
            Core.D['OpenPrice'][TimePoint]])

        elif Core.D['MACD'][TimePoint-1] < 0 and Core.Short[-1][0] != 0:
            Core.Short.append([0, Core.D['TimeStamp'][TimePoint], 
            Core.D['OpenPrice'][TimePoint]])

    if Core.D['MACDIN'][TimePoint-2] * Core.D['MACDIN'][TimePoint-1] < 0:
        if Core.D['MACDIN'][TimePoint-1] < 0 and Core.Long[-1][0] == 0:
            Core.Profit.append(Core.D['OpenPrice'][TimePoint] - Core.Long[-1][2])
            Core.Long.append([1, Core.D['TimeStamp'][TimePoint], Core.D['OpenPrice'][TimePoint]])
        elif Core.D['MACDIN'][TimePoint-1] > 0 and Core.Long[-1][0] == 0:
            Core.Profit.append(Core.D['OpenPrice'][TimePoint] - Core.Short[-1][2])
            Core.Short.append([1, Core.D['TimeStamp'][TimePoint], Core.D['OpenPrice'][TimePoint]])  

if Reload:
    Core.HistoryPrice(1)
    Core.DataSave(r'C:\Users\Happy\Desktop\BackTrack.txt')
else:
    Core.DataLoad(r'C:\Users\Happy\Desktop\BackTrack.txt')

Core.EMA()
Core.MACD()

for Counter in range(len(Core.D['TimeStamp'])):
    ItemNum = 0
    for Item in Core.D:
        ItemNum += 1
        if Core.D[Item][Counter] == None:
            StartPoint+=1
            break
    if ItemNum == len(Core.D):
        break

while (StartPoint+Offset+Period)<len(Core.D['TimeStamp']):
    ThinkThink(StartPoint+Offset+Period)
    Period += 1

'''
for II in Long[-6:]:
    print(II)
'''

print(Core.Profit[-20:])
print(numpy.mean(Core.Profit))
TradeTimes = ((len(Core.Long)-1)/2) + ((len(Core.Short)-1)/2)
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