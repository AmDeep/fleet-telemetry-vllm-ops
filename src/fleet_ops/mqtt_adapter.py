from __future__ import annotations

import json
from collections.abc import Callable


def subscribe(client: object, broker: str, on_message: Callable[[dict], None]) -> None:
    """Attach a paho-mqtt client without hiding the deployment configuration."""
    try:
        import paho.mqtt.client as mqtt
    except ImportError as error:
        raise RuntimeError("install the mqtt extra to use live MQTT mode") from error
    if not isinstance(client, mqtt.Client):
        raise TypeError("client must be paho.mqtt.client.Client")

    def handle(_client: object, _userdata: object, message: object) -> None:
        on_message(json.loads(message.payload.decode("utf-8")))

    client.on_message = handle
    client.connect(broker)
    client.subscribe("robots/+/telemetry", qos=1)
    client.loop_start()
