from typing import Tuple

from src.implementions.auth_repository import AuthRepositoryImpl
from src.interface.auth_service import AuthService
from src.utils import Utils


class AuthServiceImpl(AuthService):
    def __init__(self, auth_repository: AuthRepositoryImpl):
        self.auth_repository = auth_repository

    def login(self, validated_data: dict) -> Tuple[str, bool]:
        #username ve password'u al
        username = validated_data.get('username')
        password = validated_data.get('password')
        return self.auth_repository.login(username, password)

    def validate_token(self, token):
        try:
            Utils.decode_token(token)
            return True, "Successfully logged in."
        except Exception as e:
            return False, str(e)

    def validate_twofa(self, email, twofa_code):
        #2fa kodunu kontrol et
        return self.auth_repository.validate_twofa(email, twofa_code)