from utils import logged
import argparse
import config
from mqtt_mixin import MqttMixin
import asyncio
from gmqtt.mqtt.constants import MQTTv311
import json

# gmqtt also compatible with uvloop
import uvloop
import signal
from models import Device, SensorEventBlob
from mongoengine import connect

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
STOP = asyncio.Event()


def ask_exit(*args):
    STOP.set()


@logged
class EventHandler(MqttMixin):
    def __init__(self):
        # initialize
        self.define_mqtt_client("away-event-handler")
        connect(host=config.MONGO_DB_URI)

    async def on_message(
        self, client, topic, payload, qos, properties
    ):  # pylint: disable=unused-argument
        """
        Define how to handle the incoming stream
        """
        SensorEventBlob(topic=topic, payload=json.loads(payload)).save()
        self.logger.info("Event persisted.")

    async def handle_events(self):
        self.mqtt_client.set_auth_credentials(
            config.TELEMATICS_MQTT_BROKER_AUTH_TOKEN, None
        )
        await self.mqtt_client.connect(
            config.TELEMATICS_MQTT_BROKER_HOST,
            config.TELEMATICS_MQTT_BROKER_HOST_PORT,
            ssl=True,
            version=MQTTv311,
            raise_exc=True,
            keepalive=60,
        )
        self.mqtt_client.subscribe(
            config.TELEMATICS_MQTT_APPLICATION_ALERTS_TOPIC, qos=1
        )
        await STOP.wait()
        await self.mqtt_client.disconnect()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--action",
        help="Define what you want to do.",
        choices=["handle_sensor_events"],
        required=True,
    )
    args = parser.parse_args()

    if args.action == "handle_sensor_events":
        loop = asyncio.get_event_loop()
        orchestrator = EventHandler()
        loop.add_signal_handler(signal.SIGINT, ask_exit)
        loop.add_signal_handler(signal.SIGTERM, ask_exit)
        loop.run_until_complete(asyncio.gather(orchestrator.handle_events()))


if __name__ == "__main__":
    main()
