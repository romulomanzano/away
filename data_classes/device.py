from mongoengine import Document
from mongoengine.fields import StringField


class Device(Document):
    """This class persists the devices"""

    eui = StringField(required=True)
    device_type = StringField(required=True)
