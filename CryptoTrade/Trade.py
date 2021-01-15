from PyBear.System.Chronus import Date
from PyBear.System.Chronus import Sleep
import PyBear.System.System as System
import PyBear.System.Multitask as Multitask
import Core as Core
import talib
import numpy

Data = {}
TimePoint = Date()

Put = {}
Short = {}
Profit = 0

def GetMarketInfo():
    Data['Market'] = Core.Swap.get_specific_ticker('BTC-USDT-SWAP')

def GetWalletInfo():
    Data['Wallet'] = Core.Swap.get_coin_account('BTC-USDT-SWAP')

def GetOrderInfo():
    Data['Order'] = Core.Swap.get_order_list(instrument_id='BTC-USDT-SWAP', state='6')[0]['order_info']

def GetHoldingInfo():
    Data['Holding'] = Core.Swap.get_specific_position('BTC-USDT-SWAP')['holding']


def Update():
    while(True):
        GetMarketInfo()
        GetOrderInfo()
        GetHoldingInfo()
        EMA()
        Sleep(1)
UpdateThread = Multitask.SimpleThread(Update, ()).Start()

def HomePage():
    try:
        System.ClearScreen()

        print('------', Date().String(2), '------')

        print('\n\033[1;32;40m ---%s%s--- \033[0m'%('当前价格：', Data['Market']['last']))

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
    if Data['EMA510IN']

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


def EMA():
    Time = Date()
    ClosePrice = []
    for i in range(1):
        End = Time.ISOString()
        Start = Time.Shift(Hour=-2).ISOString()
        Result = Core.Swap.get_kline(instrument_id='BTC-USDT-SWAP',start=Start, end=End, granularity='60')
        Close = [float(price[4]) for price in Result]
        Close.reverse()
        if i!=0:
            Close = Close[:-1]
        ClosePrice = Close + ClosePrice
    ClosePrice = numpy.array(ClosePrice)

    Data['EMA5'] = talib.EMA(ClosePrice, timeperiod=5)
    Data['EMA10'] = talib.EMA(ClosePrice, timeperiod=10)
    Data['EMA20'] = talib.EMA(ClosePrice, timeperiod=20)
    Data['EMA60'] = talib.EMA(ClosePrice, timeperiod=60)
    
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

System.ClearScreen()
while(True):  
    try:
        HomePage()
        ThinkThink()
        Sleep(2)
    except KeyboardInterrupt:
        Handler()

    System.ClearScreen()