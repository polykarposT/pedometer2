# Generated by Django 3.1 on 2020-09-02 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedometerapp', '0003_auto_20200902_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steps',
            name='created_at',
            field=models.DateField(unique=True),
        ),
    ]
