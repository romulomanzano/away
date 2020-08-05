from mongoengine import Document
from mongoengine.fields import StringField


class Role(Document):
    """This class persists the roles of a user"""

    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)
