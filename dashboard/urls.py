from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashhome, name='dashboard'),
    path('updateorder', views.updateorder, name='updateorder')
]