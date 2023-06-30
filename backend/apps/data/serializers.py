from rest_framework import serializers

from .models import ExampleDataDaily


class ExampleDataDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleDataDaily
        fields = "__all__"
