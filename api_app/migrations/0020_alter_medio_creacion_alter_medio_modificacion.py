# Generated by Django 4.2.1 on 2023-07-05 07:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0019_alter_computadora_ip_alter_medio_creacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medio',
            name='creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 5, 2, 41, 20, 140056)),
        ),
        migrations.AlterField(
            model_name='medio',
            name='modificacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 5, 2, 41, 20, 140056)),
        ),
    ]
