# Generated by Django 4.2.1 on 2023-06-29 06:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0012_ubicacion_text_alter_medio_creacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componente',
            name='tipo_capacidad',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='componente',
            name='tipo_frecuencia',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='medio',
            name='creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 29, 1, 10, 11, 768818)),
        ),
        migrations.AlterField(
            model_name='medio',
            name='modificacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 29, 1, 10, 11, 768818)),
        ),
    ]