from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('', BlogPostView)

urlpatterns = [
    path('', include(router.urls)),
    path('list', BlogListView.as_view()),
    path('category/parents/<str:category_slug>', get_parents),
    path('category/children/<str:category_slug>', get_children),
]
