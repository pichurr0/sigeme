# Generated by Django 4.2.1 on 2023-07-01 23:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0015_alter_medio_creacion_alter_medio_modificacion_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='medio',
            name='api_medio_marca_i_9992c2_idx',
        ),
        migrations.AlterField(
            model_name='medio',
            name='creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 1, 18, 2, 11, 669942)),
        ),
        migrations.AlterField(
            model_name='medio',
            name='modificacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 1, 18, 2, 11, 669942)),
        ),
    ]
