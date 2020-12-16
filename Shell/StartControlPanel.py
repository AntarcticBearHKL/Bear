if True:
    import PyBear.GlobalBear as GlobalBear
    import PyBear.Library.Data.Redis as RedisBear
    import PyBear.Library.Cipher as CipherBear

    import PyBear.Utilities.Financial.Market as MarketBear
    import PyBear.Utilities.Financial.Analyst as AnalystBear
    import PyBear.Utilities.Financial.Brokor as BrokorBear

    import PyBear.Utilities.Financial.BrokorProcedure.OHCLVA as OHCLVA
    import PyBear.Utilities.Financial.BrokorProcedure.MACD as MACD
    import PyBear.Utilities.Financial.BrokorProcedure.BOLL as BOLL
    import PyBear.Utilities.Financial.BrokorProcedure.KDJ as KDJ
    import PyBear.Utilities.Financial.BrokorProcedure.RSI as RSI
    import PyBear.Utilities.Financial.BrokorProcedure.StrategyMACD as StrategyMACD
    import PyBear.Utilities.Financial.BrokorProcedure.Recommander as Recommander
    import PyBear.Utilities.Financial.BrokorProcedure.Buyer as Buyer


    import PyBear.Utilities.Financial.AnalystProcedure.CHNStockUpdate as CHNStockUpdate
    import PyBear.Utilities.Financial.AnalystProcedure.CHNStockStrategyCore as CHNStockStrategyCore

    GlobalBear.NewServer(
        'MySQL', '47.95.119.172', 3306,
        'Debuger', 'A11b22;;')
    GlobalBear.NewServer(
        'MongoDB', '47.95.119.172', 27017,
        'Debuger', 'A11b22;;')
    GlobalBear.NewServer(
        'Redis', '47.95.119.172', 6379,
        'Debuger', 'A11b22;;')

    GlobalBear.NewServer(
        'RedisLocal', '192.168.0.233', 6379,
        'Debuger', 'A11b22;;')

def DataScan(Name):
    keys = RedisBear.Redis('RedisLocal').hgetall(Name)
    Keys = list(keys)
    Keys.sort()
    for Item in Keys:
        if keys[Item] == 'Success':
            print(Item)

def Analyst():
    Analyst = AnalystBear.Analyst()
    #Analyst.LoadModule(CHNStockUpdate.Config())
    Analyst.LoadModule(CHNStockStrategyCore.Config())
    Analyst.Run()

def BrokorTest():
    Brokor = BrokorBear.Brokor()
    Brokor.Process(OHCLVA.Config({
        'StockCode': '000001.SZ',
        'Day': '1000'
    }))
    Brokor.Process(MACD.Config({
        'Fast': '22',
        'Slow': '120',
        'Signal': '9'
    }))
    Brokor.Process(KDJ.Config({
        'FastK': '22',
        'SlowK': '5',
        'SlowD': '5',
    }))
    Brokor.Process(StrategyMACD.Config({}))
    Brokor.Run()
    Brokor.PrintData(['KDJF', 'KDJS'])

    '''Brokor.Process(Buyer.Config({
        'Target': 'StrategyMACD',
        'Asset': '100000'
    }))
    Brokor.Run()
    ret = Brokor.Result['Buyer']
    for Item in ret:
        print(Item)
        print('\n')'''

def t():
    import random
    a = 100000
    while True:
        if random.random()>=0.5:
            a = int(a*1.01)
        else:
            a = int(a*0.99)
        print(a)


if __name__ == '__main__':
    DataScan('CoreStrategy_806')
    #Analyst()
    #BrokorTest()