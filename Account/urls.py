from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken


router = routers.DefaultRouter()
router.register('home', BlogUserViewSet)
# router.register('login/',ObtainAuthToken)

app_name = 'Account'

urlpatterns = [
    path('', include(router.urls)),
    path('register/', BlogUserRegisterView.as_view(), name='register'),
    path('result/', register_result, name='result'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('base/', BaseView.as_view(), name='base')
]
