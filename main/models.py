from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Убедитесь, что email уникален
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    USERNAME_FIELD = 'email'  # Указываем, что для аутентификации будет использоваться email
    REQUIRED_FIELDS = [
        'username']  # username по-прежнему нужен, но его не будем использовать для входа
    PROFILE_CHOICES = [
        ('company', 'Компания'),
        ('initiator', 'Заказчик-инициатор'),
    ]
    profile_type = models.CharField(
        'Тип профиля',
        max_length=20,
        choices=PROFILE_CHOICES,
        default='guest',
    )
    def __str__(self):
        return f"{self.email} ({self.get_profile_type_display()})"