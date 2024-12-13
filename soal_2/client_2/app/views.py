from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from .validateJWT import validateJwt

class ValidateJWTAndFetchUserDetails(APIView):
    def post(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            validateJwt(auth_header)

            return JsonResponse({"data":"authenticated to client 2"}, status=200)
        except TokenError as e:
            print(e)
            return JsonResponse({'error': f'Invalid token: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
