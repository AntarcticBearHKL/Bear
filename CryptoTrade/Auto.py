from PyBear.System.Chronus import Date
from PyBear.System.Chronus import Sleep
import PyBear.System.System as System
import PyBear.System.Multitask as Multitask
from Core import CoreSystem
from PyBear.System import File
import Core as Core
import talib
import numpy
import os
import json

Core = CoreSystem()

UpdateCounter = 0

def Update():
    global UpdateCounter
    try:
        Core.GetMarketInfo()
        Core.GetOrderInfo()
        Core.GetHoldingInfo()
        Core.PriceLatest(3)
        Core.EMA()
        Core.MACD()

        UpdateCounter += 1
        Sleep(1)
    except Exception as e:
        print(e)
        Core.Error.append(e)

def HomePage():
    global UpdateCounter

    System.ClearScreen()

    print('------ 系统时间：', Date().String(2))
    print('------ 已运行时间的：', Date()-Core.StartTime, ' 秒')
    print('------ 已更新: ', UpdateCounter, ' 次')

    print('\n\033[1;32;40m----%s%s%s---- \033[0m'%(' 当前价格：', Core.Data['Market']['last'], ' '))

    print('DIF: ', Core.Data['DIF'][-5:])
    print('DEA: ', Core.Data['DEA'][-5:])
    print('MACD: ', Core.Data['MACD'][-5:])

    print('\n')

    print('看涨交易：', Core.Long[-4:])
    print('看空交易：', Core.Short[-4:])
    print('利润数据：', Core.Profit[-4:])

    TradeTimes = ((len(Core.Long)-1)/2) + ((len(Core.Short)-1)/2)

    if len(Core.Profit) == 0:
        print('平均利润：', 0)
    else:
        print('平均利润：', numpy.mean(Core.Profit))

    print('交易次数：', int(TradeTimes))

    print("错误次数: ", len(Core.Error))

    print(Core.Data['OpenPrice'][-3:])

    if len(Core.Data['Order']) != 0:
        print('\033[1;36;40m ---%s--- \033[0m'%('等待成交：'))
        Typelist = [None, "买多：", "买空：", "平多：", "平空："]
        for Order in Core.Data['Order']:
            print(Typelist[int(Order['type'])], Order['size'], ' 单 委托价格：', Order['price'])
        print('\n')

    if len(Core.Data['Holding']) != 0:
        for Order in Core.Data['Holding']:
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
    if Core.Data['MACD'][-3] * Core.Data['MACD'][-2] < 0:
        if Core.Data['MACD'][-2] > 0 and Core.Long[-1][0] != 0:
            Core.Long.append([0, Core.Data['TimeStamp'][-1], 
            Core.Data['OpenPrice'][-1]])

        elif Core.Data['MACD'][-2] < 0 and Core.Short[-1][0] != 0:
            Core.Short.append([0, Core.Data['TimeStamp'][-1], 
            Core.Data['OpenPrice'][-1]])

    if Core.Data['MACDIN'][-3] * Core.Data['MACDIN'][-2] < 0:
        if Core.Data['MACDIN'][-2] < 0 and Core.Long[-1][0] == 0:
            Core.Profit.append(Core.Data['OpenPrice'][-1] - Core.Long[-1][2])
            Core.Long.append([1, Core.Data['TimeStamp'][-1], Core.Data['OpenPrice'][-1]])
        elif Core.Data['MACDIN'][-2] > 0 and Core.Short[-1][0] == 0:
            Core.Profit.append(Core.Data['OpenPrice'][-1] - Core.Short[-1][2])
            Core.Short.append([1, Core.Data['TimeStamp'][-1], Core.Data['OpenPrice'][-1]])  

System.ClearScreen()
Multitask.SimpleThread(Update, ()).Start()
while(True):  
    try:
        HomePage()
        ThinkThink()
        Core.ResultSave(r'C:\Users\Happy\Desktop\AutoLog.txt')
        Multitask.SimpleThread(Update, ()).Start()
        Sleep(1)
    except KeyError as e:
        print("正在加载：", e)
        Sleep(1)