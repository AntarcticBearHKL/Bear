from PyBear.System.Chronus import Date
from PyBear.System.Chronus import Sleep
import PyBear.System.System as System
import PyBear.System.Multitask as Multitask
import Core as Core
import talib
import numpy

Data = {}
TimePoint = Date()
StartTime = Date()

Long = []
Short = []
Profit = [0]

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
    while(True):
        GetMarketInfo()
        GetOrderInfo()
        GetHoldingInfo()
        ClosePrice()
        EMA()
        MACD()
        UpdateCounter += 1
        Sleep(1)
UpdateThread = Multitask.SimpleThread(Update, ()).Start()

def HomePage():
    global Long
    global Short
    global Profit
    try:
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

        print('Long', Long)
        print('Short', Short)
        print('Profit', Profit)

        print('ProfitMean', numpy.mean(Profit))

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

    except Exception as e:
        print("loading....", e)
        print('\n')

def ThinkThink():
    global Long
    global Short
    global Profit

    if Data['DEA'][-2]*Data['DEA'][-3]<0:
        if Data['DEA'][-2]>0: ##买入看涨点位
            Long.append([0, Date().String(), Data['Market']['last']])
        else: ##买入看空点位
            Short.append([0, Date().String(), Data['Market']['last']])

    if len(Long) == 0 or len(Short) == 0:
        return
    if Data['DIF'][-2]<Data['DIF'][-3]<0: ##卖出看涨点位
        if Long[-1][0] == 1:
            Profit.append(float(Data['Market']['last']) - float(Long[-1][2]))
            Long.append([1, Date().String(), Data['Market']['last']])
    else: ##卖出看空点位
        if Short[-1][0] == 1:
            Profit.append(float(Data['Market']['last']) - float(Short[-1][2]))
            Short.append([1, Date().String(), Data['Market']['last']])    

def Handler():
    Command = input('Command: ')
    if Command == '':
        pass
    elif Command[0] == '1':
        Price = input('Price: ')
        if Price == '':
            Price = Data['Market']['last']
        else:
            Price = round(int(Price)/100.00, 2)

        Direction = input('Direction: ')
        Size = input('Size: ')

        input('下单：方向：' + str(Direction) + ' 委托数量：' + str(Size) + ' 委托价格：' + str(Price))
        Open(Direction, Size, Price)
    elif Command[0] == '2':
            Price = input('Price: ')
            if Price == '':
                Price = Data['Market']['last']
            else:
                Price = round(int(Price)/100.00, 2)

            Direction = input('Direction: ')
            Size = input('Size: ')

            input('平仓：方向：' + str(Direction) + ' 委托数量：' + str(Size) + ' 委托价格：' + str(Price))
            Open(int(Direction)+2, Size, Price)
            

def Open(Direction, Size, Price, ID='DefaultOrder'):
    Core.Swap.take_order(instrument_id='BTC-USDT-SWAP', 
        type=Direction, price=Price, 
        size=Size, client_oid=ID)

def Liquidate(Direction, Size, Price):
    Core.Swap.take_order(instrument_id='BTC-USDT-SWAP', 
        type=Direction, price=Price, 
        size=Size, client_oid=ID)

def CancelOrder():
    pass

def ClosePrice(Period = 3):
    Time = Date()
    ClosePrice = []
    for i in range(Period):
        End = Time.ISOString()
        Start = Time.Shift(Hour=-2).ISOString()
        Result = Core.Swap.get_kline(instrument_id='BTC-USDT-SWAP',start=Start, end=End, granularity='60')
        Close = [float(price[4]) for price in Result]
        Close.reverse()
        if i!=0:
            Close = Close[:-1]
        ClosePrice = Close + ClosePrice
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
        fastperiod=2, 
        slowperiod=10, 
        signalperiod=2)

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
Sleep(3)
while(True):  
    HomePage()
    ThinkThink()
    Sleep(1)
    continue
    try:
        HomePage()
        ThinkThink()
        Sleep(1)
    except Exception as e:
        print('Loading...', e)
        Sleep(1)

    System.ClearScreen()