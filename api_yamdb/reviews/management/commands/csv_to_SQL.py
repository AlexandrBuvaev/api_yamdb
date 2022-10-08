import csv
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creating model objects according the file path specified'
    data = os.listdir(path='./static/data')

    def handle(self, *args):
        for file in self.data:
            with open(file, 'r') as csv_file:
                name_file = file.split('.')[0]
                model = name_file.title
                reader = csv.reader(csv_file, delimiter=',', quotechar='|')
                header = reader.next()
                for row in reader:
                    _object_dict = {key: value for key,
                                    value in zip(header, row)}
                    model.objects.create(**_object_dict)
