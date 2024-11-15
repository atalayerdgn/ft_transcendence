import jwt  # JSON Web Token (JWT) modülü, token'ı çözümlemek ve doğrulamak için kullanılır
from django.conf import settings  # Django ayarlarına erişim sağlamak için kullanılır (örneğin, SECRET_KEY)
from django.http import JsonResponse  # JSON formatında HTTP yanıtları döndürmek için kullanılır
import logging  # İşlem adımlarını ve hataları kaydetmek için kullanılan Python modülü

# 'apigateway' adında bir logger oluşturuluyor ve DEBUG seviyesinde log kaydediliyor
logger = logging.getLogger('apigateway')
logger.setLevel(logging.DEBUG)

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # Middleware işlemi sonrası bir sonraki işleme devam etmek için `get_response` fonksiyonu alınır

    def __call__(self, request):
        # Giriş yapılmadan erişilebilecek yolları tanımla (örneğin, login ve register gibi)
        exempt_paths = ['/users/create/', '/users/login/' , '/users/login_with_42/', '/users/oauth_callback/' , '/favicon.ico']
        if request.path in exempt_paths:
            return self.get_response(request)  # Eğer istek bu yollardan birine yapılmışsa, doğrulama yapılmadan işleme devam edilir

        # Header'dan Authorization kısmından token'ı al
        token = request.headers.get('Authorization')
        if not token:
            logger.debug('Missing token')  # Token yoksa hata mesajı loglanır
            return JsonResponse({'error': 'Missing token'}, status=401)  # 401 Unauthorized yanıtı ile kullanıcı bilgilendirilir

        try:
            # Bearer token formatında gelen token'ı "Bearer <token>" olarak ayır
            token = token.split(' ')[1]
            logger.debug('Token: %s', token) # Ayrıştırılan token'ı logla

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