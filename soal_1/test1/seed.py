import os
import django
from datetime import datetime
from random import choice, randint
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test1.settings")
django.setup()

from user.models import User

fake = Faker()

def generate_fake_users(number_of_users):
    for _ in range(number_of_users):
        firstname = fake.first_name()
        lastname = fake.last_name()
        nickname = fake.user_name()
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)
        is_active = True

        user = User(
            firstname=firstname,
            lastname=lastname,
            nickname=nickname,
            date_of_birth=date_of_birth,
            is_active=is_active
        )
        user.save()

        print(f"User {nickname} created successfully!")

generate_fake_users(10)
