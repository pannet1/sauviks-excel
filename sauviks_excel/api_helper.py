from omspy_brokers.angel_one import AngelOne


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


if __name__ == "__main__":
    from __init__ import CRED, FUTL

    config = FUTL.get_lst_fm_yml(CRED)
    api = login(config)
    print(credentials(api))
