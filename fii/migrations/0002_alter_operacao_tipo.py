# Generated by Django 4.0.6 on 2022-07-25 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fii', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operacao',
            name='tipo',
            field=models.CharField(choices=[('C', 'Compra'), ('V', 'Venda'), ('D', 'Desdobramento'), ('S', 'Subscrição')], max_length=1),
        ),
    ]