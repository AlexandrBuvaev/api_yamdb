# Generated by Django 2.2.16 on 2022-10-13 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0004_auto_20221013_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorie',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]