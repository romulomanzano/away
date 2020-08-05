from mongoengine import Document
from mongoengine.fields import ReferenceField, ListField, StringField


class User(Document):
    """This class persists the devices"""

    roles = ListField(ReferenceField("Device"))
    email = StringField(required=True)
