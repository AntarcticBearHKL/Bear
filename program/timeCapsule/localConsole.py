import pyBear.bear as bear
import pyBear.system.network.application as network
import pyBear.system.utility as utility
import coreSystem as core

while True:
    utility.clearScreen()
    command = input('Please Input Command:')
    command = command.split('.')
    commandDict = {}
    for counter in range(len(command)):
        if counter == 0:
            commandDict['code'] = command[counter]
        else:
            commandDict[str(counter)] = command[counter]
    resultCode, result = network.httpGet('http://192.168.0.109/coreSystem', commandDict)
    if isinstance(result, str):
        print(resultCode, result)
    elif isinstance(result, dict):
        for item in result:
            print(item)
    input('Press Enter To Continue')
