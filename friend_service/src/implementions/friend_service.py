import uuid
from typing import Tuple, List

from ..implementions.friend_repository import FriendRepositoryImpl
from ..interface.friend_service import FriendService
from ..models.models import Friend, FriendRequest


class FriendServiceImpl(FriendService):
    def __init__(self, repository : FriendRepositoryImpl):
        self.repository = repository

    def send_request(self, validated_data : dict):
        friendship_req = FriendRequest(**validated_data)
        return self.repository.send_req(friendship_req)

    def accept_request(self, req_id: uuid.UUID, main_user : uuid.UUID , user_id: uuid.UUID):
        return self.repository.accept(req_id, main_user, user_id)

    def reject_request(self, req_id: uuid.UUID):
        return self.repository.reject(req_id)

    def get_friend_list(self, user_id: uuid.UUID) -> Tuple[List[Friend], str]:
        return self.repository.list_friends(user_id)

    def get_friendship_requests(self, user_id: uuid.UUID) -> Tuple[List[FriendRequest], str]:
        return self.repository.list_requests(user_id)


