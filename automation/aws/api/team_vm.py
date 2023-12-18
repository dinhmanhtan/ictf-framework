from flask import request
import requests
from settings import SETTING, GAME_CONFIG_PATH
from api.helpers import requires_db_ip, get_game_config_from_file


def get_teams():
    if SETTING.DB_HOST == None:
        game_configs = get_game_config_from_file(GAME_CONFIG_PATH)
        team_configs = game_configs["teams"]
        teams = {}
        if not team_configs:
            return {"success": True, "teams": teams}

        for team_config in team_configs:
            teams[team_config["id"]] = team_config
        return {"success": True, "teams": teams}

    else:
        r = requests.get(
            f"http://{SETTING.DB_HOST}/teams/info?secret={SETTING.SECRET_DB}"
        )
        data = r.json()

    return data


@requires_db_ip
def get_all_teamvm():
    r = requests.get(
        f"http://{SETTING.DB_HOST}/team/vm/get_all?secret={SETTING.SECRET_DB}"
    )
    data = r.json()
    # SETTING.get_db_public_ip()

    return data


@requires_db_ip
def add_teams():
    data = request.json
    teams = data.get("teams", None)
    if teams != None:
        for team in teams:
            result = requests.post(
                f"http://{SETTING.DB_HOST}/team/add_direct?secret={SETTING.SECRET_DB}",
                data=team,
            )

            response = result.json()
            if response["result"] != "success":
                print("ERROR %s" % response["fail_reason"])
                return {"success": False}

    return {"success": True}


# @app.route("/team/vm/get/<int:team_id>")
@requires_db_ip
def team_vm_get(team_id):
    res = requests.get(
        "http://{}/team/vm/get/{}?secret={}".format(
            SETTING.DB_HOST, team_id, SETTING.SECRET_DB
        )
    )
    data = res.json()

    return data


# @app.route("/team/info/id/<int:team_id>")
@requires_db_ip
def team_info(team_id):
    res = requests.get(
        f"http://{SETTING.DB_HOST}/team/info/id/{team_id}?secret={SETTING.SECRET_DB}"
    )
    data = res.json()

    return data


# @app.route("/team/delete/<int:team_id>", methods=["DELETE"])
@requires_db_ip
def team_delete(team_id):
    res = requests.delete(
        f"http://{SETTING.DB_HOST}/team/delete/{team_id}?secret={SETTING.SECRET_DB}"
    )
    data = res.json()

    return data

