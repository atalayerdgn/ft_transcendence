
from django.urls import path, include

from .views.views import FriendServiceHandler

urlpatterns = [
    path('send-request/', FriendServiceHandler.as_view({'post': 'send_request'}), name='send-request'),
    path('accept-request/', FriendServiceHandler.as_view({'post': 'accept_request'}), name='accept-request'),
    path('reject-request/', FriendServiceHandler.as_view({'post': 'reject_request'}), name='reject-request'),
    path('friend-list/', FriendServiceHandler.as_view({'get': 'get_friend_list'}), name='friend-list'),
    path('friendship-requests/', FriendServiceHandler.as_view({'get': 'get_friendship_requests'}), name='friendship-requests'),
]