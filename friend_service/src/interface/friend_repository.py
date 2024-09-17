import uuid
from abc import abstractmethod
from typing import Tuple, List
from django.db import models

from ..models.models import Friend, FriendRequest


class FriendRepository:
    @abstractmethod
    def reject(self, req_id : uuid.UUID):
        pass

    @abstractmethod
    def accept(self, req_id: uuid.UUID, main_user : uuid.UUID , user_id: uuid.UUID) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def send_req(self, friendship_req : FriendRequest):
        pass

    @abstractmethod
    def list_friends(self, user_id: uuid.UUID) -> Tuple[models.QuerySet, str]:
        pass

    @abstractmethod
    def list_requests(self, user_id: uuid.UUID) -> Tuple[models.QuerySet, str]:
        pass