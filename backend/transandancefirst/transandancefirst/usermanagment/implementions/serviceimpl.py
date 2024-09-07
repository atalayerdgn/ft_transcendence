from typing import Tuple, List
from uuid import UUID

from transandancefirst.usermanagment.interface.user_repository import UserRepository
from transandancefirst.usermanagment.interface.user_service import UserService
from .repositoryimpl import UserRepositoryImpl
from ..models.models import User
from ..serializers.serializers import UserSerializer, UserSerializer


class UserServiceImpl(UserService):
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: UUID) -> Tuple[User, str]:
        user, message = self.user_repository.get_by_id(user_id)
        return user, message

    def get_user_by_username(self, username: str) -> Tuple[User, str]:
        return self.user_repository.get_by_username(username)

    def get_user_by_email(self, email: str) -> Tuple[User, str]:
        return self.user_repository.get_by_email(email)

    def create_user(self, validated_data : dict) -> Tuple[bool, str]:
        user = User(**validated_data)
        return self.user_repository.create(user)

    def delete_user(self, user_id: UUID) -> Tuple[bool, str]:
        return self.user_repository.delete_user(user_id)

    def get_all_users(self) -> Tuple[List[User],str]:
        return self.user_repository.get_all()

