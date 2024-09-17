import uuid
from typing import List

from django.db import models



class FriendRequest(models.Model):
    from_user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    to_user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Friend(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    friend_list = models.JSONField(default=list, blank=True)

    def add_friend(self, user_id):
        if user_id not in self.friend_list:
            self.friend_list.append(user_id)
