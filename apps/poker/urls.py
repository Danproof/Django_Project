from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='poker-home'),
    path('demo/', views.demo, name='poker-demo'),
    path('1/', views.one, name='1'),
    path('2/', views.one, name='2'),
    path('new_game/', views.new_game, name='poker-new-game'),
    path('table<int:table_id>/', views.table, name='poker-table'),

]