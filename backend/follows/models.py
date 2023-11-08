from django.db import models

from users.models import User


class Follow(models.Model):
    """Follow model."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Пользователь'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Подписчик'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow_pair',
            )
        ]
        ordering = ['user']

    def __str__(self):
        return f'{self.user.username} follows {self.following.username}'
