from PyBear.System.Chronus import Date
from PyBear.System.Chronus import Sleep
from PyBear.System import File
import Core as Core
import talib
import numpy
import json

Data = {}
Reload = 0
StartPoint = 0
Offset = 3
Period = 0

Long = [[-1]]
Short = [[-1]]
Profit = []

def Price():
    global Data

    Time = Date()
    
    TimeStamp = []
    OpenPrice = []
    HighPrice = []
    LowPrice = []
    ClosePrice = []

    for i in range(10):
        print(i)
        End = Time.ISOString()
        Start = Time.Shift(Day=-10).ISOString()
        Result = Core.Swap.get_history_kline(instrument_id='BTC-USDT-SWAP',start=End, end=Start, granularity='3600')

        TS = [price[0] for price in Result]
        TS.reverse()
        Open = [float(price[1]) for price in Result]
        Open.reverse()
        High = [float(price[2]) for price in Result]
        High.reverse()
        Low = [float(price[3]) for price in Result]
        Low.reverse()
        Close = [float(price[4]) for price in Result]
        Close.reverse()

        if i!=0:
            TS = TS[:-1]
            Open = Open[:-1]
            High = High[:-1]
            Low = Low[:-1]
            Close = Close[:-1]

        TimeStamp = TS + TimeStamp
        OpenPrice = Open + OpenPrice
        HighPrice = High + HighPrice
        LowPrice = Low + LowPrice
        ClosePrice = Close + ClosePrice

        Sleep(0.5)

    Data['TimeStamp'] = TimeStamp
    Data['OpenPrice'] = OpenPrice
    Data['HighPrice'] = HighPrice
    Data['LowPrice'] = LowPrice
    Data['ClosePrice'] = ClosePrice

    File.Write(r'C:\Users\Happy\Desktop\BackTrack.txt', json.dumps(Data))

def EMA():
    Data['EMA5'] = talib.EMA(numpy.array(Data['ClosePrice']), timeperiod=5)
    Data['EMA10'] = talib.EMA(numpy.array(Data['ClosePrice']), timeperiod=10)
    Data['EMA20'] = talib.EMA(numpy.array(Data['ClosePrice']), timeperiod=20)
    Data['EMA60'] = talib.EMA(numpy.array(Data['ClosePrice']), timeperiod=60)
    
    for Item in ['EMA5','EMA10','EMA20','EMA60']:
        TempList = []
        for EMA in Data[Item]:
            if numpy.isnan(EMA):
                TempList.append(None)
            else:
                TempList.append(float(round(EMA, 2)))
        Data[Item] = TempList
    
    Data['EMA510IN'] = []
    for Counter in range(len(Data['EMA5'])):
        if Data['EMA5'][Counter] and Data['EMA10'][Counter]:
            Data['EMA510IN'].append(round(Data['EMA5'][Counter]-Data['EMA10'][Counter], 2))
        else:
            Data['EMA510IN'].append(None)

def MACD():
    DIF, DEA, NOIR = talib.MACD(
        numpy.array(Data['ClosePrice']),
        fastperiod=8, 
        slowperiod=16, 
        signalperiod=10)

    Data['DIF'] = []
    Data['DEA'] = []
    Data['MACD'] = []
    Data['MACDIN'] = []

    for Item in DIF:
        if numpy.isnan(Item):
            Data['DIF'].append(None)
        else:
            Data['DIF'].append(round(Item,2))

    for Item in DEA:
        if numpy.isnan(Item):
            Data['DEA'].append(None)
        else:
            Data['DEA'].append(round(Item,2))

    for Item in list(DIF - DEA):
        if numpy.isnan(Item):
            Data['MACD'].append(None)
        else:
            Data['MACD'].append(round(Item*2,2))

    for Counter in range(len(Data['MACD'])):
        if Counter == 0:
            Data['MACDIN'].append(None)
        elif Data['MACD'][Counter-1] == None:
            Data['MACDIN'].append(None)
        else:
            Data['MACDIN'].append(round(Data['MACD'][Counter]-Data['MACD'][Counter-1],2))


def ThinkThink(TimePoint):
    global Long
    global Short
    global Profit

    if Data['MACD'][TimePoint-2] * Data['MACD'][TimePoint-1] < 0:
        if Data['MACD'][TimePoint-1] > 0 and Long[-1][0] != 0:
            Long.append([0, Data['TimeStamp'][TimePoint], 
            Data['OpenPrice'][TimePoint]])

        elif Data['MACD'][TimePoint-1] < 0 and Short[-1][0] != 0:
            Short.append([0, Data['TimeStamp'][TimePoint], 
            Data['OpenPrice'][TimePoint]])

    if Data['MACDIN'][TimePoint-2] * Data['MACDIN'][TimePoint-1] < 0:
        if Data['MACDIN'][TimePoint-1] < 0 and Long[-1][0] == 0:
            Profit.append(Data['OpenPrice'][TimePoint] - Long[-1][2])
            Long.append([1, Data['TimeStamp'][TimePoint], Data['OpenPrice'][TimePoint]])
        elif Data['MACDIN'][TimePoint-1] > 0 and Long[-1][0] == 0:
            Profit.append(Data['OpenPrice'][TimePoint] - Short[-1][2])
            Short.append([1, Data['TimeStamp'][TimePoint], Data['OpenPrice'][TimePoint]])  

if Reload:
    Price()
else:
    Data = json.loads(File.Read(r'C:\Users\Happy\Desktop\BackTrack.txt'))

EMA()
MACD()

for Counter in range(len(Data['TimeStamp'])):
    ItemNum = 0
    for Item in Data:
        ItemNum += 1
        if Data[Item][Counter] == None:
            StartPoint+=1
            break
    if ItemNum == len(Data):
        break

while (StartPoint+Offset+Period)<len(Data['TimeStamp']):
    ThinkThink(StartPoint+Offset+Period)
    Period += 1

for II in Long[-6:]:
    print(II)

print(Profit[-20:])
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

print(len(Data['TimeStamp']))
input()