# Generated by Django 4.2.1 on 2023-07-28 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0038_componente_tipo_ram'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TipoComponente',
        ),
        migrations.AlterField(
            model_name='componente',
            name='tipo_ram',
            field=models.CharField(choices=[('ddr1', 'Ddr1'), ('ddr2', 'Ddr2'), ('ddr3', 'Ddr3'), ('ddr4', 'Ddr4')], max_length=200, null=True),
        ),
    ]