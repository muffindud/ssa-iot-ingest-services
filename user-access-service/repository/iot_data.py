from json import loads

from services.postgres import Database
from services.mongo import DB


db = Database()
mongo_db = DB


def get_data(device_id: int, page: int = 1, size: int = 10) -> list[dict]:
    collection = mongo_db['iot_data']
    skip = (page - 1) * size
    with collection.find({'device_id': device_id}, {"data": 1, "_id": 0}).skip(skip).limit(size) as cursor:
        data = [doc["data"] for doc in cursor]
    return data


def truncate_mongo_data() -> None:
    collection = mongo_db['iot_data']
    collection.delete_many({})


def get_device_owner_id(device_id: int) -> int | None:
    result = db.execute_query(
        "SELECT user_id FROM user_devices WHERE device_id = %s",
        (device_id,)
    )

    if result:
        return result[0][0]

    return None
