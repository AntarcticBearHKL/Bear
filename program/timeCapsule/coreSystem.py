import os,sys
import pyBear.bear as bear
import pyBear.system.network.application as network 
from module import account 

bear.newServer('timeCapsuleDatabase', 'OWM4MjVjZmMyNWJjMzIwZmRjYjc3NzU2MTMwZjcyZGU=YTczYmZmZThmMjZhNDUzNzZkMTY5NDQ4ZGRiYzhmMzY=NmY1OTYyOWE3NzA5OWMyZTU1Y2RjNzcyNWFiODY1ODY=YjA5N2VmZDU3YWJjYzNmYzI3MTIzMDJkZjA0NGE3Yjc=ODllN2U2Y2IxOTdmNzk1NGE1NGViY2IxNGFiNmM4NmI=')

def getHandler(client):
    #client.printRequest()
    if client.path[1] != 'coreSystem':
        client.write('No Respond: 1649')
        return   
    if 'code' in client.argument:
        if str(client.argument['code']) in moduleList:
            ret = moduleList[str(client.argument['code'])](client)
            client.write(ret)
            return
    client.write('No Respond: 1648')

def parameterAnalyst(request, argument, body):
    return None

if __name__ == '__main__':
    moduleList = {}
    account.install(moduleList)

    network.httpServer(getHandler=getHandler, postHandler=None, parameterAnalyst=parameterAnalyst)
