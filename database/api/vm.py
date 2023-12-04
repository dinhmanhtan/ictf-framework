import json
import sys
from flask import request

from . import app, mysql
from .utils import requires_auth


@app.route("/vm/get/<string:vm_name>")
@requires_auth
def vm_get(vm_name):
    to_return = {}

    try:
        cursor = mysql.cursor()

        cursor.execute(
            "SELECT vm_name,root_key, ip,instance_type, volume_size, private_ip FROM vm WHERE vm_name = %s ",
            (vm_name,),
        )

        key_cursor = cursor.fetchone()
        if key_cursor is None:
            to_return["num"] = "404"
            to_return["msg"] = "team not found"
            return json.dumps(to_return)

        to_return["vm_name"] = key_cursor["vm_name"]
        to_return["root_key"] = key_cursor["root_key"]
        to_return["ip"] = key_cursor["ip"]
        to_return["private_ip"] = key_cursor["private_ip"]
        to_return["instance_type"] = key_cursor["instance_type"]
        to_return["volume_size"] = key_cursor["volume_size"]

    except Exception as e:
        print(e)
        return json.dumps({"result": "failure", "reason": str(e)})

    return json.dumps(to_return)


@app.route("/vm/get_all")
@requires_auth
def vm_get_all():
    page = request.args.get("page", None)
    size = request.args.get("size", None)

    if not page or not page.isdigit() or int(page) < 1:
        page = 1
    if not size or not size.isdigit() or int(size) < 1:
        size = 10

    page = int(page)
    size = int(size)
    offset = (page - 1) * size

    try:
        cursor = mysql.cursor()

        cursor.execute(
            "SELECT vm_name,root_key, ip,instance_type, volume_size, private_ip FROM vm OFFSET %s LIMIT %s",
            (offset, size),
        )

        key_cursor = cursor.fetchall()

        return json.dumps(key_cursor)

    except Exception as e:
        print(e)
        return json.dumps({"result": "failure", "reason": str(e)})


@app.route("/vm/add/config", methods=["POST"])
@requires_auth
def vm_add_config():
    """
    It can be reached at
    ``/vm/add/config?secret=<API_SECRET>``.

    The JSON response is::

        {
          "result": "success" | "fail"
          "vm_name": string
        }

    :param string name: the name of vm
    :param string root_key:  root users private key
    :return: a JSON dictionary containing the result
    """
    try:
        vm_name = request.form.get("vm_name", None)
        if vm_name == None:
            return json.dumps({"result": "fail", "reason": "vm_name can't be null"})

        cursor = mysql.cursor()
        cursor.execute("""SELECT vm_name from vm WHERE vm_name = %s""", (vm_name,))

        if cursor.fetchone():
            return json.dumps({"result": "fail", "reason": "vm has already existed"})

        root_key = request.form.get("root_key", None)
        ip = request.form.get("ip", None)
        private_ip = request.form.get("private_ip", None)
        instance_type = request.form.get("instance_type", None)
        volume_size = request.form.get("volume_size", None)

        cursor = mysql.cursor()
        cursor.execute(
            """INSERT INTO vm
                                  (vm_name, root_key, ip,private_ip,instance_type,volume_size)
                              VALUES (%s, %s, %s, %s, %s, %s )""",
            (vm_name, root_key, ip, private_ip, instance_type, volume_size),
        )
        result_team_id = cursor.lastrowid

        mysql.database.commit()

        return json.dumps({"result": "success", "id": result_team_id})
    except Exception as e:
        print(e)
        return json.dumps({"result": "failure", "reason": str(e)})


@app.route("/vm/update/config", methods=["POST"])
@requires_auth
def vm_update_config():
    """
    Note that this endpoint requires a POST request.

    It can be reached at
    ``/vm/update/config?secret=<API_SECRET>``.

    The JSON response is::

        {
          "result": "success" | "fail"
          "vm_name": string
        }

    :param srting name: the name of the vm
    :param string root_key:  the new root users private key
    :return: a JSON dictionary containing the result
    """
    try:
        vm_name = request.form.get("vm_name", None)
        if vm_name == None:
            return json.dumps({"result": "fail", "reason": "vm_name can't be null"})

        cursor = mysql.cursor()
        cursor.execute("""SELECT vm_name from vm WHERE vm_name = %s""", (vm_name,))

        if not cursor.fetchone():
            return json.dumps({"result": "fail", "reason": "vm doesn't exsited"})

        root_key = request.form.get("root_key", None)
        ip = request.form.get("ip", None)
        private_ip = request.form.get("private_ip", None)
        instance_type = request.form.get("instance_type", None)
        volume_size = request.form.get("volume_size", None)

        cursor = mysql.cursor()
        cursor.execute(
            """UPDATE vm
                                  SET root_key = %s,
                                      ip = %s,
                                      private_ip = %s,
                                      instance_type = %s,
                                      volume_size = %s
                              WHERE vm_name = %s""",
            (root_key, ip, private_ip, instance_type, volume_size, vm_name),
        )
        mysql.database.commit()

        return json.dumps({"result": "success", "vm_name": vm_name})
    except Exception as e:
        print(e)
        return json.dumps({"result": "failure", "reason": str(e)})


@app.route("/getlatest/infrastructure/logs", methods=["GET"])
@requires_auth
def get_latest_infrastructure_logs():
    try:
        cursor = mysql.cursor()
        cursor.execute(
            """SELECT *  from infrastructure_logs ORDER BY created_at DESC LIMIT 1 """
        )
        result = cursor.fetchone()
        result["content"] = result["content"].decode("latin-1")
        return json.dumps({"result": "success", "data": result}, default=str)
    except Exception as e:
        print(e)
        return json.dumps({"result": "failure", "reason": str(e)})


@app.route("/get/infrastructure/logs/<int:id>", methods=["GET"])
@requires_auth
def get_infrastructure_log_by_id(id):
    try:
        cursor = mysql.cursor()
        cursor.execute("""SELECT *  from infrastructure_logs WHERE id = %s """, (id,))
        result = cursor.fetchone()
        result["content"] = result["content"].decode("latin-1")
        return json.dumps({"result": "success", "data": result}, default=str)
    except Exception as e:
        print(e)
        return json.dumps({"result": "failure", "reason": str(e)})


@app.route("/infrastructure/add/logs", methods=["POST"])
@requires_auth
def add_log_infrastructure():
    try:
        content = request.json.get("content", None)
        if content == None:
            return json.dumps({"result": "fail", "reason": "content can't be null"})

        cursor = mysql.cursor()
        cursor.execute(
            """INSERT INTO infrastructure_logs
                            (content)
                        VALUES (%s)""",
            (content,),
        )
        mysql.database.commit()
        log_id = cursor.lastrowid

        return json.dumps({"result": "success", "id": log_id})
    except Exception as e:
        print(e)
        return json.dumps({"result": "failure", "reason": str(e)})


@app.route("/infrastructure/update/logs/<int:id>", methods=["POST"])
@requires_auth
def update_infrastructure_logs(id):
    try:
        content = request.json.get("content", None)
        if content == None:
            return json.dumps({"result": "fail", "reason": "content can't be null"})

        cursor = mysql.cursor()
        cursor.execute(
            """SELECT created_at  from infrastructure_logs WHERE id = %s""", (id,)
        )

        if not cursor.fetchone():
            return json.dumps({"result": "fail", "reason": "not found"})

        cursor = mysql.cursor()
        cursor.execute(
            """UPDATE infrastructure_logs
                                  SET content = %s
                              WHERE id = %s""",
            (content, id),
        )
        mysql.database.commit()

        return json.dumps({"result": "success", "id": id})
    except Exception as e:
        print(e)
        return json.dumps({"result": "failure", "reason": str(e)})
