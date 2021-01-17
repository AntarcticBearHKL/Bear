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


def Open(Direction, Size, Price, ID='DefaultOrder'):
    Core.Swap.take_order(instrument_id='BTC-USDT-SWAP', 
        type=Direction, price=Price, 
        size=Size, client_oid=ID)

def Liquidate(Direction, Size, Price):
    Core.Swap.take_order(instrument_id='BTC-USDT-SWAP', 
        type=int(Direction) + 2, price=Price, 
        size=Size, client_oid=ID)

def CancelOrder():
    pass