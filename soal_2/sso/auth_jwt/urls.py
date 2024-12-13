from django.urls import path
from .views import GenerateAccessToken, GenerateAccessTokenFromRefreshToken

urlpatterns = [
    path('token/', GenerateAccessToken.as_view()),
    path('refresh/', GenerateAccessTokenFromRefreshToken.as_view()),
]
