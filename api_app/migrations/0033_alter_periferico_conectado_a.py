# Generated by Django 4.2.1 on 2023-07-25 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0032_alter_periferico_conectado_a'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periferico',
            name='conectado_a',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', related_query_name='tag', to='api_app.medio', verbose_name='conexion'),
        ),
    ]
