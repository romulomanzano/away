import gmqtt
import utils
import config


@utils.logged
class MqttMixin:
    """
    A common interface to interact with MQTT.
    """

    def on_connect(
        self, client, flags, rc, properties
    ):  # pylint: disable=unused-argument
        self.logger.info("Connected - {}".format(self.__class__.__name__))

    def on_disconnect(
        self, client, packet, exc=None
    ):  # pylint: disable=unused-argument
        self.logger.info("Disconnected - {}".format(self.__class__.__name__))

    def on_subscribe(
        self, client, mid, qos, properties
    ):  # pylint: disable=unused-argument
        self.logger.info("Subscribed  - {}".format(self.__class__.__name__))

    def on_message(
        self, client, topic, payload, qos, properties
    ):  # pylint: disable=unused-argument
        """
        This is sub-class specific
        """
        raise NotImplementedError

    def define_mqtt_client(self, client_id):
        will_message = gmqtt.Message(
            "brokers/{}/alerts/service/{}/disconnected".format(
                client_id, self.__class__.__name__
            ),
            "Unexpected Exit.",
            will_delay_interval=10,
            qos=1,
            retain=False,
        )
        self.mqtt_client = gmqtt.Client(
            client_id=client_id,
            clean_session=True,
            optimistic_acknowledgement=True,
            will_message=will_message,
        )
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_subscribe = self.on_subscribe
