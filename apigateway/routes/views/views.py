# APIView sınıfı, Django Rest Framework'te temel bir görünümdür. HTTP yöntemlerini (GET, POST, PUT, DELETE vb.) yönetir.
from rest_framework.views import APIView
# GatewayServiceImpl, API Gateway iş mantığını içerir.
from ..implementions.gateway_service import GatewayServiceImpl
# GatewayRepositoryImpl, veri erişim katmanını temsil eder.
from ..implementions.gateway_repository import GatewayRepositoryImpl

# API Gateway için bir görünüm sınıfı tanımlıyoruz.
class APIGatewayView(APIView):
    def __init__(self, **kwargs):
        # Üst sınıfın (__init__ metodu) başlatılmasını sağlar.
        super().__init__(**kwargs)
        # GatewayServiceImpl, repository (veri erişim katmanı) bağımlılığı ile başlatılıyor.
        self.service = GatewayServiceImpl(GatewayRepositoryImpl())

    # HTTP GET isteklerini işler.
    def get(self, request, path):
        # İsteği servis katmanına yönlendirir.
        return self.service.process_request(request, path)

    # HTTP POST isteklerini işler.
    def post(self, request, path):
        return self.service.process_request(request, path)

    # HTTP PUT isteklerini işler.
    def put(self, request, path):
        return self.service.process_request(request, path)

    # HTTP PATCH isteklerini işler.
    def patch(self, request, path):
        return self.service.process_request(request, path)

    # HTTP DELETE isteklerini işler.
    def delete(self, request, path):
        return self.service.process_request(request, path)
