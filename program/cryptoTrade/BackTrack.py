from PyBear.System.Chronus import Date
from PyBear.System.Chronus import Sleep
from Core import CoreSystem
import numpy

Core = CoreSystem()

Reload = 1
DataPeriod = 10
def GetData():
    if Reload:
        Core.HistoryPrice(DataPeriod)
        Core.DataSave(r'C:\Users\Happy\Desktop\BackTrack.txt')
    else:
        Core.DataLoad(r'C:\Users\Happy\Desktop\BackTrack.txt')
    Core.MACD()

def HomePage():
    print('利润：', Core.Profit[-5:])
    print('平均利润：', numpy.mean(Core.Profit)-36)
    print('波动：', numpy.std(Core.Profit, ddof = 1))
    TradeTimes = ((len(Core.Long)-1)/2) + ((len(Core.Short)-1)/2)
    print('交易次数：', int(TradeTimes))

def ShowInfo():
    St = -50
    En = -40
    while St<=En:
        print(Core.Data['TimeStamp'][St])
        print(Core.Data['MACDIN'][St])
        St+=1

GetData()
while Core.StrategyRun(3):
    Core.Strategy(Core.CurrentPoint)
HomePage()       

input('Press Enter To Continue...')