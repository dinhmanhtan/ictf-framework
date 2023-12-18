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
def get_flags():
    query_string = request.query_string.decode("utf-8")
    response = requests.get(
        f"http://{SETTING.DB_HOST}/flags?{query_string}&secret={SETTING.SECRET_DB}"
    )

    return response.json()


@requires_db_ip
def get_flags_submissions():
    query_string = request.query_string.decode("utf-8")
    response = requests.get(
        f"http://{SETTING.DB_HOST}/flags/submissions?{query_string}&secret={SETTING.SECRET_DB}"
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
    team_scores = []
    for score in scores:
        ts = {
            "team_name": teams[str(score["team_id"])]["name"],
            "total_points": score["total_points"],
            "attack_points": 0,
            "defense_points": 0,
            "sla_points": 0,
        }
        for service_id in range(10001, 10007):
            service_score = score[str(service_id)]
            if service_score:
                ts["attack_points"] += service_score["attack_points"]
                ts["defense_points"] += service_score["defense_points"]
                ts["sla_points"] += service_score["sla_points"]
        team_scores.append(ts)

    return {"success": True, "scores": team_scores}


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
