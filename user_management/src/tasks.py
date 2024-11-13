from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User


@shared_task
def check_inactive_users():
    # 1 dakikadan uzun süredir heartbeat göndermeyen kullanıcıları offline yap
    threshold = timezone.now() - timedelta(minutes=1)
    User.objects.filter(
        last_heartbeat__lt=threshold, 
        is_online=True
    ).update(is_online=False)