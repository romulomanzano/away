import os
from dotenv import load_dotenv, find_dotenv

# load environment variables
load_dotenv(find_dotenv())

TELEMATICS_MQTT_BROKER_HOST = os.getenv("TELEMATICS_MQTT_BROKER_HOST")
TELEMATICS_MQTT_BROKER_HOST_PORT = int(
    os.getenv("TELEMATICS_MQTT_BROKER_HOST_PORT", "8883")
)
TELEMATICS_MQTT_BROKER_AUTH_TOKEN = os.getenv("TELEMATICS_MQTT_BROKER_AUTH_TOKEN")
# Alerts
TELEMATICS_MQTT_APPLICATION_ALERTS_TOPIC = os.getenv(
    "TELEMATICS_MQTT_APPLICATION_ALERTS_TOPIC"
)
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
REDIS_CONNECTION_STRING = os.getenv("REDIS_CONNECTION_STRING", "redis://redis:6379")
TASK_QUEUE = "task_queue"
