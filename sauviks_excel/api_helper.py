from omspy_brokers.angel_one import AngelOne
from __init__ import UTIL
from pprint import pprint


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

    dct = FUTL.get_lst_fm_yml(CRED)
    print(dct)
    api = login(dct["angelone"])
    dct_sym_dtls: dict = tkn_from_config(dct["search"])
    print(dct_sym_dtls)
