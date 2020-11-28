from django.contrib import admin

from catalog.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


