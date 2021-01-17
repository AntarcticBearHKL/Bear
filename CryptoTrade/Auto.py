from PyBear.System.Chronus import Date
from PyBear.System.Chronus import Sleep
import PyBear.System.System as System
import PyBear.System.Multitask as Multitask
from PyBear.System import File
import Core as Core
import talib
import numpy
import os
import json

Data = {}
TimePoint = Date()
StartTime = Date()
Error = []

Long = [[-1]]
Short = [[-1]]
Profit = []

UpdateCounter = 0

def GetMarketInfo():
    Data['Market'] = Core.Swap.get_specific_ticker('BTC-USDT-SWAP')

def GetWalletInfo():
    Data['Wallet'] = Core.Swap.get_coin_account('BTC-USDT-SWAP')

def GetOrderInfo():
    Data['Order'] = Core.Swap.get_order_list(instrument_id='BTC-USDT-SWAP', state='6')[0]['order_info']

def GetHoldingInfo():
    Data['Holding'] = Core.Swap.get_specific_position('BTC-USDT-SWAP')['holding']


def Update():
    global UpdateCounter
    global Error
    try:
        GetMarketInfo()
        GetOrderInfo()
        GetHoldingInfo()
        Price(3)
        EMA()
        MACD()

        UpdateCounter += 1
        Sleep(1)
    except Exception as e:
        Problem = True
        Error.append(e)

def HomePage():
    global Long
    global Short
    global Profit
    global Error

    System.ClearScreen()

    print('------ 系统时间：', Date().String(2))
    print('------ 已运行时间的：', Date()-StartTime, ' 秒')
    print('------ 已更新: ', UpdateCounter, ' 次')

    print('\n\033[1;32;40m----%s%s%s---- \033[0m'%(' 当前价格：', Data['Market']['last'], ' '))

    EMADict = {
        '现价': float(Data['Market']['last']), 
        '05日线': Data['EMA5'][-1], 
        '10日线': Data['EMA10'][-1], 
        '20日线': Data['EMA20'][-1], 
        '60日线': Data['EMA60'][-1]
        }
    print('EMA 指标：', sorted(EMADict.items(), key = lambda kv:(kv[1], kv[0])))

    print('EMA 五十差：', [Data['EMA510IN'][-3], Data['EMA510IN'][-2], Data['EMA510IN'][-1]])
    print('\n')

    print('DIF: ', Data['DIF'][-5:])
    print('DEA: ', Data['DEA'][-5:])
    print('MACD: ', Data['MACD'][-5:])

    print('看涨交易：', Long[-4:])
    print('看空交易：', Short[-4:])
    print('利润数据：', Profit[-4:])

    TradeTimes = ((len(Long)-1)/2) + ((len(Short)-1)/2)

    if len(Profit) == 0:
        print('平均利润：', 0)
    else:
        print('平均利润：', numpy.mean(Profit))

    print('交易次数：', int(TradeTimes))

    print("错误次数: ", len(Error))

    FileContent = {}
    FileContent['Long'] = Long
    FileContent['Short'] = Short
    FileContent['Profit'] = Profit
    FileContent['TradeTimes'] = TradeTimes
    FileContent['Error'] = [str(Item) for Item in Error]
    File.Write(r'C:\Users\Happy\Desktop\Result.txt', json.dumps(FileContent))

    if len(Data['Order']) != 0:
        print('\033[1;36;40m ---%s--- \033[0m'%('等待成交：'))
        Typelist = [None, "买多：", "买空：", "平多：", "平空："]
        for Order in Data['Order']:
            print(Typelist[int(Order['type'])], Order['size'], ' 单 委托价格：', Order['price'])
        print('\n')

    if len(Data['Holding']) != 0:
        for Order in Data['Holding']:
            Position = Order['avail_position']
            if int(Position) == 0:
                continue
            OpenPrice = Order['avg_cost']
            Profit = float(Order['unrealized_pnl'])
            ProfitP = round(round(float(Order['unrealized_pnl'])/float(Order['margin']),2)*100.00, 2)
            if Order['side'] == 'long':
                print('\033[1;35;40m ---%s--- \033[0m'%('买入开多：'))
                print('持仓量：', Position, '平均持仓价格：', OpenPrice)
                if Profit>0:
                    print('\033[1;31;40m %s%s%s%s%s \033[0m'%('收益：',Profit, ' 收益率：', ProfitP, '%'))
                else:
                    print('\033[1;32;40m %s%s%s%s%s \033[0m'%('收益：',Profit, ' 收益率：', ProfitP, '%'))
                print('\n')
            else:
                print('\033[1;36;40m ---%s--- \033[0m'%('卖出开空：'))
                print('持仓量：', Position, '平均持仓价格：', OpenPrice)
                if Profit>0:
                    print('\033[1;31;40m %s%s%s%s%s \033[0m'%('收益：',Profit, ' 收益率：', ProfitP, '%'))
                else:
                    print('\033[1;32;40m %s%s%s%s%s \033[0m'%('收益：',Profit, ' 收益率：', ProfitP, '%'))
                print('\n')


def ThinkThink():
    global Long
    global Short
    global Profit
    if len(Data['DEA']) == 0:
        return
    if len(Data['DIF']) == 0:
        return

    if Data['DEA'][-2]*Data['DEA'][-3]<0:
        if Data['DEA'][-2]>0 and Long[-1][0] != 0: ##买入看涨点位
            Long.append([0, Date().String(), Data['ClosePrice'][-2]])
        elif Data['DEA'][-2]<0 and Short[-1][0] != 0: ##买入看空点位
            Short.append([0, Date().String(), Data['ClosePrice'][-2]])

    if Data['DIF'][-2]<Data['DIF'][-3]: ##卖出看涨点位
        if Long[-1][0] == 0:
            Profit.append(float(Data['Market']['last']) - float(Long[-1][2]))
            Long.append([1, Date().String(), Data['ClosePrice'][-2]])
    else: ##卖出看空点位
        if Short[-1][0] == 0:
            Profit.append(float(Data['Market']['last']) - float(Short[-1][2]))
            Short.append([1, Date().String(), Data['ClosePrice'][-2]])    


def Price(Period = 3):    
    global Data
    Time = Date()
    
    TimeStamp = []
    OpenPrice = []
    HighPrice = []
    LowPrice = []
    ClosePrice = []

    for i in range(Period):
        print(i)
        End = Time.ISOString()
        Start = Time.Shift(Hour=-2).ISOString()
        Result = Core.Swap.get_kline(instrument_id='BTC-USDT-SWAP',start=Start, end=End, granularity='60')

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

    Data['TimeStamp'] = TimeStamp
    Data['OpenPrice'] = OpenPrice
    Data['HighPrice'] = HighPrice
    Data['LowPrice'] = LowPrice
    Data['ClosePrice'] = ClosePrice

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
        fastperiod=10, 
        slowperiod=20, 
        signalperiod=10)

    Data['DIF'] = []
    Data['DEA'] = []
    Data['MACD'] = []

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
    
System.ClearScreen()
Multitask.SimpleThread(Update, ()).Start()
while(True):  
    try:
        HomePage()
        ThinkThink()
        Multitask.SimpleThread(Update, ()).Start()
        Sleep(1)
    except KeyError as e:
        print("正在加载：", e)
        Sleep(1)
        print('\n')