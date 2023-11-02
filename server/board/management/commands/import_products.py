import csv
from django.core.management.base import BaseCommand
from board.models import Product


class Command(BaseCommand):
    help = 'Load a list of products from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The CSV file path')

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file_path']

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # 첫 번째 라인(헤더)을 건너뜁니다.
            for row in reader:
                Product.objects.create(
                    name=row[0],
                    url=row[1],
                    image_url=row[2],
                    price=row[3]
                )
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded products from {file_path}'))
