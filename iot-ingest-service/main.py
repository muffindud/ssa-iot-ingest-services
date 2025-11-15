from os import getenv
from random import randint

from paho.mqtt import client as mqtt


BROKER = getenv("ECLIPSE_MQTT_BROKER", "localhost")
PORT = int(getenv("ECLIPSE_MQTT_PORT", 1883))
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
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(TOPIC)
    client.on_message = on_message


def run() -> None:
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == "__main__":
    run()
