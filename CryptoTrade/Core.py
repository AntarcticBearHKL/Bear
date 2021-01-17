import okex.account_api as account
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import okex.index_api as index
import okex.option_api as option
import okex.system_api as system
import okex.information_api as information
import json
import datetime

Data = {}
Long = [[-1]]
Short = [[-1]]
Profit = []
Error = []

def Time():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"

api_key = "f735b07f-e18d-4ca3-8b8a-beaa61ad16c1"
secret_key = "F042A3D395A940DEBA703A522B29DF78"
passphrase = "T1r2a3deCode"

Account = account.AccountAPI(api_key, secret_key, passphrase, False)

Index = index.IndexAPI(api_key, secret_key, passphrase, False)

Information = information.InformationAPI(api_key, secret_key, passphrase, False)

Swap = swap.SwapAPI(api_key, secret_key, passphrase, False)

def DataSave(Path):
    File.Write(Path, json.dumps(Data))

def DataLoad(Path):
    Data = json.loads(File.Read(Path))


def Open(Direction, Size, Price, ID='DefaultOrder'):
    Swap.take_order(instrument_id='BTC-USDT-SWAP', 
        type=Direction, price=Price, 
        size=Size, client_oid=ID)

def Liquidate(Direction, Size, Price):
    Swap.take_order(instrument_id='BTC-USDT-SWAP', 
        type=int(Direction) + 2, price=Price, 
        size=Size, client_oid=ID)

def CancelOrder():
    pass


def Price():
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
        Result = Swap.get_history_kline(instrument_id='BTC-USDT-SWAP',start=End, end=Start, granularity='3600')

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