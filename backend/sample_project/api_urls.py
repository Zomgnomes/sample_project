from apps.data.urls import router as data_router
from apps.users.urls import router as user_router
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(data_router.registry)

urlpatterns = [
    path("", include(router.urls)),
]
