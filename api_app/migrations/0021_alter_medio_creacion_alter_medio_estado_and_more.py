# Generated by Django 4.2.1 on 2023-07-08 05:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0020_alter_medio_creacion_alter_medio_modificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medio',
            name='creacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 8, 0, 14, 45, 827828)),
        ),
        migrations.AlterField(
            model_name='medio',
            name='estado',
            field=models.CharField(choices=[('bien', 'Bien'), ('reparacion', 'Reparacion'), ('roto', 'Roto')], default='bien', max_length=21),
        ),
        migrations.AlterField(
            model_name='medio',
            name='modificacion',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 8, 0, 14, 45, 827828)),
        ),
        migrations.DeleteModel(
            name='TipoEstadoMedio',
        ),
    ]