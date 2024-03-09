from omspy_brokers.angel_one import AngelOne
from __init__ import UTIL
from pprint import pprint
from rich import print


def login(config):
    api = AngelOne(**config)
    if api.authenticate():
        print("api connected")
    else:
        print("api not connected")
    return api


def credentials(obj_angel):
    h = obj_angel
    dct = dict(
        auth_token=h.auth_token,
        api_key=h._api_key,
        client_code=h._user_id,
        feed_token=h.obj.feed_token,
    )
    return dct


def tkn_from_config(broker, search: list) -> dict:
    dct = {}
    for exchsym in search:
        lst = exchsym.split(":")
        resp = broker.searchScrip(lst[0], lst[1])
        pprint(resp)
        token = resp["data"][0]["symboltoken"]
        dct.update({lst[1]: {"exchange": lst[0], "token": token}})
        print(token)
        UTIL.slp_for(2)
    return dct


if __name__ == "__main__":
    from __init__ import CRED, FUTL
    import pandas as pd
    # pd.set_option('display.max_rows', None)

    dct = FUTL.get_lst_fm_yml(CRED)
    print(dct)
    api = login(dct["angelone"])
    dct_sym_dtls: dict = tkn_from_config(api.obj, dct["search"])
    print(dct_sym_dtls)

    def greeks(broker):
        route = {
            "api.market.greeks": "/rest/secure/angelbroking/marketData/v1/optionGreek"
        }
        broker._routes.update(route)
        params = {
            "name": "NIFTY",
            "expirydate": "28MAR2024"
        }
        marketDataResult = broker._postRequest("api.market.greeks", params)
        return marketDataResult

    while True:
        resp = greeks(api.obj)
        if isinstance(resp, dict) and \
                resp.get("data", None):
            keys = ["name", "expiry", "tradeVolume"]
            dct = [{k: v for k, v in dct.items()
                    if k not in keys}
                   for dct in resp["data"]
                   ]

            df = pd.DataFrame(dct)
            print(df.head(n=30))
            UTIL.slp_for(1)
