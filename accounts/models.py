from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField(
        max_length=254,
        unique=True
    )
    phone_number = models.CharField(
        max_length=12,
        unique=True
    )
    bonuses = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class BonusTransaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bonus_transactions'
    )
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_awarded = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        permissions = [
            ("can_redeem_bonus", "Can redeem bonus orders"),
        ]
    def __str__(self):
        return f"{self.bonus_awarded} бонусів користувачу {self.user.email} — {self.created_at:%Y-%m-%d %H:%M}"