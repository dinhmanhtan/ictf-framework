from flask import request
import requests
import json
import os.path
from settings import SETTING
from api.helpers import requires_db_ip
from datetime import datetime
import pytz


@requires_db_ip
def game_is_on():
    r = requests.get(f"http://{SETTING.DB_HOST}/game/ison?secret={SETTING.SECRET_DB}")
    data = r.json()

    return data


def upload_game_config_file():
    data = request.json

    with open("game_config.json", "w") as f:
        json.dump(data, f, indent=2)
    return {"success": True}


def get_game_config():
    if not os.path.isfile("game_config.json"):
        return {"config": None}

    with open("game_config.json", "r") as f:
        return {"config": f.read()}


@requires_db_ip
def start_game():
    response = requests.get(
        f"http://{SETTING.DB_HOST}/game/insert?secret={SETTING.SECRET_DB}"
    )

    return response.json()


@requires_db_ip
def stop_game():
    response = requests.get(
        f"http://{SETTING.DB_HOST}/game/delete?secret={SETTING.SECRET_DB}"
    )

    return response.json()


@requires_db_ip
def get_score():
    response = requests.get(
        f"http://{SETTING.DB_HOST}/teams/info?secret={SETTING.SECRET_DB}"
    )
    teams = response.json()["teams"]
    if not teams:
        return {"success": False, "msg": "No teams"}
    response = requests.get(
        f"http://{SETTING.DB_HOST}/scores?secret={SETTING.SECRET_DB}"
    )
    scores = response.json()["scores"]
    if not scores:
        print(response.json())
        return {"success": False}

    for id, team_score in scores.items():
        team_score["team_name"] = teams[id]["name"]
        scores[id] = team_score

    return {"success": True, "scores": list(scores.values())}


@requires_db_ip
def get_game_tick():
    response = requests.get(
        f"http://{SETTING.DB_HOST}/game/tick?secret={SETTING.SECRET_DB}"
    )
    data = response.json()
    if data["tick_id"] != 0:
        data["status"] = "on"
    else:
        data["status"] = "wait"

    date_format = "%Y-%m-%d %H:%M:%S"

    timestamp_begin = int(
        pytz.utc.localize(
            datetime.strptime(data["created_on"], date_format)
        ).timestamp()
    )
    timestamp_end = int(
        pytz.utc.localize(datetime.strptime(data["ends_on"], date_format)).timestamp()
    )

    data["created_on"] = timestamp_begin
    data["ends_on"] = timestamp_end

    return data
