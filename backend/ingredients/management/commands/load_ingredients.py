import csv

from django.core.management.base import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):
    """Custom Command class to load ingredients."""
    path = './data/ingredients.csv'

    def handle(self, *args, **options):
        with open(self.path) as f:
            reader = csv.reader(f)
            for row in reader:
                if Ingredient.objects.filter(
                        name=row[0],
                        measurement_unit=row[1]
                ).first():
                    print(f'Ingredients {row[0]} already exists.')
                else:
                    print(row[0], row[1])
                    Ingredient.objects.create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
