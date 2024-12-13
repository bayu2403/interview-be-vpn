from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken

def validateJwt(auth_header):
  if not auth_header or not auth_header.startswith("Bearer "):
      return JsonResponse({'error': 'Authentication credentials were not provided.'}, status=401)

  token_str = auth_header.split(" ")[1]
  token = AccessToken(token_str)
  return token