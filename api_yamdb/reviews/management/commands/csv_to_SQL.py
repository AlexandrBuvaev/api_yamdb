import csv
import os


from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Creating model objects according the file path specified'
<<<<<<< HEAD
    data = os.listdir(path='static/data')
    title_app_models = ['Genre', 'Titles', 'Categorie', 'Title_genre']
    review_app_models = ['Review', 'Comment']
    user_app_models = ['User', ]

=======

    data = os.listdir(path='static/data')
    title_app_models = ['Genre', 'Titles', 'Categorie', 'Title_genre']
    review_app_models = ['Review', 'Comment']
    user_app_models = ['User', ]

>>>>>>> 685de7723df4e0ee82884088addfdb42b450a03e
    def handle(self, *args, **options):
        for file in self.data:
            with open(f'static/data/{file}', encoding='utf-8') as csv_file:
                name_file = file.split('.')[0]
                app_label = ''
                if name_file.title() in self.user_app_models:
                    app_label = 'users'
                elif name_file.title() in self.review_app_models:
                    app_label = 'reviews'
                else:
                    app_label = 'titles'
                    print(name_file)
                model = apps.get_model(
                    app_label=app_label, model_name=name_file.title())
                reader = csv.reader(csv_file, delimiter=',', quotechar='"',
                                    skipinitialspace=True)
                header = next(reader)
                for row in reader:
                    print(row)
                    _object_dict = {key: value for key,
                                    value in zip(header, row)}
                    model.objects.create(**_object_dict)
