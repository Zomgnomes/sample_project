from django.contrib import admin

from .models import ExampleDataDaily


class ExampleDataDailyAdmin(admin.ModelAdmin):
    list_display = ["id", "related_id", "date", "red", "green", "blue", "nir"]
    search_fields = ["id", "related_id", "date", "red", "green", "blue", "nir"]
    ordering = ["related_id", "date"]


admin.site.register(ExampleDataDaily, ExampleDataDailyAdmin)
