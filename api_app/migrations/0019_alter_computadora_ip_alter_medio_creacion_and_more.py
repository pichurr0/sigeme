# Generated by Django 4.2.1 on 2023-07-02 23:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0018_tiposistemaoperativo_version_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computadora',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='medio',
            name='creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 2, 18, 53, 38, 350305)),
        ),
        migrations.AlterField(
            model_name='medio',
            name='modificacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 2, 18, 53, 38, 350305)),
        ),
    ]
