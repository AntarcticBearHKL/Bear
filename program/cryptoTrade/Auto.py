# -*- coding: utf-8 -*-  

from PyBear.System.Chronus import Date
from PyBear.System.Chronus import Sleep
import PyBear.System.System as System
import PyBear.System.Multitask as Multitask
from Core import CoreSystem
from PyBear.System import File
import talib
import numpy
import os
import json

core = CoreSystem()

updateCounter = 0

def update():
    global updateCounter
    try:
        core.getMarketInfo()
        core.getOrderInfo()
        core.getHoldingInfo()
        core.minutePrice(5)
        core.MACD()

        updateCounter += 1
        Sleep(1)
    except Exception as e:
        print(e)
        core.error.append(e)

def headPanel():
    print('------ System Clock: ', Date().String(2))
    print('------ Uptime: ', Date()-core.startTime, ' seconds')
    print('------ Update Timeis: ', updateCounter, ' times')
    print("------ Error: ", len(core.error), ' times')

def latestPrice():
    print('\n\033[1;32;40m----%s%s%s---- \033[0m'%(' Current Price: ', core.marketPrice, ' '))


def orderInfo():
    if len(core.data['Order']) != 0:
        print('\033[1;36;40m ---%s--- \033[0m'%('Waiting Order: '))
        Typelist = [None, "Open Long: ", "Open Short: ", "Liquidate Long: ", "Liquidate Short: "]
        for Order in core.data['Order']:
            print(Typelist[int(Order['type'])], Order['size'], ' Price: ', Order['price'])
        print('\n')
   

def holdingInfo():
    if len(core.data['Holding']) != 0:
        for Order in core.data['Holding']:
            Position = Order['avail_position']
            if int(Position) == 0:
                continue
            OpenPrice = Order['avg_cost']
            Profit = round(float(Order['unrealized_pnl'])-0.38, 2)
            ProfitP = round(round(Profit/float(Order['margin']),2)*100.00, 2)
            if Order['side'] == 'long':
                print('\033[1;35;40m---- %s ---- \033[0m'%('Long: '))
                print('Holding: ', Position, 'Average Price: ', OpenPrice)
                if Profit>0:
                    print('\033[1;31;40m %s%s%s%s%s \033[0m'%('Profit: ',Profit, ' Rate of Return: ', ProfitP, '%'))
                else:
                    print('\033[1;32;40m %s%s%s%s%s \033[0m'%('Profit: ',Profit, '  Rate of Return: ', ProfitP, '%'))
                print('\n')
            else:
                print('\033[1;36;40m---- %s ---- \033[0m'%('Short: '))
                print('Holding: ', Position, 'Average Price', OpenPrice)
                if Profit>0:
                    print('\033[1;31;40m %s%s%s%s%s \033[0m'%('Profit: ',Profit, '  Rate of Return: ', ProfitP, '%'))
                else:
                    print('\033[1;32;40m %s%s%s%s%s \033[0m'%('Profit: ',Profit, '  Rate of Return: ', ProfitP, '%'))
                print('\n')
   
def debug():
    print('MACDII', core.data['MACDIntervalInverse'][-5:])


def homePage():
    System.ClearScreen()
    headPanel()
    latestPrice()
    debug()
    orderInfo()
    holdingInfo()

System.ClearScreen()
Multitask.SimpleThread(update, ()).Start()
while(True):  
    try:
        homePage()
        core.strategyMACD(-1)
        Multitask.SimpleThread(update, ()).Start()
        core.resultLog('/log/resultLog-'+core.startTime.String(2))
        core.errorLog('/log/errorLog-'+core.startTime.String(2))
        Sleep(3)
    except KeyError as e:
        print("正在加载：", e)
        Sleep(1)
    except:
        print("FATAL ERROR HAPPEND")
        core.cancelAll()
        core.liquidateAll()
