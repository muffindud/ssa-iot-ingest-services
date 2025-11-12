from services.postgres import Database


db = Database()


def get_user_device_ids(user_id: int) -> list[int]:
    results = db.execute_query(
        "SELECT device_id FROM user_devices WHERE user_id = %s",
        (user_id,)
    )

    device_ids = [row[0] for row in results]
    return device_ids


def truncate_user_data() -> None:
    db.execute_query("TRUNCATE TABLE user_devices")
    db.execute_query("TRUNCATE TABLE users")
    db.execute_query("TRUNCATE TABLE devices")
