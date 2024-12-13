import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sso.settings') 
django.setup()

from django.contrib.auth.models import User

users_data = [
    {'username': 'user1', 'email': 'user1@example.com', 'password': 'password1'},
    {'username': 'user2', 'email': 'user2@example.com', 'password': 'password2'},
    {'username': 'user3', 'email': 'user3@example.com', 'password': 'password3'},
]

def create_user():
    for user_data in users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            print(f"User '{user_data['username']}' created.")
        else:
            print(f"User '{user_data['username']}' already exists.")

if __name__ == '__main__':
    create_user()
