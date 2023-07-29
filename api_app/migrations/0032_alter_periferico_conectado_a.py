# Generated by Django 4.2.1 on 2023-07-25 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0031_alter_medio_modelo_alter_periferico_conectado_a'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periferico',
            name='conectado_a',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tags', related_query_name='tag', to='api_app.medio', verbose_name='conexion'),
        ),
    ]
