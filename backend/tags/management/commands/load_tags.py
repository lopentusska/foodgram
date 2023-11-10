import csv

from django.core.management.base import BaseCommand

from tags.models import Tag


class Command(BaseCommand):
    """Custom Command class to load tags."""
    path = './data/tags.csv'

    def handle(self, *args, **options):
        with open(self.path) as f:
            reader = csv.reader(f)
            for row in reader:
                if Tag.objects.filter(
                    name=row[0],
                    color=row[1],
                    slug=row[2]
                ).first():
                    print(f'Tag {row[0]} already exists.')
                else:
                    print(row[0], row[1], row[2])
                    Tag.objects.create(
                        name=row[0],
                        color=row[1],
                        slug=row[2]
                    )
