from django.db import models


class Tag(models.Model):
    """Tag model."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Таг',
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
