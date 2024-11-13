import requests
import uuid
from typing import Tuple, List
from venv import logger


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
    
    def user_exists(self, user_id: uuid.UUID) -> bool:
        logger.error(f"Checking if user exists with user_id: {user_id}")
        response = requests.get(f"http://usermanagementc:8000/users/id/?id={user_id}")
        logger.error(f"rRRRRRRRRRRRRRRRRRRRRRRRResponse: {response.json()}")
        if response.status_code == 200:
            return True
        return False

