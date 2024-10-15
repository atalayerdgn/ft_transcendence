import jwt
from django.conf import settings
from django.http import JsonResponse
import logging

# Logger ayarları
logger = logging.getLogger('apigateway')
logger.setLevel(logging.DEBUG)

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Giriş yapılmadan erişilebilecek yolları tanımla (login ve register gibi)
        exempt_paths = ['/users/create/', '/users/login/']
        if request.path in exempt_paths:
            return self.get_response(request)

        # Header'dan Authorization kısmından token'ı al
        token = request.headers.get('Authorization')
        if not token:
            logger.debug('Missing token')  # Token yoksa logla
            return JsonResponse({'error': 'Missing token'}, status=401)

        try:
            # Bearer token formatında gelen token'ı "Bearer <token>" olarak ayır
            token = token.split(' ')[1]
            logger.debug('Token: %s', token)

            # Token'ı çöz ve içindeki kullanıcı bilgilerini al
            decoded_token = jwt.decode(token, settings.USER_SECRET_KEY, algorithms=['HS256'])
            logger.debug('Decoded Token: %s', decoded_token)

            # Kullanıcı ID'sini request'e ekleyelim
            request.user_id = decoded_token['user_id']

            # Token doğrulama başarılıysa loga başarılı mesajı yazalım
            logger.debug('********** Token is valid **********')
            logger.debug('Token is valid for user_id: %s', request.user_id)
            logger.debug('Token is valid for username %s', decoded_token['username'])
            logger.debug('************************************')

        except jwt.ExpiredSignatureError:
            logger.debug('Token has expired')  # Token süresi dolmuşsa logla
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            logger.debug('Invalid token')  # Token geçersizse logla
            return JsonResponse({'error': 'Invalid token'}, status=401)
        except Exception as e:
            logger.debug('Error decoding token: %s', str(e))  # Diğer hatalar için logla
            return JsonResponse({'error': str(e)}, status=400)

        # Eğer token geçerliyse, isteği bir sonraki middleware'e gönder
        return self.get_response(request)
'''
Middleware, her gelen isteği inceleyerek önce token olup olmadığını kontrol eder.
Token varsa, JWT modülü kullanarak token'ı çözer ve içindeki bilgileri doğrular.
Token geçerliyse, kullanıcı bilgilerini request'e ekler ve isteği işleme alır.
Token geçersizse veya süresi dolmuşsa, ilgili hata mesajını döndürür ve isteği reddeder.
'''