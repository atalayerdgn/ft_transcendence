import uuid
from typing import Tuple, List

from ..interface.friend_repository import FriendRepository
from django.db import models
from ..models.models import FriendRequest, Friend


class FriendRepositoryImpl(FriendRepository):
    def create_model(self, main_user_id: uuid.UUID, user_id: uuid.UUID):
        user_one = Friend.objects.filter(user_id=main_user_id).first()
        user_one.add_friend(user_id)

        user_two = Friend.objects.filter(user_id=user_id).first()
        user_two.add_friend(main_user_id)

    def reject(self, req_id: uuid.UUID) -> Tuple[bool, str]:
        try:
            model = FriendRequest.objects.filter(req_id=req_id).first()
            model.delete()
            return True, ""
        except Exception as e:
            return False, str(e)

    def accept(self, req_id: uuid.UUID, main_user_id: uuid.UUID, user_id: uuid.UUID) -> Tuple[bool, str]:
        try:
            model = FriendRequest.objects.filter(req_id=req_id).first()
            model.delete()
            self.create_model(main_user_id, user_id)
            return True, ""
        except Exception as e:
            return False, str(e)

    def send_req(self, friendship_req: FriendRequest):
        try:
            if not FriendRequest.objects.filter(to_user_id=friendship_req.to_user_id, from_user_id = friendship_req.from_user_id).first():
                model = FriendRequest(from_user_id=friendship_req.from_user_id, to_user_id=friendship_req.to_user_id)
                model.save()
                return True, ""
            else:
                return False, ""
        except Exception as e:
            return False, str(e)

    def list_friends(self, user_id: uuid.UUID) -> Tuple[models.QuerySet, str]:
        try:
            friends = Friend.objects.filter(user_id=user_id)
            return friends, ""
        except Exception as e:
            return Friend.objects.none(), str(e)  # Boş bir QuerySet döndür

    def list_requests(self, user_id: uuid.UUID) -> Tuple[models.QuerySet, str]:
        try:
            model = FriendRequest.objects.filter(from_user_id=user_id)
            return list(model), ""
        except Exception as e:
            return [], str(e)
