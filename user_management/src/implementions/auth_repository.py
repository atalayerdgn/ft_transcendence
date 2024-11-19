from typing import Optional, Tuple
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
        
    def oauth_callback(self, user_info: dict) -> Tuple[bool, str, Optional[User]]:
        try:
            # Önce kullanıcıyı e-posta adresine göre bulmaya çalış
            user = User.objects.filter(email=user_info.get('email')).first()
            if user:
                # Kullanıcı bulunduysa bilgilerini güncelle
                user.username = user_info.get('login')
                user.first_name = user_info.get('first_name')
                user.last_name = user_info.get('last_name')
                user.save()
                return True, 'User updated successfully', user
            else:
                # Kullanıcı bulunamazsa yeni kullanıcı oluştur
                user = User.objects.create(
                    username=user_info.get('login'),
                    first_name=user_info.get('first_name'),
                    last_name=user_info.get('last_name'),
                    email=user_info.get('email')
                )
                return True, 'User created successfully', user
        except Exception as e:
            # Herhangi bir hata olursa hata mesajı ve None döndür.
            return False, f"Error updating or creating user: {str(e)}", None
        