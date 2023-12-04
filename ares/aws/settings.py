from register_vms import get_instance_public_ip
import sqlite3
from ipaddress import ip_address

VAR_FILE_PATH = "ictf_game_vars.auto.tfvars.json"
GAME_CONFIG_PATH = "game_config.json"


class Setting:
    # DB_HOST = "192.168.1.18:5001"
    DB_HOST = None
    SECRET_DB = "baEwFwsT0KRtdwYMrZuxMybgU"
    IS_DB_RUNNING = False

    def __init__(self) -> None:
        self.get_db_public_ip()

    def get_db_public_ip(self):
        database_public_ip = get_instance_public_ip("database", "terraform.exe")
        if database_public_ip != None:
            database_public_ip = database_public_ip.replace('"', "")

        if database_public_ip and not (
            ip_address(database_public_ip).is_private
            or ip_address(database_public_ip).is_loopback
            or ip_address(database_public_ip).is_link_local
        ):
            self.DB_HOST = database_public_ip


class SQL:
    def __init__(self):
        self.conn = sqlite3.connect("game.db")
        self.cursor = self.conn.cursor()


SETTING = Setting()
