from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

class GenerateAccessToken(APIView):
    permission_classes = [AllowAny]  # No authentication required

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        
        refresh_token = RefreshToken.for_user(user)

        return JsonResponse({'access_token': str(refresh_token.access_token), 'refresh_token': str(refresh_token)})

class GenerateAccessTokenFromRefreshToken(APIView):
    permission_classes = [AllowAny]  # No authentication required

    def post(self, request):
        refresh = request.POST.get('refresh_token')
        try:
            token = RefreshToken(refresh)

            user = User.objects.get(id=int(token.payload.get('user_id')))
            new_token = RefreshToken.for_user(user)
            
            access_token = str(new_token.access_token)
            new_refresh_token = str(new_token)
            
            if hasattr(token, 'blacklist'):
                token.blacklist()

            return JsonResponse({'access_token': access_token, 'refresh_token': new_refresh_token})

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Invalid refresh token'}, status=400)