# Generated by Django 3.2.3 on 2023-10-14 11:43

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients_label', '0002_auto_20231014_1143'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes_label', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='users_label.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(default=None, validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='ingredients_label.IngredientQuantity', to='ingredients_label.Ingredient'),
        ),
    ]
