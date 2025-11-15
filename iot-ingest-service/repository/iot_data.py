from json import loads

from services.mongo import DB


mongo_db = DB


def publish_data(device_id: int, data: dict) -> None:
    collection = mongo_db['iot_data']
    document = {
        'device_id': device_id,
        'data': data
    }
    collection.insert_one(document)
