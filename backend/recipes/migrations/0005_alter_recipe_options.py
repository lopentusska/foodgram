# Generated by Django 3.2.3 on 2023-10-17 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes_label', '0004_alter_recipe_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['created']},
        ),
    ]
