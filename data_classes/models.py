from mongoengine import Document
from mongoengine.fields import ReferenceField, ListField, StringField, DictField


class Device(Document):
    """This class persists the devices"""

    eui = StringField(required=True)
    device_type = StringField(required=True)


class DeviceOwner(Document):
    """This class persists the devices"""

    user = ReferenceField("User")
    device = ReferenceField("Device")


class Role(Document):
    """This class persists the roles of a user"""

    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)


class User(Document):
    """This class persists the devices"""

    roles = ListField(ReferenceField("Device"))
    email = StringField(required=True)


class SensorEventBlob(Document):  # remove after testing
    """This class persists the devices"""

    topic = StringField()
    payload = DictField(required=True)
