from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import F, Q


class UserRole:
    USER = 'user'
    ADMIN = 'admin'
    choices = [
        (USER, 'USER'),
        (ADMIN, 'ADMIN')
    ]


class User(AbstractUser):
    """Модель пользователей."""
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        verbose_name='Username'
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.TextField(max_length=150, blank=True)
    last_name = models.TextField(max_length=150, blank=True)
    role = models.TextField(
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name='Пользовательская роль'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow',
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='self_following',
            ),
        )
