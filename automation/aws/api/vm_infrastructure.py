import os
from flask import request
import threading, json
import re, requests
from settings import SETTING, VAR_FILE_PATH, GAME_CONFIG_PATH, SQL
from update_infrastructure import (
    apply_infrastructure,
    update_vars,
    destroy_infrastructure,
)
from api.helpers import requires_db_ip
from register_vms import bootstrap_game
from api.create_teams import add_teams_info
from api.create_services import database_api_secret_path, create_all_services
import paramiko
import io
import concurrent.futures


# @app.route("/init_infrastructure", methods=["GET"])
def init_infrastructure():
    x = threading.Thread(target=apply_infrastructure, args=({"type": "register_vm"},))
    x.start()

    return {"success": True}


# @app.route("/update_infrastructure", methods=["POST"])
def update_infrastructure():
    configs = request.json
    vm_names = []
    for vm_name_config in configs.keys():
        vm_names.append(vm_name_config.split("_")[0])

    print(configs)
    update_vars(configs=configs)
    x = threading.Thread(
        target=apply_infrastructure,
        args=({"type": "register_vm", "register_data": vm_names},),
    )
    x.start()

    return {"success": True}


# @app.route("/getlatest/infrastructure/logs", methods=["GET"])
def get_latest_log():
    # r = requests.get(
    #     f"http://{SETTING.DB_HOST}/getlatest/infrastructure/logs?secret={SETTING.SECRET_DB}"
    # )
    sql = SQL()
    res = sql.cursor.execute(
        """ SELECT content  from infrastructure_logs ORDER BY created_at DESC LIMIT 1  """
    )
    data = res.fetchone()

    if data == None:
        return {"success": True, "content": data, "done": True}

    content = data[0]
    if content == None:
        return {"success": True, "content": result, "done": True}
    str1 = "".join(
        c if (ord(c) < 128 and ord(c) > 30) or c == "\n" else "" for c in content
    )

    result = re.sub("\[\d+m", "", str1)
    result = re.sub("\[\?\d.+", "", result)
    result = re.sub("\[\d[A-Z]", "", result)
    result = result.replace("Infrastructure Logs\n", "")

    index = result.find("DONE!!!")
    done = True if index != -1 else False

    sql.conn.close()
    return {"success": True, "content": result, "done": done}


# @app.route("/get/infrastructure/logs/<int:id>", methods=["GET"])
def get_log_by_id(id):
    r = requests.get(
        "http://{}/get/infrastructure/logs/{}?secret={}".format(
            SETTING.DB_HOST, id, SETTING.SECRET_DB
        )
    )
    content = r.json()["data"]["content"]
    str1 = "".join(
        c if (ord(c) < 128 and ord(c) > 30) or c == "\n" else "" for c in content
    )

    result = re.sub("\[\d+m", "", str1)
    result = re.sub("\[\?\d.+", "", result)
    result = re.sub("\[\d[A-Z]", "", result)
    result = result.replace("Infrastructure Logs\n", "")

    index = result.find("DONE!!!")
    done = True if index != -1 else False

    return {"success": True, "content": result, "done": done}


# @app.route("/vm/get_all", methods=["GET"])
def get_all_vm():
    if SETTING.DB_HOST == None:
        return {"success": False, "msg": "Database instance was null"}

    page = request.args.get("page", 1)
    size = request.args.get("size", 10)

    r = requests.get(
        f"http://{SETTING.DB_HOST}/vm/get_all?secret={SETTING.SECRET_DB}&page={page}&size={size}"
    )
    data = r.json()
    # print(data)
    if data["count"] == 0:
        return {"success": False, "type": "register"}

    return data


# @app.route("/vm/get/<string:vm_name>", methods=["GET"])
@requires_db_ip
def get_vm_by_name(vm_name):
    r = requests.get(
        f"http://{SETTING.DB_HOST}/vm/get/{vm_name}?secret={SETTING.SECRET_DB}"
    )
    data = r.json()

    return data


# @app.route("/vm/add", methods=["POST"])
def add_vm():
    data = request.json
    # oneOfvm_types = [
    #     "database",
    #     "gamebot",
    #     "router",
    #     "scoreboard",
    #     "teaminterface",
    #     "logger",
    #     "dispatcher",
    # ]
    # teamvm_config = []
    # scriptbot_config = []
    # # print(data)
    # vm_config_data = data.get("configs")

    # initiate = False

    # vm_configs = {}
    # for vm in vm_config_data:
    #     if vm["vm_type"] in oneOfvm_types:
    #         vm_configs[f"{vm['vm_type']}_configuration"] = {
    #             "instance_type": vm["instance_type"],
    #             "volume_size": vm["volume_size"],
    #         }
    #         initiate = True

    #     elif vm["vm_type"].startswith("teamvm"):
    #         teamvm_config.append(
    #             {
    #                 "id": int(vm["id"]),
    #                 "instance_type": vm["instance_type"],
    #                 "volume_size": int(vm["volume_size"]),
    #             }
    #         )
    #     elif vm["vm_type"] == "scriptbot" or vm["vm_type"].startswith("scriptbot"):
    #         scriptbot_config.append(
    #             {
    #                 "id": int(vm["id"]),
    #                 "instance_type": vm["instance_type"],
    #                 "volume_size": int(vm["volume_size"]),
    #             }
    #         )
    # # If this is the fisrt initiation of VMs
    # if initiate:
    #     vm_configs["teamvm_configuration"] = teamvm_config
    #     vm_configs["scriptbot_configuration"] = scriptbot_config
    # else:
    #     with open(VAR_FILE_PATH, "r") as f:
    #         vars = json.load(f)

    #         if teamvm_config != []:
    #             arr = vars["teamvm_configuration"]
    #             for sc in teamvm_config:
    #                 arr.append(sc)
    #             vm_configs["teamvm_configuration"] = arr

    #         if scriptbot_config != []:
    #             arr = vars["scriptbot_configuration"]
    #             for sc in scriptbot_config:
    #                 arr.append(sc)
    #             vm_configs["scriptbot_configuration"] = arr

    # if data.get("scriptbot_num", None) != None:
    #     vm_configs["scriptbot_num"] = data["scriptbot_num"]

    # if data.get("teams_num", None) != None:
    #     vm_configs["teams_num"] = data["teams_num"]

    # update_vars(configs=vm_configs)

    x = threading.Thread(target=apply_infrastructure, args=({"type": "register_vm"},))
    x.start()

    return {"success": True}


# @app.route("/vm/delete", methods=["POST"])
def delete_vm():
    data = request.json
    instance_type = None
    instance_id = None

    if data != None:
        with open(VAR_FILE_PATH, "r") as f:
            vars = json.load(f)
            instance_type = data.get("instance_type", None)
            instance_id = int(data.get("id", None))
            if instance_type == None and instance_id == None:
                return {
                    "ok": False,
                    "msg": "instance type and instance id can't be null",
                }, 400

            if instance_type == "teamvm":
                teamvm_configurations = vars["teamvm_configuration"]
                teamvm_configurations = [
                    tvm for tvm in teamvm_configurations if tvm["id"] != instance_id
                ]

                vars["teamvm_configuration"] = teamvm_configurations

                if vars["teams_num"] == len(teamvm_configurations) + 1:
                    vars["teams_num"] = vars["teams_num"] - 1
                else:
                    return {"success": True}

            if instance_type == "scriptbot":
                scriptbot_configurations = vars["scriptbot_configuration"]

                scriptbot_configurations = [
                    sc for sc in scriptbot_configurations if sc["id"] != instance_id
                ]
                vars["scriptbot_configuration"] = scriptbot_configurations
                if vars["scriptbot_num"] == len(scriptbot_configurations) + 1:
                    vars["scriptbot_num"] = vars["scriptbot_num"] - 1
                else:
                    return {"success": True}

        with open(VAR_FILE_PATH, "w") as f:
            json.dump(vars, f, indent=2)

    deleted_data = {"type": f"delete_{instance_type}"}
    if instance_type == "teamvm":
        deleted_data["team_id"] = instance_id
    elif instance_type == "scriptbot":
        deleted_data["scriptbot_id"] = instance_id

    x = threading.Thread(target=apply_infrastructure, args=(deleted_data,))
    x.start()

    return {"success": True}


# @app.route("/vm/reset_all", methods=["GET"])
def vm_reset():
    x = threading.Thread(target=destroy_infrastructure)
    x.start()

    return {"success": True}


def register_game():
    with open(VAR_FILE_PATH, "r") as f:
        vars = json.load(f)
        bootstrap_game(GAME_CONFIG_PATH, "terraform.exe", vars)

    game_config = json.load(open(GAME_CONFIG_PATH, "r"))

    if os.path.isfile(database_api_secret_path):
        f = open(database_api_secret_path, "r")
        database_api_secret = f.read().rstrip()
        db_secret = database_api_secret  # to read from the folder "secrets" generated by the make_secret.sh script

        add_teams_info("http://" + SETTING.DB_HOST, db_secret, game_config)
    else:
        raise Exception("Missing database secrets!")

    create_all_services(
        "http://{}".format(SETTING.DB_HOST),
        db_secret,
        game_config["services"],
        game_config["service_metadata"]["host_dir"],
    )

    return {"success": True}


def test_ssh_connection(vm_name, hostname, port, username, private_key_content):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()

        # Automatically add the server's host key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SSH server using key-based authentication
        if not vm_name.startswith("team") or vm_name == "teaminterface":
            private_key = paramiko.RSAKey(file_obj=io.StringIO(private_key_content))
            ssh.connect(hostname, port, username, pkey=private_key, timeout=3)

        # Close the SSH connection
        ssh.close()
        return None

    except Exception as e:
        return {"vm_name": vm_name, "error": str(e)}


# @app.route("/vm/check_ssh", methods=["GET"])
@requires_db_ip
def check_ssh_all_vms():
    r = requests.get(
        f"http://{SETTING.DB_HOST}/vm/get_all?secret={SETTING.SECRET_DB}&page=1&size=15"
    )
    data = r.json()
    vms = data["data"]

    r = requests.get(
        f"http://{SETTING.DB_HOST}/team/vm/get_all?secret={SETTING.SECRET_DB}"
    )
    data = r.json()
    team_vms = data["result"]

    vm_fail = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit worker_function for each thread
        futures = []
        for vm in vms:
            if not vm["vm_name"].startswith("teamvm"):
                futures.append(
                    executor.submit(
                        test_ssh_connection,
                        vm["vm_name"],
                        vm["ip"],
                        22,
                        "ubuntu",
                        vm["root_key"],
                    )
                )
        # for vm in team_vms:
        #     futures.append(
        #         executor.submit(
        #             test_ssh_connection,
        #             f"team{vm['team_id']}",
        #             vm["ip"],
        #             22,
        #             "ctf",
        #             vm["ctf_key"],
        #         )
        #     )

        # Retrieve results as they become available
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result:
                    vm_fail.append(result)
            except Exception as e:
                print(f"An error occurred: {e}")

    return {"success": True, "vm_fail": vm_fail}


# @app.route("/vm/check_ssh", methods=["POST"])
@requires_db_ip
def check_ssh_vm(vm_name):
    key_path = f"./sshkeys/{vm_name}-key.key"
    data = request.json
    ip = data["ip"]
    if vm_name.startswith("teamvm"):
        return {"success": True, "fail": False}
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey(filename=key_path)

        if not vm_name.startswith("teamvm") or vm_name == "teaminterface":
            ssh.connect(ip, 22, "ubuntu", pkey=private_key)

            print("SSH connection successful ", vm_name)

            ssh.close()

        return {"success": True, "fail": False}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"success": True, "fail": True}, 400
