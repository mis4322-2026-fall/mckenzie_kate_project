from getpass import getpass

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Create an ordinary local demonstration account using hidden password prompts."

    def handle(self, *args, **options):
        user_model = get_user_model()
        username = input("Fictional username: ").strip()
        user = user_model(username=username)
        try:
            user.full_clean(exclude=["password"])
            password = getpass("Password: ")
            if password != getpass("Password (again): "):
                raise CommandError("Passwords do not match; no account created.")
            validate_password(password, user)
            user.set_password(password)
            user.save()
        except (ValidationError, IntegrityError) as error:
            raise CommandError(str(error)) from error
        self.stdout.write(self.style.SUCCESS("Demonstration account created."))
