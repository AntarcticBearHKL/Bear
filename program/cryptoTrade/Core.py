import okex.account_api as account
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import okex.index_api as index
import okex.option_api as option
import okex.system_api as system
import okex.information_api as information
from PyBear.System.Chronus import Date
from PyBear.System.Chronus import Sleep
from PyBear.System import File
from PyBear.Math import Cipher
import datetime
import talib
import numpy
import json


class CoreSystem:
    def __init__(self):
        self.startTime = Date()
        self.Initialized = False

        self.data = {}
        self.marketPrice = None

        self.longOrder = None
        self.shortOrder = None
        self.orderList = []
        self.error = {}

        api_key = "f735b07f-e18d-4ca3-8b8a-beaa61ad16c1"
        secret_key = "F042A3D395A940DEBA703A522B29DF78"
        passphrase = "T1r2a3deCode"

        self.account = account.AccountAPI(api_key, secret_key, passphrase, False)

        self.index = index.IndexAPI(api_key, secret_key, passphrase, False)

        self.information = information.InformationAPI(api_key, secret_key, passphrase, False)

        self.swap = swap.SwapAPI(api_key, secret_key, passphrase, False)


    def dataSave(self, Path):
        File.Write(Path, json.dumps(self.data))

    def dataLoad(self, Path):
        self.data = json.loads(File.Read(Path))

    def resultLog(self, Path):
        File.Write(Path, json.dumps(self.orderList))
        
    def errorLog(self, Path):
        File.Write(Path, json.dumps(self.error))


    def judge(self, judgeItem):
        if judgeItem.count(False) == 0:
                return True
        return False


    def getMarketInfo(self):
        self.data['Market'] = self.swap.get_specific_ticker('BTC-USDT-SWAP')
        self.marketPrice = self.data['Market']['last']

    def getWalletInfo(self):
        self.data['Wallet'] = self.swap.get_coin_account('BTC-USDT-SWAP')

    def getOrderInfo(self):
        self.data['Order'] = self.swap.get_order_list(instrument_id='BTC-USDT-SWAP', state='6')[0]['order_info']

    def getOrderInfoById(self, clientOid):
        return self.swap.get_order_info(instrument_id='BTC-USDT-SWAP', client_oid=clientOid)
    def getHoldingInfo(self):
        self.data['Holding'] = self.swap.get_specific_position('BTC-USDT-SWAP')['holding']



    def placeOrder(self, direction, size, price):
        clientOid = 'Order' + Cipher.NumberIndex()        
        self.swap.take_order(instrument_id='BTC-USDT-SWAP', 
            type=direction, price=price,   
            size=size, client_oid=clientOid)
        return clientOid

    def placeOrderMatchPrice(self, direction, size):
        clientOid = 'Order' + Cipher.NumberIndex()        
        self.swap.take_order(instrument_id='BTC-USDT-SWAP', 
        type=direction, order_type=4, price=None, 
        size=size, client_oid=clientOid)
        return clientOid

    def cancelOrder(self, clientOid=None):
        self.swap.revoke_order(instrument_id='BTC-USDT-SWAP', client_oid=clientOid)

    def cancelAll(self):
        for order in self.data['Order']:
            self.swap.revoke_order(instrument_id='BTC-USDT-SWAP', order_id=order['order_id'])
   

    def liquidateAll(self):
        if self.longOrder:
            size = self.getOrderInfoById(self.longOrder[0])['size']
            self.placeOrderMatchPrice(3, size)

        if self.shortOrder:
            size = self.getOrderInfoById(self.shortOrder[0])['size']
            self.placeOrderMatchPrice(4, size)




    def minutePrice(self, sampling): 
        Time = Date()
        
        TimeStamp = []
        OpenPrice = []
        HighPrice = []
        LowPrice = []
        ClosePrice = []

        for i in range(sampling):
            End = Time.ISOString()
            Start = Time.Shift(Hour=-2).ISOString()
            Result = self.swap.get_kline(instrument_id='BTC-USDT-SWAP',start=Start, end=End, granularity='60')

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

        self.data['TimeStamp'] = TimeStamp
        self.data['OpenPrice'] = OpenPrice
        self.data['HighPrice'] = HighPrice
        self.data['LowPrice'] = LowPrice
        self.data['ClosePrice'] = ClosePrice

    def monthPrice(self, Num, ByMinute=True):
        Time = Date()
        
        TimeStamp = []
        OpenPrice = []
        HighPrice = []
        LowPrice = []
        ClosePrice = []

        for i in range(Num):
            End = Time.ISOString()
            if ByMinute:
                Start = Time.Shift(Hour=-2).ISOString()
                Result = self.swap.get_history_kline(instrument_id='BTC-USDT-SWAP',start=End, end=Start, granularity='60')
            else:
                Start = Time.Shift(Day=-10).ISOString()
                Result = self.swap.get_history_kline(instrument_id='BTC-USDT-SWAP',start=End, end=Start, granularity='3600')

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

        self.data['TimeStamp'] = TimeStamp
        self.data['OpenPrice'] = OpenPrice
        self.data['HighPrice'] = HighPrice
        self.data['LowPrice'] = LowPrice
        self.data['ClosePrice'] = ClosePrice


    def MACD(self, Fastperiod=30, Slowperiod=60, SignalPeriod=200):
        DIF, DEA, NOIR = talib.MACD(
            numpy.array(self.data['ClosePrice']),
            fastperiod=Fastperiod, 
            slowperiod=Slowperiod, 
            signalperiod=SignalPeriod)

        tempDIF = []
        tempDEA = []
        tempMACD = []
        tempMACDI = []
        tempMACDII = []

        for Item in DIF:
            if numpy.isnan(Item):
                tempDIF.append(None)
            else:
                tempDIF.append(round(Item,2))

        for Item in DEA:
            if numpy.isnan(Item):
                tempDEA.append(None)
            else:
                tempDEA.append(round(Item,2))

        for Item in list(DIF - DEA):
            if numpy.isnan(Item):
                tempMACD.append(None)
            else:
                tempMACD.append(round(Item*2,2))

        for Counter in range(len(tempMACD)):
            if Counter == 0:
                tempMACDI.append(None)
            elif tempMACD[Counter-1] == None:
                tempMACDI.append(None)
            else:
                Interval =  round(tempMACD[Counter]-tempMACD[Counter-1],2)
                if Interval>=0:
                    tempMACDI.append(1)
                else:
                    tempMACDI.append(-1)

        for Counter in range(len(tempMACDI)):
            if Counter == 0:
                tempMACDII.append(None)
            elif tempMACDI[Counter-1] == None:
                tempMACDII.append(None)
            else:
                if tempMACDI[Counter]>0 and tempMACDI[Counter-1]<0:
                    tempMACDII.append(1)
                elif tempMACDI[Counter]<0 and tempMACDI[Counter-1]>0:
                    tempMACDII.append(-1)
                else:
                    tempMACDII.append(0)

        self.data['DIF'] = tempDIF
        self.data['DEA'] = tempDEA
        self.data['MACD'] = tempMACD
        self.data['MACDInterval'] = tempMACDI
        self.data['MACDIntervalInverse'] = tempMACDII
       

    def strategyBackTrack(self, Offset):
        if not self.Initialized:
            self.StartPoint = 0
            self.Offset = Offset

            for Counter in range(len(self.data['TimeStamp'])):
                ItemNum = 0
                for Item in self.data:
                    ItemNum += 1
                    if self.data[Item][Counter] == None:
                        self.StartPoint+=1
                        break
                if ItemNum == len(self.data):
                    break
            
            self.CurrentPoint = self.StartPoint + self.Offset - 1
            self.Initialized = True

        if self.CurrentPoint < len(self.data['TimeStamp']) - 1:
            self.CurrentPoint += 1
            return True
        return False


    def strategyMACD(self, TimePoint):
        if self.data['MACDIntervalInverse'][TimePoint-1] == 1: #Long
            if self.shortOrder:
                size = self.getOrderInfoById(self.shortOrder[0])['size']
                self.shortOrder.append(self.placeOrderMatchPrice(4, size))
                self.orderList.append(['Short', self.shortOrder])
                self.shortOrder = None
            if not self.longOrder:
                self.cancelAll()
                self.longOrder = [self.placeOrderMatchPrice(1,1)]

        if self.data['MACDIntervalInverse'][TimePoint-1] == -1: #Short
            if self.longOrder:
                size = self.getOrderInfoById(self.longOrder[0])['size']
                self.longOrder.append(self.placeOrderMatchPrice(3, size))
                self.orderList.append(['Long', self.longOrder])
                self.longOrder = None
            if not self.shortOrder:
                self.cancelAll()
                self.shortOrder = [self.placeOrderMatchPrice(2,1)]
        
