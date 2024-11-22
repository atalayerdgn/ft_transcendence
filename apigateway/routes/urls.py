# Django'nun admin paneli için gerekli modülü içe aktarır
from django.contrib import admin

# Django'nun URL yönlendirme işlevleri için gerekli modülleri içe aktarır
from django.urls import include, path

# API Gateway işlevselliğini sağlamak için önceden tanımlanmış view'i içe aktarır

from .views.views import APIGatewayView
# URL yönlendirmelerini tanımlamak için bir liste oluşturur
urlpatterns = [
    # Dinamik olarak API Gateway'e giden URL yolu
    # '<path:path>' ifadesi, dinamik bir URL tanımı yapar. Bu ifade, 
    # URL'nin geri kalan kısmını yakalar ve 'path' adlı bir değişkene atar.
    # Örneğin, '/users/create/' veya '/products/list/' gibi URL'ler bu yol tarafından işlenir.
    path('<path:path>', APIGatewayView.as_view(), name='api_gateway'),  # Dinamik path
]
