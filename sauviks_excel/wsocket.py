from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger
from api_helper import credentials, login
from __init__ import FUTL, CRED

from pprint import pprint
config = FUTL.get_lst_fm_yml(CRED)
print(config)
obj_angel = login(config)
print(obj_angel)

dct = credentials(obj_angel)
correlation_id = "abc123"
action = 1
mode = 3
token_list = [
    {
        "exchangeType": 1,
        "tokens": ["26009"]
    }
]
print(dct)
# retry_strategy=0 for simple retry mechanism
sws = SmartWebSocketV2(auth_token=dct["auth_token"],
                       api_key=dct["api_key"],
                       client_code=dct["client_code"],
                       feed_token=dct["feed_token"],
                       max_retry_attempt=2, retry_strategy=0,
                       retry_delay=10, retry_duration=30)

# retry_strategy=1 for exponential retry mechanism
# sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN,max_retry_attempt=3, retry_strategy=1, retry_delay=10,retry_multiplier=2, retry_duration=30)


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
