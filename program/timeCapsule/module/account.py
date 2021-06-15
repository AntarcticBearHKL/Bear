import pyBear.bear as bear
import json
import pyBear.mathematics.cipher as cipher
import pyBear.system.chronus as chronus
import pyBear.system.mongodb as mongo

def install(moduleList):
    moduleList['1101'] = createAccount
    moduleList['1102'] = debit
    moduleList['1103'] = credit
    moduleList['1105'] = deleteAccount
    moduleList['1106'] = transfer
    
    moduleList['1191'] = balanceSheet
    moduleList['1192'] = billing

def createAccount(client):
    # code name subject balance
    code = client.argument['1']
    name = client.argument['2']
    subject = client.argument['3']

    balanceSheet = mongo.collection('timeCapsuleDatabase', 'timeCapsule', 'balanceSheet') 
    if balanceSheet.search({'code':code}, count=True):
        return 'Account Exist'
    
    balanceSheet.insert({
        'code': code,
        'name': name,
        'subject': subject,
        'balance': '0.00',
    })
    return 'Success'

def debit(client):
    # code amount remark comment
    date = client.argument['1']
    amount = client.argument['2']
    remark = client.argument['3']
    comment = client.argument['4']
    code = client.argument['5']


    balanceSheet = mongo.collection('timeCapsuleDatabase', 'timeCapsule', 'balanceSheet')
    if not balanceSheet.search({'code':code}, count=True):
        return 'Account Not Exist'

    account = balanceSheet.search({'code':code})[0]
    if account['subject'] != '1':
        amount = -float(amount)/100
    else:
        amount = float(amount)/100
    accountValue = float(account['balance']) + amount

    balanceSheet.change({'code':code},{'$set':{'balance':str(accountValue)}})
    
    if len(date) < 14:
        time = date[0:8]
        timezone = date[8:]
    else:
        time = date[0:14]
        timezone = date[14:]
    date = chronus.frame(time, timeZone=timezone)
    datestr = date.stringify()
    dateint = date.timestamp()

    detailAccount = mongo.collection('timeCapsuleDatabase', 'timeCapsule', 'detailAccount')
    detailAccount.insert({
        'transactionID': cipher.UUID(),
        'datestr': datestr,
        'dateint': dateint,
        'code': code,
        'amount': str(amount),
        'remark': remark,
        'comment': comment
    })

    return 'Success'

def credit(client):
    # code amount remark comment
    date = client.argument['1']
    amount = client.argument['2']
    remark = client.argument['3']
    comment = client.argument['4']
    code = client.argument['5']


    balanceSheet = mongo.collection('timeCapsuleDatabase', 'timeCapsule', 'balanceSheet')
    if not balanceSheet.search({'code':code}, count=True):
        return 'Account Not Exist'

    account = balanceSheet.search({'code':code})[0]
    if account['subject'] == '1':
        amount = -float(amount)/100
    else:
        amount = float(amount)/100
    accountValue = float(account['balance']) + amount

    balanceSheet.change({'code':code},{'$set':{'balance':str(accountValue)}})
    
    if len(date) < 14:
        time = date[0:8]
        timezone = date[8:]
    else:   
        time = date[0:14]
        timezone = date[14:]
    date = chronus.frame(time, timeZone=timezone)
    datestr = date.stringify()
    dateint = date.timestamp()

    detailAccount = mongo.collection('timeCapsuleDatabase', 'timeCapsule', 'detailAccount')
    detailAccount.insert({
        'transactionID': cipher.UUID(),
        'datestr': datestr,
        'dateint': dateint,
        'code': code,
        'amount': str(amount),
        'remark': remark,
        'comment': comment
    })

    return 'Success'

def deleteAccount(client):
    pass

def transfer(client):
    if debit(client) != 'Success':
        return 'Error'
    client.argument['5'] = client.argument['6']
    if credit(client) != 'Success':
        return 'Error'
    return 'Success'

def balanceSheet(client):
    balanceSheet = mongo.collection('timeCapsuleDatabase', 'timeCapsule', 'balanceSheet')
    bs = balanceSheet.search({})
    ret = {
        'Asset': [],
        'Liabilities': [],
        'Equity': [],
    }
    for item in bs:
        del item['_id']
        if item['subject']=='1':
            ret['Asset'].append(item)
        elif item['subject']=='2':
            ret['Liabilities'].append(item)
        elif item['subject']=='3':
            ret['Equity'].append(item)
    return json.dumps(ret)

def billing(client):
    pass
