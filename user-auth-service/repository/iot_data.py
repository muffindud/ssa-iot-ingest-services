from json import loads

from services.postgres import Database


db = Database()

def get_device_from_db(device_mac: str) -> dict | None:
    results = db.execute_query(
        "SELECT id, name, type FROM devices WHERE name = %s",
        (device_mac,)
    )

    if results:
        device = results[0]
        device_id, name, device_type = device
        return {
            'id': device_id,
            'name': name,
            'type': device_type
        }

    return None


def create_device_in_db(device_mac: str, device_type: str) -> int:
    result = db.execute_query(
        "INSERT INTO devices (name, type) VALUES (%s, %s) RETURNING id",
        (device_mac, device_type)
    )

    device_id = result[0][0]

    return device_id


def get_device_id(device_mac: str) -> int | None:
    result = db.execute_query(
        "SELECT id FROM devices WHERE name = %s",
        (device_mac,)
    )

    if result:
        return result[0][0]

    return None


def get_device_owner_id(device_id: int) -> int | None:
    result = db.execute_query(
        "SELECT user_id FROM user_devices WHERE device_id = %s",
        (device_id,)
    )

    if result:
        return result[0][0]

    return None
