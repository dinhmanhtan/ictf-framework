from flask import Flask
from flask_cors import CORS
import api
from settings import SQL

# from register_vms import bootstrap_game

app = Flask(__name__)
CORS(app)


app.add_url_rule("/teams/info", "get_teams", api.get_teams, methods=["GET"])
app.add_url_rule(
    "/team/vm/get_all", "get_all_teamvm", api.get_all_teamvm, methods=["GET"]
)
app.add_url_rule("/teams/add_direct", "add_teams", api.add_teams, methods=["POST"])
app.add_url_rule(
    "/team/vm/get/<int:team_id>", "team_vm_get", api.team_vm_get, methods=["GET"]
)
app.add_url_rule(
    "/team/info/id/<int:team_id>", "team_info", api.team_info, methods=["GET"]
)
app.add_url_rule(
    "/team/delete/<int:team_id>", "team_delete", api.team_delete, methods=["DELETE"]
)

# Infrastructure
app.add_url_rule(
    "/init_infrastructure",
    "init_infrastructure",
    api.init_infrastructure,
    methods=["GET"],
)

app.add_url_rule(
    "/update_infrastructure",
    "update_infrastructure",
    api.update_infrastructure,
    methods=["POST"],
)
app.add_url_rule(
    "/getlatest/infrastructure/logs",
    "get_latest_log",
    api.get_latest_log,
    methods=["GET"],
)

app.add_url_rule(
    "/get/infrastructure/logs/<int:id>",
    "get_log_by_id",
    api.get_log_by_id,
    methods=["GET"],
)

app.add_url_rule("/vm/get_all", "get_all_vm", api.get_all_vm, methods=["GET"])
app.add_url_rule(
    "/vm/get/<string:vm_name>", "get_vm_by_name", api.get_vm_by_name, methods=["GET"]
)
app.add_url_rule("/vm/add", "add_vm", api.add_vm, methods=["POST"])
app.add_url_rule("/vm/delete", "delete_vm", api.delete_vm, methods=["POST"])
app.add_url_rule("/vm/reset_all", "vm_reset", api.vm_reset, methods=["GET"])

# SERVICE API
app.add_url_rule(
    "/services/get_all", "get_all_services", api.get_all_services, methods=["GET"]
)

# GAME API
app.add_url_rule("/game/ison", "game_is_on", api.game_is_on, methods=["GET"])
app.add_url_rule(
    "/upload/game_config_file",
    "upload_game_config_file",
    api.upload_game_config_file,
    methods=["POST"],
)

app.add_url_rule(
    "/game/config_file",
    "get_game_config",
    api.get_game_config,
    methods=["GET"],
)
app.add_url_rule(
    "/game/register_db",
    "register_game",
    api.register_game,
    methods=["GET"],
)

app.add_url_rule(
    "/game/insert",
    "start_game",
    api.start_game,
    methods=["GET"],
)

app.add_url_rule(
    "/game/delete",
    "stop_game",
    api.stop_game,
    methods=["GET"],
)

app.add_url_rule(
    "/scores",
    "get_score",
    api.get_score,
    methods=["GET"],
)

app.add_url_rule(
    "/game/tick",
    "get_game_tick",
    api.get_game_tick,
    methods=["GET"],
)


with app.app_context():
    sql = SQL()
    sql.cursor.execute(""" DROP TABLE IF EXISTS infrastructure_logs """)
    sql.cursor.execute(
        """CREATE TABLE infrastructure_logs (id INTEGER PRIMARY KEY AUTOINCREMENT,content mediumblob,created_at timestamp not null default current_timestamp)"""
    )

    sql.conn.commit()
    sql.conn.close()


if __name__ == "__main__":
    app.run(host="localhost", port=9000, debug=True)
