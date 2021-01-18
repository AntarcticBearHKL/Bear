from PyBear.System.Chronus import Date
from PyBear.System.Chronus import Sleep
from Core import CoreSystem
import numpy

Core = CoreSystem()

Reload = 1
def GetData():
    if Reload:
        Core.HistoryPrice(3)
        Core.DataSave(r'C:\Users\Happy\Desktop\BackTrack.txt')
    else:
        Core.DataLoad(r'C:\Users\Happy\Desktop\BackTrack.txt')
    Core.MACD()

def HomePage():
    print(Core.Profit[-20:])
    print(numpy.mean(Core.Profit)-36)
    print(numpy.std(Core.Profit, ddof = 1))
    TradeTimes = ((len(Core.Long)-1)/2) + ((len(Core.Short)-1)/2)
    print(int(TradeTimes))

def ShowInfo():
    St = -50
    En = -40
    while St<=En:
        print(Data['TimeStamp'][St])
        print(Data['MACDIN'][St])
        St+=1

def Strategy(TimePoint):
    if Core.Data['MACD'][TimePoint-2] * Core.Data['MACD'][TimePoint-1] < 0:
        if Core.Data['MACD'][TimePoint-1] > 0 and Core.Long[-1][0] != 0:
            Core.Long.append([0, Core.Data['TimeStamp'][TimePoint], 
            Core.Data['OpenPrice'][TimePoint]])
        elif Core.Data['MACD'][TimePoint-1] < 0 and Core.Short[-1][0] != 0:
            Core.Short.append([0, Core.Data['TimeStamp'][TimePoint], 
            Core.Data['OpenPrice'][TimePoint]])

    if Core.Data['MACDIN'][TimePoint-2] * Core.Data['MACDIN'][TimePoint-1] < 0:
        if Core.Data['MACDIN'][TimePoint-1] < 0 and Core.Long[-1][0] == 0:
            Core.Profit.append(Core.Data['OpenPrice'][TimePoint] - Core.Long[-1][2])
            Core.Long.append([1, Core.Data['TimeStamp'][TimePoint], Core.Data['OpenPrice'][TimePoint]])
        elif Core.Data['MACDIN'][TimePoint-1] > 0 and Core.Short[-1][0] == 0:
            Core.Profit.append(Core.Data['OpenPrice'][TimePoint] - Core.Short[-1][2])
            Core.Short.append([1, Core.Data['TimeStamp'][TimePoint], Core.Data['OpenPrice'][TimePoint]])  

GetData()
while Core.StrategyRun(3):
    ThinkThink(Core.CurrentPoint)
HomePage()       
ShowInfo()
input('Press Enter To Continue...')