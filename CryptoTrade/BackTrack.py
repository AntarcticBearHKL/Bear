from PyBear.System.Chronus import Date
from PyBear.System.Chronus import Sleep
from Core import CoreSystem
import numpy
Reload = 1
StartPoint = 0
Offset = 3
Period = 0

Core = CoreSystem()

if Reload:
    Core.HistoryPrice(3)
    Core.DataSave(r'C:\Users\Happy\Desktop\BackTrack.txt')
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
print(numpy.mean(Core.Profit)-36)
print(numpy.std(Core.Profit, ddof = 1))
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