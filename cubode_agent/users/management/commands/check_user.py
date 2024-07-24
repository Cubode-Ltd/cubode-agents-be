from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Check if a user exists'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username to check')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'User "{username}" exists'))
        else:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist'))