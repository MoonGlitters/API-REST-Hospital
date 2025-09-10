from django.urls import path
from . import views

urlpatterns = [
    path('madres', views.est_madres, name='est_madres'),
    path('partos', views.est_partos, name='est_partos'),
    path('nacidos', views.est_nacidos, name='est_nacidos')
]