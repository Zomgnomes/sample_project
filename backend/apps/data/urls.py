from rest_framework import routers

from .views import ExampleDataViewSet

# Users API
router = routers.DefaultRouter()
router.trailing_slash = "/?"

router.register(r"data", ExampleDataViewSet)
