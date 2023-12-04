import functools
from settings import SETTING
import json
import requests


def requires_db_ip(func):
    @functools.wraps(func)
    def wrapper(**kwds):  # pylint: disable=missing-docstring
        if SETTING.DB_HOST == None:
            return {"success": False, "msg": "Database instance was null"}
        else:
            if not SETTING.IS_DB_RUNNING:
                r = requests.get(f"http://{SETTING.DB_HOST}/game/ping")
                if r.text != "lareneg":
                    return {"success": False, "msg": "Database is not ready"}

            return func(**kwds)

    return wrapper


def get_game_config_from_file(PATH):
    with open(PATH, "r") as f:
        vars = json.load(f)
        return vars
