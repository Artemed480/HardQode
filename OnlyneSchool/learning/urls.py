from .views import *
from django.urls import path

urlpatterns = [
    path('1', TimeStatus.as_view()),
    path('2/<int:pk>', ProductApi.as_view()),
    path('3', StatisticApi.as_view())
]
