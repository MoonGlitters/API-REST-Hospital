from django.urls import path
from . import views

urlpatterns = [
    path('doctores/', views.indexDoctores, name='doctores'),
    path('doctores/<int:id>', views.indexDoctores_id, name='doctores_id'),
    path('madres/', views.indexMadres, name='madres'),
    path('madres/<int:id>', views.indexMadres_id, name='madres_id'),
    path('partos/', views.indexPartos, name='partos'),
    path('partos/<int:id>', views.indexPartos_id, name='partos_id'),
    path('nacidos/', views.indexNacidos, name='nacidos'),
    path('nacidos/<int:id>', views.indexNacidos_id, name='nacidos_id')
]