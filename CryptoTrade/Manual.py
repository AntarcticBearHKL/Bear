from PyBear.System import File
import PyBear.System.System as System
import Core as Core
import json

while True:
    System.ClearScreen()
    Content = json.loads(File.Read(r'C:\Users\Happy\Desktop\Result.txt'))
    Command = input("Command: ")
    if Command == '':
        pass

    elif Command == '1':
        Price = input('Price: ')
        if Price == '':
            Price = Data['Market']['last']
        else:
            Price = round(int(Price)/100.00, 2)

        Direction = input('Direction: ')
        Size = input('Size: ')

        input('下单：方向：' + str(Direction) + ' 委托数量：' + str(Size) + ' 委托价格：' + str(Price))
        Core.Open(Direction, Size, Price)
    elif Command == '2':
        Price = input('Price: ')
        if Price == '':
            Price = Data['Market']['last']
        else:
            Price = round(int(Price)/100.00, 2)

        Direction = input('Direction: ')
        Size = input('Size: ')

        input('平仓：方向：' + str(Direction) + ' 委托数量：' + str(Size) + ' 委托价格：' + str(Price))
        Core.Liquidate(Direction, Size, Price)

    elif Command == '60':
        print(Content)
    elif Command == '61':
        print(Content['Long'])
    elif Command == '62':
        print(Content['Short'])
    elif Command == '63':
        print(Content['Profit'])
    elif Command == '64':
        print(Content['TradeTimes'])
    elif Command == '65':
        print(Content['Error'])

    input("Press Enter To Continue ...")