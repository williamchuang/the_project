import warnings
warnings.filterwarnings('ignore')
import time
from datetime import datetime
from myWrapper import IBWrapper, contract
from ib.ext.EClientSocket import EClientSocket
from ib.ext.ScannerSubscription import ScannerSubscription
accountName = "U9038813"
callback = IBWrapper()             # Instantiate IBWrapper. callback 
tws = EClientSocket(callback)      # Instantiate EClientSocket and return data to callback
# host = "192.168.1.165"
host = ""
port = 7497
#port = 4001
clientId = 12
tws.eConnect(host, port, clientId) # Connect to TWS
tws.setServerLogLevel(5)           # Set error output to verbose
create = contract()                # Instantiate contract class
callback.initiate_variables()
tws.reqAccountUpdates(1, accountName)
contract_info = create.create_contract("GC", "FUT", "NYMEX", "USD", "201902", "GCN8")
tws.reqAccountSummary(2,"All","NetLiquidation")
B=0
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
import gspread
from oauth2client.service_account import ServiceAccountCredentials

tws.reqPositions()


while True:
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Current-balance-5c8479f3db36.json', scope)
    gc = gspread.authorize(credentials)
    wks=gc.open_by_url("https://docs.google.com/spreadsheets/d/1a7YifpS7Klwvxy1Pz7qlD0rrKFRjZQ97vBPEUuhyhlo/edit#gid=0")
    ws = wks.get_worksheet(0)
    Time=datetime.now().strftime("%Y%m%d %H:%M:%S.%f")
    while len(callback.update_Position)>2:
        callback.update_Position.pop(0)
    if len(callback.update_Position)>0:
        Position=callback.update_Position[-1][13]
    else:
        Position=0
    while len(callback.account_Summary)>0:
        callback.account_Summary.pop(0)
    tws.reqAccountSummary(2,"All","NetLiquidation")
    while len(callback.account_Summary)<1:
        time.sleep(20)
    if len(callback.account_Summary)>0:
        B=callback.account_Summary[-1][3]
    ws.update_acell('B2', str(B))
    ws.update_acell('B3', str(Position))
    print(Position)
    ws.update_acell('B4', str(Time))

    time.sleep(240)
