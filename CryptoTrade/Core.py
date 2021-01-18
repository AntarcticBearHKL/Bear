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
import datetime
import talib
import numpy
import json

class CoreSystem:
    def __init__(self):
        self.StartTime = Date()
        self.Data = {}
        self.Long = [[-1]]
        self.Short = [[-1]]
        self.Profit = []
        self.Error = []

        api_key = "f735b07f-e18d-4ca3-8b8a-beaa61ad16c1"
        secret_key = "F042A3D395A940DEBA703A522B29DF78"
        passphrase = "T1r2a3deCode"

        self.Account = account.AccountAPI(api_key, secret_key, passphrase, False)

        self.Index = index.IndexAPI(api_key, secret_key, passphrase, False)

        self.Information = information.InformationAPI(api_key, secret_key, passphrase, False)

        self.Swap = swap.SwapAPI(api_key, secret_key, passphrase, False)

    def DataSave(self, Path):
        File.Write(Path, json.dumps(self.Data))

    def DataLoad(self, Path):
        self.Data = json.loads(File.Read(Path))

    def ResultSave(self, Path):
        Ret = {}
        Ret['Long'] = self.Long
        Ret['Short'] = self.Short
        Ret['Profit'] = self.Profit
        Ret['Error'] = [str(Item) for Item in self.Error]

        File.Write(Path, json.dumps(Ret))


    def GetMarketInfo(self):
        self.Data['Market'] = self.Swap.get_specific_ticker('BTC-USDT-SWAP')

    def GetWalletInfo(self):
        self.Data['Wallet'] = self.Swap.get_coin_account('BTC-USDT-SWAP')

    def GetOrderInfo(self):
        self.Data['Order'] = self.Swap.get_order_list(instrument_id='BTC-USDT-SWAP', state='6')[0]['order_info']

    def GetHoldingInfo(self):
        self.Data['Holding'] = self.Swap.get_specific_position('BTC-USDT-SWAP')['holding']


    def Open(self, Direction, Size, Price, ID='DefaultOrder'):
        self.Swap.take_order(instrument_id='BTC-USDT-SWAP', 
            type=Direction, price=Price, 
            size=Size, client_oid=ID)

    def Liquidate(self, Direction, Size, Price):
        self.Swap.take_order(instrument_id='BTC-USDT-SWAP', 
            type=int(Direction) + 2, price=Price, 
            size=Size, client_oid=ID)

    def CancelOrder(self, OrderID=None, ClientID=None):
        if OrderID:
            self.Swap.revoke_order(instrument_id='BTC-USDT-SWAP', order_id=OrderID)
        elif ClientID:
            self.Swap.revoke_order(instrument_id='BTC-USDT-SWAP', client_oid=ClientID)


    def PriceLatest(self, Num):
        Time = Date()
        
        TimeStamp = []
        OpenPrice = []
        HighPrice = []
        LowPrice = []
        ClosePrice = []

        for i in range(Num):
            End = Time.ISOString()
            Start = Time.Shift(Hour=-2).ISOString()
            Result = self.Swap.get_kline(instrument_id='BTC-USDT-SWAP',start=Start, end=End, granularity='60')

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

        self.Data['TimeStamp'] = TimeStamp
        self.Data['OpenPrice'] = OpenPrice
        self.Data['HighPrice'] = HighPrice
        self.Data['LowPrice'] = LowPrice
        self.Data['ClosePrice'] = ClosePrice

    def HistoryPrice(self, Num):
        Time = Date()
        
        TimeStamp = []
        OpenPrice = []
        HighPrice = []
        LowPrice = []
        ClosePrice = []

        for i in range(Num):
            End = Time.ISOString()
            if False:
                Start = Time.Shift(Hour=-2).ISOString()
                Result = self.Swap.get_history_kline(instrument_id='BTC-USDT-SWAP',start=End, end=Start, granularity='60')
            else:
                Start = Time.Shift(Day=-10).ISOString()
                Result = self.Swap.get_history_kline(instrument_id='BTC-USDT-SWAP',start=End, end=Start, granularity='3600')

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

        self.Data['TimeStamp'] = TimeStamp
        self.Data['OpenPrice'] = OpenPrice
        self.Data['HighPrice'] = HighPrice
        self.Data['LowPrice'] = LowPrice
        self.Data['ClosePrice'] = ClosePrice

    def EMA(self):
        self.Data['EMA5'] = talib.EMA(numpy.array(self.Data['ClosePrice']), timeperiod=5)
        self.Data['EMA10'] = talib.EMA(numpy.array(self.Data['ClosePrice']), timeperiod=10)
        self.Data['EMA20'] = talib.EMA(numpy.array(self.Data['ClosePrice']), timeperiod=20)
        self.Data['EMA60'] = talib.EMA(numpy.array(self.Data['ClosePrice']), timeperiod=60)
        
        for Item in ['EMA5','EMA10','EMA20','EMA60']:
            TempList = []
            for EMA in self.Data[Item]:
                if numpy.isnan(EMA):
                    TempList.append(None)
                else:
                    TempList.append(float(round(EMA, 2)))
            self.Data[Item] = TempList
        
        self.Data['EMA510IN'] = []
        for Counter in range(len(self.Data['EMA5'])):
            if self.Data['EMA5'][Counter] and self.Data['EMA10'][Counter]:
                self.Data['EMA510IN'].append(round(self.Data['EMA5'][Counter]-self.Data['EMA10'][Counter], 2))
            else:
                self.Data['EMA510IN'].append(None)

    def MACD(self):
        DIF, DEA, NOIR = talib.MACD(
            numpy.array(self.Data['ClosePrice']),
            fastperiod=10, 
            slowperiod=20, 
            signalperiod=10)

        self.Data['DIF'] = []
        self.Data['DEA'] = []
        self.Data['MACD'] = []
        self.Data['MACDIN'] = []

        for Item in DIF:
            if numpy.isnan(Item):
                self.Data['DIF'].append(None)
            else:
                self.Data['DIF'].append(round(Item,2))

        for Item in DEA:
            if numpy.isnan(Item):
                self.Data['DEA'].append(None)
            else:
                self.Data['DEA'].append(round(Item,2))

        for Item in list(DIF - DEA):
            if numpy.isnan(Item):
                self.Data['MACD'].append(None)
            else:
                self.Data['MACD'].append(round(Item*2,2))

        for Counter in range(len(self.Data['MACD'])):
            if Counter == 0:
                self.Data['MACDIN'].append(None)
            elif self.Data['MACD'][Counter-1] == None:
                self.Data['MACDIN'].append(None)
            else:
                self.Data['MACDIN'].append(round(self.Data['MACD'][Counter]-self.Data['MACD'][Counter-1],2))