from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger
from api_helper import credentials, login, tkn_from_config
from pprint import pprint
import pandas as pd
import xlwings as xw
import os
import traceback

input_xlsx = "Books1.xlsx"


def addActivate(wb, sheetName):
    # https://stackoverflow.com/questions/60432751/how-to-add-new-sheet-if-its-not-exist-in-python-using-xlwings
    try:
        sht = wb.sheets(sheetName)
    except Exception as e:
        traceback.print_exc()
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


def get_workbook():

    if os.path.isfile(input_xlsx):
        wb = xw.Book(input_xlsx)
    else:
        wb = xw.Book()
        wb.save(input_xlsx)
        wb = xw.Book(input_xlsx)

    return wb


wb = get_workbook()


def run(dct, token_list):
    global df1, df2
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
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
        global df1, df2
        if isinstance(message, dict):
            pprint(message)
            _token_list: list = token_list[0].get("tokens")
            idx = _token_list.index(message.get("token", "0"))
            df_msg = {
                "Last Traded Time": message.get("last_traded_timestamp"),
                "Top Buy Price": max(
                    (
                        message.get("best_5_buy_data")[i].get("price")
                        for i in range(0, 5)
                    )
                ),
                "Bidx1": message.get("best_5_buy_data")[0].get("price"),
                "Bidx2": message.get("best_5_buy_data")[1].get("price"),
                "Bidx3": message.get("best_5_buy_data")[2].get("price"),
                "Bidx4": message.get("best_5_buy_data")[3].get("price"),
                "Bidx5": message.get("best_5_buy_data")[4].get("price"),
                "Volume": message.get("volume_trade_for_the_day"),
                "Last Traded Price": message.get("last_traded_price"),
                "Open Interest": message.get("open_interest"),
                "Top Sell Price": max(
                    (
                        message.get("best_5_sell_data")[i].get("price")
                        for i in range(0, 5)
                    )
                ),
                "Askx1": message.get("best_5_sell_data")[0].get("price"),
                "Askx2": message.get("best_5_sell_data")[1].get("price"),
                "Askx3": message.get("best_5_sell_data")[2].get("price"),
                "Askx4": message.get("best_5_sell_data")[3].get("price"),
                "Askx5": message.get("best_5_sell_data")[4].get("price"),
            }
            if idx == 0:
                try:
                    df1 = pd.concat([df1, pd.DataFrame([df_msg])], ignore_index=True)
                    ws1 = addActivate(wb, "Sheet1")
                    ws1["A1"].value = df1
                except:
                    traceback.print_exc()
            elif idx == 1:
                try:
                    df2= pd.concat([df2, pd.DataFrame([df_msg])], ignore_index=True)
                    ws2 = addActivate(wb, "Sheet2")
                    ws2["A1"].value = df2
                except:
                    traceback.print_exc()

    def on_error(wsapp, error):
        logger.error(error)

    def on_close(wsapp):
        logger.info("Close")

    def on_control_message(wsapp, message):
        logger.info(f"Control Message: {message}")

    def close_connection():
        sws.close_connection()
        wb.save(input_xlsx)

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
