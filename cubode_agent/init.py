import os
import django
from django.contrib.auth import get_user_model
django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

from django.conf import settings

User = get_user_model()


def activateUser(user, password='cubode1234'):
    user.set_password(password)
    user.is_verified = True
    user.is_active = True
    user.save()
    print(f"User Activated: {user.username}, {user.is_verified} {user.email}")


def activateProUser(user, password='cubode1234'):
    user.set_password(password)
    user.is_verified = True
    user.is_active = True
    user.is_member_pro = True
    user.save()
    print(f"User Activated: {user.username}, {user.is_verified} {user.email}")


def activateEnterpriceUser(user, password='cubode1234'):
    user.set_password(password)
    user.is_verified = True
    user.is_active = True
    user.is_enterprise_member = True
    user.save()
    print(f"User Activated: {user.username}, {user.is_verified} {user.email}")


def initUsers():
    if not settings.DEVELOPMENT:
        return

    print("\n\nUsers Initializing\n")
    admin_user = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'cubode.admin')
    admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL',
                                 'cubode.dev.admin@cubode.com')
    admin_pass = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'cubode1234')

    if not User.objects.filter(username=admin_email).exists() and not User.objects.filter(email=admin_email).exists():
        User.objects.create_superuser(admin_user,admin_email,admin_pass)
        print(f"SuperUser Activated: {admin_email}")

    davide = User.objects.get_or_create(username='davide.dev', email='davide.dev@cubode.com')
    david = User.objects.get_or_create(username='david.dev', email='david.dev@cubode.com')
    ben = User.objects.get_or_create(username='ben.dev', email='ben.dev@cubode.com')
    proUser=User.objects.get_or_create(username='userPro', email='pro.dev@ciao.com')
    enterpriceUser=User.objects.get_or_create(username='userEnter', email='enter.dev@hola.com')

    activateUser(davide[0], password='cubode1234')
    activateUser(david[0], password='cubode1234')
    activateUser(ben[0], password='cubode1234')
    activateProUser(proUser[0], password='cubode1234')
    activateEnterpriceUser(enterpriceUser[0], password='cubode1234')
    print("\n\nDevelopment: Users Initialized\n")


if __name__ == "__main__":
    initUsers()
