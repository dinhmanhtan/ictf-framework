#!/usr/bin/env python3
import os
import json
import subprocess
import requests
from datetime import datetime
import traceback
import time
from register_vms import bootstrap_game
from settings import VAR_FILE_PATH, SETTING, SQL


def update_vars(configs):
    oneOfvm_types = [
        "database_configuration",
        "gamebot_configuration",
        "router_configuration",
        "scoreboard_configuration",
        "teaminterface_configuration",
        "logger_configuration",
        "dispatcher_configuration",
    ]

    updated_vars = {}
    with open(VAR_FILE_PATH, "r") as f:
        vars = json.load(f)
        for key, val in configs.items():
            # print(key, val)
            if val == None:
                continue

            if key in vars:
                if key in oneOfvm_types:
                    vars[key] = {
                        "instance_type": val["instance_type"],
                        "volume_size": int(val["volume_size"]),
                    }
                else:
                    vars[key] = val
            elif key.startswith("teamvm"):
                teamvm_configs = vars["teamvm_configuration"]
                id_ = int(key[6])
                for index, vm in enumerate(teamvm_configs):
                    if vm["id"] == id_:
                        teamvm_configs[index] = {
                            "id": id_,
                            "instance_type": val["instance_type"],
                            "volume_size": int(val["volume_size"]),
                        }
                        break
                vars["teamvm_configuration"] = teamvm_configs
            elif key.startswith("scriptbot"):
                scriptbot_configs = vars["scriptbot_configuration"]
                id_ = int(key[9])
                for index, vm in enumerate(scriptbot_configs):
                    if vm["id"] == id_:
                        scriptbot_configs[index] = {
                            "id": id_,
                            "instance_type": val["instance_type"],
                            "volume_size": int(val["volume_size"]),
                        }
                        break
                vars["scriptbot_configuration"] = scriptbot_configs

        updated_vars = vars

    with open(VAR_FILE_PATH, "w") as f:
        json.dump(updated_vars, f, indent=2)


def update_log_to_db(sql, content, id):
    sql.cursor.execute(
        """UPDATE infrastructure_logs
                                  SET content = ?
                              WHERE id = ? """,
        (content, id),
    )
    sql.conn.commit()


def apply_infrastructure(data=None):
    args = [
        "terraform.exe",
        "-chdir=./infrastructure",
        "apply",
        "--parallelism=3",
        "-var-file",
        "../ictf_game_vars.auto.tfvars.json",
        "-auto-approve",
    ]
    sql = SQL()

    stdout, stderr = "", ""
    try:
        logs = "Infrastructure Logs\n"
        sql.cursor.execute(
            """INSERT INTO infrastructure_logs
                            (content)
                        VALUES (?)""",
            (logs,),
        )
        id = sql.cursor.lastrowid
        sql.conn.commit()

        if id == None:
            print("Fail to add logs to DB")
        else:
            with subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True,
            ) as p:
                start = datetime.now()

                for line in p.stdout:
                    logs += line

                    now = datetime.now()
                    difference = now - start
                    seconds = difference.total_seconds()

                    if seconds >= 1.5:
                        start = now
                        update_log_to_db(sql, logs, id)

                for line in p.stderr:
                    logs += line

                    now = datetime.now()
                    difference = now - start
                    seconds = difference.total_seconds()

                    if seconds >= 1.5:
                        start = now
                        update_log_to_db(sql, logs, id)

            # print("end", len(logs))

            if "error" in logs.lower() or data == None:
                print("err", data)
                logs += "DONE!!!"
                update_log_to_db(sql, logs, id)
                sql.conn.close()
                return

            if data.get("type") == "delete_teamvm":
                team_id = data.get("team_id")
                if team_id == None:
                    print("teamid is None")
                    logs += "DONE!!!"
                    update_log_to_db(sql, logs, id)
                    sql.conn.close()
                    return

                r = requests.delete(
                    f"http://{SETTING.DB_HOST}/vm/delete/teamvm{team_id}?secret={SETTING.SECRET_DB}"
                )
                result = r.json()
                if not result["success"]:
                    print(
                        f"failed to delete vm-teamvm{team_id}: {r.text} /n",
                    )

                r = requests.delete(
                    f"http://{SETTING.DB_HOST}/team/vm/delete/{team_id}?secret={SETTING.SECRET_DB}"
                )
                result = r.json()
                if not result["success"]:
                    print(
                        f"failed to delete teamvm{team_id} configs: {r.text} /n",
                    )

            if data.get("type") == "delete_scriptbot":
                scriptbot_id = data.get("scriptbot_id")
                if scriptbot_id == None:
                    print("scriptbot is None")
                    logs += "DONE!!!"
                    r = requests.post(
                        "http://{}/infrastructure/update/logs/{}?secret={}".format(
                            SETTING.DB_HOST, id, SETTING.SECRET_DB
                        ),
                        json={"content": logs},
                    )
                    return
                print("Remove sciptbot configs in DB")
                r = requests.delete(
                    f"http://{SETTING.DB_HOST}/vm/delete/scriptbot{scriptbot_id}?secret={SETTING.SECRET_DB}"
                )
                result = r.json()
                if not result["success"]:
                    print(
                        f"failed to delete vm-scriptbot{scriptbot_id}: {r.text} /n",
                    )

            if SETTING.DB_HOST != None and data.get("type") == "register_vm":
                print("--------Register VM-------")
                register_data = data.get("register_data", [])
                with open(VAR_FILE_PATH, "r") as f:
                    vars = json.load(f)
                    bootstrap_game(
                        "../../game_config.json",
                        "terraform.exe",
                        vars,
                        register_data,
                    )

            SETTING.get_db_public_ip()
            ping = False
            if SETTING.DB_HOST:
                while not ping:
                    try:
                        r = requests.get(f"http://{SETTING.DB_HOST}/game/ping")
                        ping = True
                    except:
                        time.sleep(1)

            logs += "DONE!!!"
            update_log_to_db(sql, logs, id)
            sql.conn.close()

    except Exception as e:
        sql.conn.close()
        print("Exception:", e)
        traceback.print_exc()


def destroy_infrastructure():
    args = [
        "terraform.exe",
        "-chdir=./infrastructure",
        "destroy",
        "--parallelism=3",
        "-var-file",
        "../ictf_game_vars.auto.tfvars.json",
        "-auto-approve",
    ]
    sql = SQL()
    try:
        logs = "Infrastructure Logs\n"
        sql.cursor.execute(
            """INSERT INTO infrastructure_logs
                            (content)
                        VALUES (?)""",
            (logs,),
        )
        id = sql.cursor.lastrowid
        sql.conn.commit()

        if id == None:
            print("Fail to add logs to DB")
        else:
            with subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True,
            ) as p:
                start = datetime.now()

                for line in p.stdout:
                    logs += line

                    now = datetime.now()
                    difference = now - start
                    seconds = difference.total_seconds()

                    if seconds >= 1.5:
                        start = now
                        update_log_to_db(sql, logs, id)

                for line in p.stderr:
                    logs += line

                    now = datetime.now()
                    difference = now - start
                    seconds = difference.total_seconds()

                    if seconds >= 1.5:
                        start = now
                        update_log_to_db(sql, logs, id)

            PROV_FOLDER = os.path.dirname(os.path.abspath(__file__))
            INFRAS_FOLDER = os.path.join(PROV_FOLDER, "infrastructure")

            if "error" not in logs.lower():
                try:
                    os.remove(f"{INFRAS_FOLDER}/terraform.tfstate")
                    os.remove(f"{INFRAS_FOLDER}/terraform.tfstate.backup")

                except OSError as e:
                    print(f"Error: {e}")

            logs += "DONE!!!"
            update_log_to_db(sql, logs, id)
            SETTING.DB_HOST = None

    except Exception as e:
        print("Exception:", e)
        traceback.print_exc()

    sql.conn.close()
