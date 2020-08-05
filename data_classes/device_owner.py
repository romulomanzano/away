from mongoengine import Document
from mongoengine.fields import ReferenceField


class DeviceOwner(Document):
    """This class persists the devices"""

    user = ReferenceField("User")
    device = ReferenceField("Device")
