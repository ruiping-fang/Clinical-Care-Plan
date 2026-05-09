from django.urls import path
from .views import index, generate_careplan

urlpatterns = [
    path('', index),
    path('generate/', generate_careplan),
]