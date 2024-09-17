import uuid
from abc import abstractmethod
from typing import List, Tuple

from ..models.models import FriendRequest, Friend


class FriendService:
    @abstractmethod
    def send_request(self, validated_data : dict):
        pass

    @abstractmethod
    def accept_request(self, req_id: uuid.UUID, main_user : uuid.UUID , user_id: uuid.UUID):
        pass

    @abstractmethod
    def reject_request(self, req_id : uuid.UUID):
        pass

    @abstractmethod
    def get_friend_list(self, user_id : uuid.UUID) -> Tuple[List[Friend], str]:
        pass

    @abstractmethod
    def get_friendship_requests(self, user_id : uuid.UUID) -> Tuple[List[FriendRequest], str]:
        pass



