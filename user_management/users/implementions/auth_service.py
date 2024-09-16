from typing import Tuple

from users.implementions.auth_repository import AuthRepositoryImpl
from users.interface.auth_service import AuthService
from users.utils import JWTUtils


class AuthServiceImpl(AuthService):
    def __init__(self, auth_repository: AuthRepositoryImpl):
        self.auth_repository = auth_repository

    def login(self, validated_data: dict) -> Tuple[str, bool]:
        username = validated_data.get('username')
        password = validated_data.get('password')
        return self.auth_repository.login(username, password)

    def validate_token(self, token):
        try:
            JWTUtils.decode_token(token)
            return True, "Successfully logged in."
        except Exception as e:
            return False, str(e)
