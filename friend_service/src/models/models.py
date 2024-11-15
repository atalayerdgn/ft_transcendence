import uuid
from typing import List

from django.db import models

class Friend(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    second_user_id = models.UUIDField(default=uuid.uuid4, editable=False)
