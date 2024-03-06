from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import threading
from logzero import logger


class WebsocketClient():

    token_list = [
        {
            "exchangeType": 1,
            "tokens": ["26009"]
        }
    ]

    def __init__(self, kwargs):
        self.socket_open = False
        self.exch_str_int = {'NSE': 1, 'NFO': 2,
                             'BSE': 3, 'MCX': 5, 'NCDEX': 7, 'CDS': 13}
        self.exch_int_str = {1: 'NSE',  2: 'NFO',
                             3: 'BSE',  5: 'MCX', 7: 'NCDEX', 13: 'CDS'}
        self.ticks = {}
        self.auth_token = kwargs['auth_token'],
        self.api_key = kwargs['api_key'],
        self.client_code = kwargs['client_code'],
        self.feed_token = kwargs['feed_token']
        self.sws = SmartWebSocketV2(
            auth_token=self.auth_token,
            api_key=self.api_key,
            client_code=self.client_code,
            feed_token=self.feed_token,
            max_retry_attempt=2, retry_strategy=0,
            retry_delay=10, retry_duration=30)

    def soc_open(self, wsapp):
        self.socket_open = True
        logger.info("on open")
        logger.info("on open")
        some_error_condition = False
        if some_error_condition:
            error_message = "Simulated error"
            if hasattr(wsapp, 'on_error'):
                wsapp.on_error("Custom Error Type", error_message)
        else:
            self.sws.subscribe("sds", 3, self.token_list)

    def soc_data(self, wsapp, msg):
        logger.info(msg)
        self.ticks = msg
        print(msg)
        """
        self.ticks = {self.exch_int_str[msg['exchange_type']] +
                      ":" + str(msg['token']): msg['last_traded_price'] / 100}
        """

    def soc_error(self, wsapp, error):
        logger.error(error)

    def soc_close(self, wsapp):
        self.is_open = False
        logger.info("Close")

    def soc_control_message(self, wsapp, message):
        logger.info(f"Control Message: {message}")

    def start(self):
        # Assign the callbacks.
        self.sws.on_open = self.soc_open
        self.sws.on_data = self.soc_data
        self.sws.on_error = self.soc_error
        self.sws.on_close = self.soc_close
        self.sws.on_control_message = self.soc_control_message
        self.sws.connect()


if __name__ == "__main__":
    from toolkit.fileutils import Fileutils
    from time import sleep
    from api_helper import login, credentials

    FUTL = Fileutils()
    config = FUTL.get_lst_fm_yml("../../sauviks-excel.yml")
    obj_angel = login(config)
    dct = credentials(obj_angel)
    t1 = WebsocketClient(dct)
    t1.start()

    while t1.socket_open:
        token_list = [
            {
                "exchangeType": 1,
                "tokens": ["26000", "26009", "26022", "26023"]
            }
        ]
        t1.sws.subscribe("sdf", 3, token_list)
        break

    while True:
        print(f"ticks: {t1.ticks}")
        sleep(5)
