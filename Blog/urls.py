from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('', BlogPostView)

urlpatterns = [
    path('', include(router.urls)),
    path('list', BlogListView.as_view())
]
