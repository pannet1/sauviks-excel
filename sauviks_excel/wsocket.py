from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger
from api_helper import credentials, login, tkn_from_config
from pprint import pprint
import pandas as pd
import xlwings as xw
import os


def addActivate(wb, sheetName, template=None):
    # https://stackoverflow.com/questions/60432751/how-to-add-new-sheet-if-its-not-exist-in-python-using-xlwings
    try:
        sht = wb.sheets(sheetName).activate()
    except Exception as e:
        print(e)
        if template:
            template.sheets["Template"].api.Copy(wb.sheets.active.api)
            sht = wb.sheets["Template"].api.Name = sheetName
        else:
            sht = wb.sheets.add(sheetName)
    return sht


def wsocket(**dct):
    # retry_strategy=1 for exponential retry mechanism
    # sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN,max_retry_attempt=3, retry_strategy=1, retry_delay=10,retry_multiplier=2, retry_duration=30)
    sws = SmartWebSocketV2(
        auth_token=dct["auth_token"],
        api_key=dct["api_key"],
        client_code=dct["client_code"],
        feed_token=dct["feed_token"],
        max_retry_attempt=2, retry_strategy=0,
        retry_delay=10, retry_duration=30)
    return sws


def run(dct, token_list):
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

    # websocket constants
    ws1 = addActivate(wb, 'Sheet1')
    ws2 = addActivate(wb, 'Sheet2')

    correlation_id = "sauviks"
    action = 1
    mode = 3
    sws = wsocket(**dct)

    def on_open(wsapp):
        logger.info("on open")
        some_error_condition = False
        if some_error_condition:
            error_message = "Simulated error"
            if hasattr(wsapp, 'on_error'):
                wsapp.on_error("Custom Error Type", error_message)
        else:
            sws.subscribe(correlation_id, mode, token_list)

    def on_data(wsapp, message):
        pprint(message)

    def on_error(wsapp, error):
        logger.error(error)

    def on_close(wsapp):
        logger.info("Close")

    def on_control_message(wsapp, message):
        logger.info(f"Control Message: {message}")

    def close_connection():
        sws.close_connection()

    # Assign the callbacks.
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close
    sws.on_control_message = on_control_message
    sws.connect()


# Websocket V2 sample code ENDS Here #######from SmartApi.smartWebSocketV2 import SmartWebSocketV2
#
if __name__ == "__main__":
    from __init__ import CRED, FUTL

    D_EXCHCODE = {'NSE': 1, 'NFO': 2,
                  'BSE': 3, 'MCX': 5, 'NCDEX': 7, 'CDS': 13}

    dct = FUTL.get_lst_fm_yml(CRED)
    api = login(dct["angelone"])
    # get the token from api
    dct_sym_dtls: dict = tkn_from_config(api.obj, dct["search"])
    logger.info(dct_sym_dtls)

    # Initialize a dictionary to store exchange data
    exchange_data = {}
    # Iterate over the original dictionary
    for key, value in dct_sym_dtls.items():
        exchange = value['exchange']
        token = value['token']
        # If the exchange is not in the exchange_data dictionary, initialize it
        if exchange not in exchange_data:
            exchange_data[exchange] = {
                'exchangeType': D_EXCHCODE[exchange], 'tokens': []}
        # Append the token to the list of tokens for the corresponding exchange
        exchange_data[exchange]['tokens'].append(token)
    # Convert the dictionary values to a list
    result = list(exchange_data.values())
    logger.info(result)

    # get more details need for wsocket from api
    config = credentials(api)
    logger.info(config)

    # start the wsocket
    run(config, token_list=result)
    # THIS WILL NO BE INTERPRETED
