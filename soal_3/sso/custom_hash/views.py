from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
import json
from .custom_hasher import CustomPBKDF2PasswordHasher

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        project_name = data.get('project_name')

        if not username or not password or not project_name:
            return JsonResponse({'status': 'failure', 'message': 'Missing required fields.'}, status=400)

        if CustomUser.objects.filter(username=username, project_name=project_name).exists():
            return JsonResponse({'status': 'success', 'message': 'User already exists.'}, status=200)

        try:
            hasher = CustomPBKDF2PasswordHasher()
            hasher.project_name = project_name
            hashed_password = hasher.encode(password, salt='static_salt')

            user = CustomUser.objects.create(username=username, password=hashed_password, project_name=project_name)
            return JsonResponse({'status': 'success', 'message': 'User created successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'failure', 'message': str(e)}, status=500)


@csrf_exempt
def validate_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        project_name = data.get('project_name')

        if not username or not password or not project_name:
            return JsonResponse({'status': 'failure', 'message': 'Missing required fields.'}, status=400)

        try:
            user = CustomUser.objects.get(username=username, project_name=project_name)
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'failure', 'message': 'User not found.'}, status=404)

        try:
            hasher = CustomPBKDF2PasswordHasher()
            hasher.project_name = project_name
            if hasher.verify(password, user.password):
                return JsonResponse({'status': 'success', 'message': 'Password validated successfully.'})
            else:
                return JsonResponse({'status': 'failure', 'message': 'Invalid password.'})
        except Exception as e:
            return JsonResponse({'status': 'failure', 'message': str(e)}, status=500)
