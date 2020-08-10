from django.contrib.auth.models import User


def create_username(user_data):
    found = False
    added_number = 1
    while not found:
        new_username = user_data['first_name'] + user_data['last_name'] + str(added_number)
        if User.objects.filter(username=new_username).exists():
            added_number += 1
            continue
        else:
            return new_username

