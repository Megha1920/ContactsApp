# contacts/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
def validate_phone_numbers(phone_numbers):
    for number in phone_numbers.split(','):
        number = number.strip()
        if not number.isdigit():
            raise ValidationError(f"Phone number '{number}' contains non-numeric characters.")
        if len(number) != 10:
            raise ValidationError(f"Phone number '{number}' must be exactly 10 digits long.")

class Contact(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.TextField()
    company = models.CharField(max_length=100)
    phone_numbers = models.TextField(validators=[validate_phone_numbers])  # Store multiple phone numbers as comma-separated string

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

