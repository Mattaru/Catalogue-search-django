from django.urls import path

from catalog.views import CarList

app_name = 'catalog'

urlpatterns = [
    path('cars/', CarList.as_view(), name='car-list'),
]