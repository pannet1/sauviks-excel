from omspy_brokers.angel_one import AngelOne
from toolkit.fileutils import Fileutils


def login(config):
    api = AngelOne(**config)
    if api.authenticate():
        print("api connected")
    else:
        print("api not connected")
    return api


def credentials(obj_angel):
    h = obj_angel
    jwt = h.sess["data"]["jwtToken"]
    auth_token = jwt.split(' ')[1]
    print("acc", auth_token)
    dct = dict(
        auth_token=h.auth_token,
        api_key=h._api_key,
        client_code=h._user_id,
        feed_token=h.obj.feed_token,
    )
    return dct


if __name__ == "__main__":
    FUTL = Fileutils()
    config = FUTL.get_lst_fm_yml("../../angel_one.yml")
    api = login(config)
    print(credentials(api))
