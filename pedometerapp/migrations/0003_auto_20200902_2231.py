# Generated by Django 3.1 on 2020-09-02 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedometerapp', '0002_auto_20200902_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steps',
            name='steps',
            field=models.IntegerField(unique_for_date='created_at'),
        ),
    ]
