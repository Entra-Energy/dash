# Generated by Django 2.2.26 on 2022-06-15 11:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_back', '0005_auto_20220615_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='online',
            name='saved_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 15, 14, 5, 46, 486789)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 15, 14, 5, 46, 486789)),
        ),
        migrations.AlterField(
            model_name='price',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 15, 14, 5, 46, 486789)),
        ),
    ]