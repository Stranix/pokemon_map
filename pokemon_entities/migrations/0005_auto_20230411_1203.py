# Generated by Django 3.1.14 on 2023-04-11 09:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0004_auto_20230411_1129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemon',
            old_name='parent',
            new_name='previous_evolution',
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='appeared_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 4, 11, 12, 3, 25, 15490)),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='disappeared_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 4, 11, 12, 3, 25, 15490)),
        ),
    ]
