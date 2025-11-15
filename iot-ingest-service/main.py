from os import getenv
from random import randint
from json import loads

from jwt import decode as jwt_decode
from paho.mqtt import client as mqtt

from repository.iot_data import publish_data


BROKER = getenv("ECLIPSE_MQTT_BROKER", "localhost")
PORT = int(getenv("ECLIPSE_MQTT_PORT", 1883))
DEVICE_JWT_SECRET = getenv("DEVICE_JWT_SECRET")
TOPIC = "$share/group/iot/ingest"


def connect_mqtt() -> mqtt.Client:
    client_id = f"python-mqtt-{randint(0, 1000)}"
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id=client_id
    )
    client.connect(BROKER, PORT)
    return client


def subscribe(client: mqtt.Client) -> None:
    def on_message(client, userdata, msg) -> None:
        try:
            json = loads(msg.payload.decode())
            token = json.get("token")
            data = json.get("data")

            identity = jwt_decode(token, DEVICE_JWT_SECRET)

            if identity.get("device_id") is None or identity.get("role") != "device":
                print("Invalid token: missing device_id or incorrect role")
                return

            device_id = identity["device_id"]

            publish_data(device_id, data)

        except Exception as e:
            print(f"Error decoding JSON: {e}")
            return

    client.subscribe(TOPIC)
    client.on_message = on_message


def run() -> None:
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == "__main__":
    run()
