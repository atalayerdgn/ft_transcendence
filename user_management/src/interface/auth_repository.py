from abc import abstractmethod

from src.models.models import User


class AuthRepository:
    def __init__(self):
        super().__init__()

    @abstractmethod
    def login(self, username, password):
        pass

    @abstractmethod
    def generate_token(self, user : User) -> str:
        pass
    
    @abstractmethod
    def generate_2fa_code(self) -> str:
        pass
    
    @abstractmethod
    def set_twofa_code(self, user : User) -> str:
        pass
    
    @abstractmethod
    def send_2fa_code(self, email : str, code : str) -> bool:
        pass
    
    