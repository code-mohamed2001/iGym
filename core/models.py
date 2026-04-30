from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('receptionist', 'Receptionist'),
        ('trainer', 'Trainer'),
    )
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='receptionist')
    phone = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

    @property
    def is_owner(self):
        return self.role == 'owner'

    @property
    def is_receptionist(self):
        return self.role == 'receptionist'

    @property
    def is_trainer(self):
        return self.role == 'trainer'
