import argparse
import config
from utils import logged
import gmqtt
from mqtt_mixin import MqttMixin
import asyncio

# gmqtt also compatible with uvloop
import uvloop
import signal

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
STOP = asyncio.Event()


def ask_exit(*args):
    STOP.set()


@logged
class Telematics(MqttMixin):
    def __init__(
        self,
        telematics_broker_host,
        telematics_port,
        telematics_auth_token,
        telematics_application_id,
    ):
        self.telematics_broker_host = telematics_broker_host
        self.telematics_port = telematics_port
        self.telematics_auth_token = telematics_auth_token
        self.telematics_application_id = telematics_application_id
        self.telematics_client = None
        # initialize internal mqtt client
        self.define_mqtt_client("{}-{}".format("Relayer", telematics_application_id))

    @staticmethod
    def _on_connect_telematics(
        client, flags, rc, properties
    ):  # pylint: disable=unused-argument
        Telematics.logger.info(
            "Connected - Telematics Hub {}".format(
                client._client_id  # skipcq: PYL-W0212
            )
        )

    @staticmethod
    def _on_disconnect_telematics(
        client, packet, exc=None
    ):  # pylint: disable=unused-argument
        Telematics.logger.info(
            "Disconnected - Telematics Hub {}".format(
                client._client_id  # skipcq: PYL-W0212
            )
        )

    @staticmethod
    def _assign_callbacks_to_client_telematics(client):
        # helper function which sets up client's callbacks
        client.on_connect = Telematics._on_connect_telematics
        client.on_disconnect = Telematics._on_disconnect_telematics

    async def initialize_telematics_connection(self):
        will_message = gmqtt.Message(
            config.TELEMATICS_MQTT_APPLICATION_ALERTS_TOPIC,
            "Unexpected Exit.",
            will_delay_interval=10,
            qos=1,
            retain=True,
        )
        self.telematics_client = gmqtt.Client(
            client_id="{}-{}".format(
                self.__class__.__name__, self.telematics_application_id
            ),
            clean_session=True,
            optimistic_acknowledgement=True,
            will_message=will_message,
        )
        Telematics._assign_callbacks_to_client_telematics(self.telematics_client)
        self.telematics_client.set_auth_credentials(self.telematics_auth_token, None)
        await self.telematics_client.connect(
            self.telematics_broker_host,
            self.telematics_port,
            ssl=True,
            version=5,
            raise_exc=True,
            keepalive=60,
        )

    async def on_message(
        self, client, topic, payload, qos, properties
    ):  # pylint: disable=unused-argument
        # forward and retain
        self.telematics_client.publish(
            config.TELEMATICS_MQTT_APPLICATION_TOPIC,
            payload,
            qos=1,
            content_type="json",
            retain=True,
            user_property=properties.get("user_property"),
        )
        self.logger.info("Retaining in our own MQTT broker.")

    async def post_inference_to_telematics_hub(self):
        # external telematics client
        await self.initialize_telematics_connection()
        # internal mqtt broker
        await self.mqtt_client.connect(
            config.LORA_MQTT_BROKER_HOST, config.LORA_MQTT_BROKER_HOST_PORT
        )
        self.mqtt_client.subscribe(config.LORA_MQTT_APPLICATION_TOPIC, qos=1)
        await STOP.wait()
        await self.mqtt_client.disconnect()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--action",
        help="Define what you want to do.",
        choices=["stream_inference_telematics"],
        required=True,
    )
    parser.add_argument(
        "--broker_host",
        help="Telematics broker host URL.",
        default=config.TELEMATICS_MQTT_BROKER_HOST,
    )
    parser.add_argument(
        "--broker_host_port",
        help="Telematics broker host port.",
        default=config.TELEMATICS_MQTT_BROKER_HOST_PORT,
    )
    parser.add_argument(
        "--broker_auth_token",
        help="Telematics broker auth token.",
        default=config.TELEMATICS_MQTT_BROKER_AUTH_TOKEN,
    )
    parser.add_argument(
        "--application-identifier",
        help="Application identifier for LORA Network.",
        default=config.LORA_APPLICATION_IDENTIFIER,
        dest="application_identifier",
    )

    args = parser.parse_args()

    if args.action == "stream_inference_telematics":
        telematics = Telematics(
            telematics_broker_host=args.broker_host,
            telematics_port=args.broker_host_port,
            telematics_auth_token=args.broker_auth_token,
            telematics_application_id=args.application_identifier,
        )
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, ask_exit)
        loop.add_signal_handler(signal.SIGTERM, ask_exit)
        loop.run_until_complete(
            asyncio.gather(telematics.post_inference_to_telematics_hub())
        )


if __name__ == "__main__":
    main()
