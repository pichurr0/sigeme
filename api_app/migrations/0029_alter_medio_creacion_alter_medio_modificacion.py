# Generated by Django 4.2.1 on 2023-07-21 04:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0028_alter_medio_creacion_alter_medio_modificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medio',
            name='creacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='medio',
            name='modificacion',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
