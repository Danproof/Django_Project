from django.urls import path
from .consumers import TableConsumer

ws_urlpatterns = [
    path('ws/table/<int:table_id>/', TableConsumer.as_asgi())
]