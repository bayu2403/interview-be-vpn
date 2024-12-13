from django.urls import path
from . import views

urlpatterns = [
    path('v1/create-user/', views.create_user),
    path('v1/validate-user/', views.validate_user),
]
