#!/usr/bin/env python3

import subprocess
import argparse
import os
import json
import requests
import threading


class TfOutputException(Exception):
    """
    Exception raised by terraform if the output command fails
    """


class NoSSHKeyFoundException(Exception):
    """
    Exception raised when the team's private key is not found
    """


class NoDatabaseSecretFoundException(Exception):
    """
    Exception raised when the database's secret is not found
    """


class NoGameConfigFoundException(Exception):
    """
    Exception raised when the game config is not found
    """


class RegistrationErrorException(Exception):
    """
    Exception raised when the registration of a team fails
    """


class NoInstancePublicIpFound(Exception):
    """
    Exception raised when the instance public ip is not found
    """


SSHKEYS_FOLDER = "./sshkeys/"
SECRETS_FOLDER = "../../secrets/"

FAKE_IP = "0.0.0.0"


def _execute_terraform_output(args, terraform_path):
    try:
        tf_output_process = subprocess.run(
            "{} -chdir='./infrastructure' output {}".format(terraform_path, args),
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        data = tf_output_process.stdout.decode("utf-8").strip()
        if "No outputs found" in data:
            return None
        return data
    except Exception as e:
        # print(e)
        return None

    # if tf_output_process.returncode != 0:
    #     return {}


def _get_teamvm_public_ips(terraform_path):
    teamvms_ips = _execute_terraform_output("-json teamvms_public_ip", terraform_path)
    if teamvms_ips == None:
        return []

    teamvms_ips = json.loads(teamvms_ips)

    return teamvms_ips


def _get_scriptbot_public_ips(terraform_path):
    scriptbots_ips = _execute_terraform_output(
        "-json scriptbots_public_ip", terraform_path
    )
    if scriptbots_ips == None:
        return []

    scriptbots_ips = json.loads(scriptbots_ips)

    return scriptbots_ips


def get_instance_public_ip(instance_name, terraform_path):
    return _execute_terraform_output(
        "{}_public_ip".format(instance_name), terraform_path
    )


def get_instance_private_ip(instance_name, terraform_path):
    return _execute_terraform_output(
        "{}_private_ip".format(instance_name), terraform_path
    )


def register_team_vm(
    db_api,
    db_secret,
    team_id,
    team_ip,
    team_ssh_private_key_path,
    vm_config,
    update=False,
):
    # db_api = "192.168.1.18:5001"
    if not os.path.exists(team_ssh_private_key_path):
        raise NoSSHKeyFoundException

    with open(team_ssh_private_key_path, "r") as priv_key_f:
        team_ssh_private_key = priv_key_f.read()

    register_team_vm_url = "http://{}/team/add/keys/{}".format(db_api, team_id)
    if update:
        register_team_vm_url = "http://{}/team/update/keys/{}".format(db_api, team_id)

    data = {
        "ctf_key": team_ssh_private_key,
        "root_key": "",
        "ip": team_ip,
        "port": 0,
        "instance_type": vm_config["instance_type"],
        "volume_size": vm_config["volume_size"],
    }

    result = requests.post(
        register_team_vm_url, data=data, params={"secret": db_secret}
    )
    response = result.json()
    if response["result"] == "success":
        return response["team_id"]
    else:
        raise RegistrationErrorException(response)


def register_vm(db_api, db_secret, vm_name, ip, private_ip, vm_config, update=False):
    print(f"Registry {vm_name} VM")
    # db_api = "192.168.1.18:5001"

    if vm_name.startswith("scriptbot"):
        vm_ssh_private_key_path = f"{SSHKEYS_FOLDER}/scriptbot-key.key"
    else:
        vm_ssh_private_key_path = f"{SSHKEYS_FOLDER}/{vm_name}-key.key"

    if not os.path.exists(vm_ssh_private_key_path):
        raise NoSSHKeyFoundException

    with open(vm_ssh_private_key_path, "r") as priv_key_f:
        vm_ssh_private_key = priv_key_f.read()

    url = "http://{}/vm/add/config".format(db_api)

    data = {
        "root_key": vm_ssh_private_key,
        "vm_name": vm_name,
        "ip": ip,
        "private_ip": private_ip,
        "instance_type": vm_config["instance_type"],
        "volume_size": vm_config["volume_size"],
    }
    if update:
        url = "http://{}/vm/update/config".format(db_api)

    result = requests.post(url, data=data, params={"secret": db_secret})
    response = result.json()
    if response["result"] == "success":
        return True
    else:
        print(response)
        # raise RegistrationErrorException(response)


def bootstrap_game(game_config_path, terraform_path, ictf_vars, updated_vms=[]):
    if not os.path.exists(game_config_path):
        raise NoGameConfigFoundException

    with open(game_config_path, "r") as game_config_f:
        game_config = json.load(game_config_f)

    print(
        "\n[*] ---------------- STEP 4: Register teamvms into the database ----------------"
    )
    database_api_secret_path = os.path.join(SECRETS_FOLDER, "database-api/secret")
    database_public_ip = get_instance_public_ip("database", terraform_path)
    database_public_ip = database_public_ip.replace('"', "")
    print(database_public_ip)

    if not os.path.exists(database_api_secret_path):
        raise NoDatabaseSecretFoundException

    with open(database_api_secret_path, "r") as db_secret_f:
        database_api_secret = db_secret_f.read().rstrip()

    normal_vms = [
        "database",
        "gamebot",
        "router",
        "scoreboard",
        "logger",
        "dispatcher",
        "teaminterface",
    ]

    t1 = threading.Thread(
        target=register_teamvms,
        args=(
            game_config,
            database_public_ip,
            database_api_secret,
            ictf_vars,
            terraform_path,
            updated_vms,
        ),
    )
    t2 = threading.Thread(
        target=register_scriptbots,
        args=(
            database_public_ip,
            database_api_secret,
            ictf_vars,
            terraform_path,
            updated_vms,
        ),
    )
    thread_vm_list = [t1, t2]

    for vm_name in normal_vms:
        t = threading.Thread(
            target=register_other_vms,
            args=(
                vm_name,
                database_public_ip,
                database_api_secret,
                ictf_vars,
                terraform_path,
                updated_vms,
            ),
        )
        thread_vm_list.append(t)

    for vm_register_thread in thread_vm_list:
        vm_register_thread.start()

    for vm_register_thread in thread_vm_list:
        vm_register_thread.join()


def register_other_vms(
    vm_name,
    database_public_ip,
    database_api_secret,
    ictf_vars,
    terraform_path,
    updated_vms,
):
    vm_config = get_vm_config(vm_name, ictf_vars)
    private_ip = get_instance_private_ip(vm_name, terraform_path)
    if vm_name == "database":
        public_ip = database_public_ip
    else:
        public_ip = get_instance_public_ip(vm_name, terraform_path)
        if public_ip:
            public_ip = public_ip.replace('"', "")

    update = False
    if vm_name in updated_vms:
        update = True

    if public_ip:
        register_vm(
            database_public_ip,
            database_api_secret,
            vm_name,
            public_ip,
            private_ip,
            vm_config,
            update,
        )


def register_scriptbots(
    database_public_ip, database_api_secret, ictf_vars, terraform_path, updated_vms
):
    scriptbot_ips = _get_scriptbot_public_ips(terraform_path)
    scriptbot_vm_configs = get_vm_config("scriptbot", ictf_vars)
    if len(scriptbot_ips) <= 0:
        return
    for index, scriptbot_config in enumerate(scriptbot_vm_configs):
        i = scriptbot_config["id"]
        print("[+] Registering Scriptbot {}".format(i))

        config = scriptbot_vm_configs[index]
        scriptbot_public_ip = scriptbot_ips.get(f"scriptbot{i}", None)

        update = False
        if f"scriptbot{i}" in updated_vms:
            update = True

        if scriptbot_public_ip:
            register_vm(
                database_public_ip,
                database_api_secret,
                f"scriptbot{i}",
                scriptbot_public_ip,
                "",
                config,
                update,
            )


def register_teamvms(
    game_config,
    database_public_ip,
    database_api_secret,
    ictf_vars,
    terraform_path,
    updated_vms,
):
    teamvm_ips = _get_teamvm_public_ips(terraform_path)
    team_vms_config = ictf_vars["teamvm_configuration"]
    if len(teamvm_ips) > 0:
        for team_config in team_vms_config:
            print("[+] Registering Team {}".format(team_config["id"]))
            teamvm_public_ip = teamvm_ips.get(f"teamvm{team_config['id']}", None)

            if teamvm_public_ip:
                team_ssh_private_key_path = os.path.join(
                    SSHKEYS_FOLDER, "team{}-key.key".format(team_config["id"])
                )
                update = False
                if f"teamvm{team_config['id']}" in updated_vms:
                    update = True

                register_team_vm(
                    database_public_ip,
                    database_api_secret,
                    team_config["id"],
                    teamvm_public_ip,
                    team_ssh_private_key_path,
                    team_config,
                    update,
                )


def get_vm_config(name, config):
    vm_config_name = f"{name}_configuration"

    return config[vm_config_name]


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "-t",
#         "--terraform_path",
#         type=str,
#         default="terraform.exe",
#         help="Path to the terraform tool (default: terraform in your $PATH)",
#     )
#     args = parser.parse_args()

#     with open("ictf_game_vars.auto.tfvars.json", "r") as f:
#         ictf_vars = json.load(f)

#     bootstrap_game("../../game_config.json", args.terraform_path, ictf_vars)
