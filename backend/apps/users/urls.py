from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet

# Users API
router = routers.DefaultRouter()
router.trailing_slash = '/?'

router.register(r'users', UserViewSet)

