# Generated by Django 4.2.1 on 2023-06-22 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0004_alter_componente_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='computadora',
            name='es_servidor',
            field=models.BooleanField(default=False),
        ),
    ]
