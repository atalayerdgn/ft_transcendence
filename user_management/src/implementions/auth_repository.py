from typing import Tuple
from django.contrib.auth.hashers import check_password
from src.interface.auth_repository import AuthRepository
from src.models.models import User
from src.utils import Utils
from django.utils import timezone
import random
import datetime
import logging

# Logger'ı ayarla
logger = logging.getLogger(__name__)

class AuthRepositoryImpl(AuthRepository):
    #login methodu, kullanıcı adı ve şifre alır ve kullanıcıyı veritabanında arar
    def login(self, username: str, password: str) -> dict:
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                temp_token = self.generate_token(user, is_2fa_validated=False) #değişiklik yapıldı
                twofa_code = self.set_twofa_code(user) #eozdur
                success = self.send_2fa_code(user.email, twofa_code)#eozdur
                if not success:
                    return {'success': False, 'error': "2FA code sent but failed to deliver"}
                return {
                    'success': True,
                    'temp_token': temp_token
                }
            return {'success': False, 'error': "Wrong password"}
        except User.DoesNotExist:
            return {'success': False, 'error': "User not found"}
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return {'success': False, 'error': f"Error: {str(e)}"}

    def generate_token(self, user: User, is_2fa_validated: bool = False) -> str:
        payload = {
            'username': user.username,
            'user_id': str(user.id),
            'is_2fa_validated': is_2fa_validated
        }
        return Utils.create_token(payload)

    def generate_2fa_code(self) -> str: #eozdur
        return str(random.randint(100000, 999999))

    def set_twofa_code(self, user: User) -> str: #eozdur
        code = self.generate_2fa_code()
        user.twofa_code = code
        user.twofa_code_expiry = timezone.now() + datetime.timedelta(minutes=5)
        user.save()
        return code

    def send_2fa_code(self, email: str, code: str) -> bool: #eozdur
        logger.debug(f"Sending 2FA code {code} to {email}")
        subject = "Your 2FA Code"
        body = f"Your 2FA code is: {code}"
        #içeriği oluşturulan e-posta gönderilir
        success = Utils.send_email(email, subject, body)  # E-posta gönderme
        if success:
            logger.info("E-posta başarıyla gönderildi.")
        else:
            logger.error("E-posta gönderiminde bir hata oluştu.")
        return success

    def validate_twofa(self, user: User, twofa_code: str) -> bool: #eozdur
        try:
            if user.twofa_code == twofa_code and user.twofa_code_expiry > timezone.now():
                user.twofa_code = None
                user.twofa_code_expiry = None
                user.save()
                return True
            return False
        except Exception as e:
            #user.twofa_code logla
            logger.info(f"User 2FA code: {user.twofa_code}")
            logger.error(f"Error during 2FA validation: {str(e)}")
            return False