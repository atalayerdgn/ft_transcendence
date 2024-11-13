from typing import Tuple
from django.contrib.auth.hashers import check_password
from src.interface.auth_repository import AuthRepository
from src.models.models import User
from src.utils import Utils
from django.utils import timezone
import logging

# Logger'ı ayarla
logger = logging.getLogger(__name__)

class AuthRepositoryImpl(AuthRepository):
    #login methodu, kullanıcı adı ve şifre alır ve kullanıcıyı veritabanında arar
    def login(self, username: str, password: str) -> dict:
        try:
            user = User.objects.get(username=username) # Kullanıcıyı veritabanından al
            if check_password(password, user.password): # Şifre doğruysa
                return user  # Doğru kullanıcı döndürülür
            return None  # Şifre yanlışsa None döndür
        except User.DoesNotExist:
            return None  # Kullanıcı bulunamazsa None döndür
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return None  # Hata durumunda None döndür

    def validate_twofa(self, user: User) -> None:
        try:
            user.is_online = True # Kullanıcıyı çevrimiçi yap
            user.save() # Kullanıcıyı veritabanına kaydet
        except Exception as e:
            logger.error(f"Error during 2FA validation: {str(e)}")
            raise e
        
    def get_user_by_id(self, user_id: int) -> User:
        try:
            return User.objects.get(id=user_id)  # Kullanıcıyı veritabanından al
        except User.DoesNotExist:
            return None  # Kullanıcı bulunamazsa None döndür
        except Exception as e:
            logger.error(f"Error during user retrieval: {str(e)}")
            return None  # Hata durumunda None döndür
        