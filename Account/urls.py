from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register('home', BlogUserViewSet)

app_name = 'Account'

urlpatterns = [
    path('', include(router.urls)),
    path('register/', BlogUserRegisterView.as_view()),
    path('result/', register_result, name='result'),
    path('login/', obtain_auth_token, name='login')
]