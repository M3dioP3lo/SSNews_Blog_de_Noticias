import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings')
django.setup()

from django.contrib.auth.models import User
from home.models import Profile

def create_profiles():
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)
        print(f"Profile created for {user.username}")

if __name__ == "__main__":
    create_profiles()