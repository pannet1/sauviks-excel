# import xlwings as xw
# import pandas as pd
# wb = xw.Book("Book5.xlsx")
# ws1= wb.sheets["Sheet1"]
# ws2= wb.sheets["Sheet2"]

# d = {'Column1': [1, 2, 3], 'Column2':[1,2,3]}
# for i in range(0,100):
#     d['Column1'].append(i)
#     d['Column2'].append(i)
#     df = pd.DataFrame(d)
#     ws1= wb.sheets["Sheet1"]
#     ws2= wb.sheets["Sheet2"]
#     ws1["B2"].value = df
#     ws2["B2"].value = df
# import time
# time.sleep(500)
# wb.save('Book5.xlsx')

from SmartApi import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger
import pyotp
from toolkit.fileutils import Fileutils
import sys
import xlwings as xw
import pandas as pd
import os


DIRP = "../../"
SETG = Fileutils().get_lst_fm_yml(DIRP + "creds.yml")
angel_one = SETG["angelone"]
correlation_id = "abc123"
action = 1
mode = 3
token_list = [{"exchangeType": 1, "tokens": ["26009"]}]


def connect_to_angel_one():
    global refreshToken, feedToken, api, auth_token
    api = SmartConnect(api_key=angel_one["api_key"])
    totp = pyotp.TOTP(angel_one["totp"]).now()
    data = api.generateSession(angel_one["username"], angel_one["pwd"], totp)
    logger.info(data)
    if data["status"] == False:
        logger.error(data)
        sys.exit()
    refreshToken = data["data"]["refreshToken"]
    feedToken = api.getfeedToken()
    auth_token = api.access_token
    # return smartApi


def addActivate(wb, sheetName, template=None):
    # https://stackoverflow.com/questions/60432751/how-to-add-new-sheet-if-its-not-exist-in-python-using-xlwings
    try:
        sht = wb.sheets(sheetName).activate()
    except:
        if template:
            template.sheets["Template"].api.Copy(wb.sheets.active.api)
            sht = wb.sheets["Template"].api.Name = sheetName
        else:
            sht = wb.sheets.add(sheetName)
    return sht





def on_open(wsapp):
    logger.info("on open")
    some_error_condition = False
    if some_error_condition:
        error_message = "Simulated error"
        if hasattr(wsapp, "on_error"):
            wsapp.on_error("Custom Error Type", error_message)
    else:
        sws.subscribe(correlation_id, mode, token_list)


def on_data(wsapp, message):
    # df1.update(message)
    # ws1["B2"].value = df1
    # df2.update(message)
    # ws2["B2"].value = df2
    pprint(message)


def on_error(wsapp, error):
    logger.error(error)


def on_close(wsapp):
    logger.info("Close")


def on_control_message(wsapp, message):
    logger.info(f"Control Message: {message}")


def close_connection():
    sws.close_connection()


if __name__ == "__main__":
    input_xlsx = "Books1.xlsx"
    global wb, ws1, ws2, df1, df2
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    if os.path.isfile(input_xlsx):
        wb = xw.Book(input_xlsx)
    else:
        wb = xw.Book()
        wb.save(input_xlsx)
        wb = xw.Book(input_xlsx)
    ws1= addActivate(wb, 'Sheet1')
    ws2= addActivate(wb, 'Sheet2')
    connect_to_angel_one()
    logger.info(api.getProfile(refreshToken))
    sws = SmartWebSocketV2(
        auth_token=auth_token,
        api_key=angel_one["api_key"],
        client_code=angel_one["username"],
        feed_token=feedToken,
        max_retry_attempt=2,
        retry_strategy=0,
        retry_delay=10,
        retry_duration=30,
    )
    # Assign the callbacks.
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close
    sws.on_control_message = on_control_message

    sws.connect()
