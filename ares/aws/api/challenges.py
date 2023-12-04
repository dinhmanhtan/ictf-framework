import requests
from settings import SETTING
from api.helpers import requires_db_ip


@requires_db_ip
def get_all_services():
    r = requests.get(
        f"http://{SETTING.DB_HOST}/services/get_all?secret={SETTING.SECRET_DB}"
    )
    data = r.json()

    return data
