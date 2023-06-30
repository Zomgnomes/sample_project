
from apps.users.urls import router as user_router
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.registry.extend(user_router.registry)

urlpatterns = [
    path('', include(router.urls)),
]
