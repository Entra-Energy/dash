# Generated by Django 2.2.26 on 2022-08-01 08:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_back', '0002_auto_20220726_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aris',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power_aris', models.FloatField()),
                ('timestamp_aris', models.DateTimeField(default=datetime.datetime(2022, 8, 1, 11, 19, 32, 748066))),
                ('wind_aris', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Neykovo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power_neykovo', models.FloatField()),
                ('timestamp_neykovo', models.DateTimeField(default=datetime.datetime(2022, 8, 1, 11, 19, 32, 749064))),
                ('wind_neykovo', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='flexabilitysim',
            name='scheduled',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 1, 11, 19, 32, 747065)),
        ),
        migrations.AlterField(
            model_name='flexi',
            name='response_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 1, 11, 19, 32, 747065)),
        ),
        migrations.AlterField(
            model_name='online',
            name='saved_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 1, 11, 19, 32, 745064)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 1, 11, 19, 32, 745064)),
        ),
        migrations.AlterField(
            model_name='price',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 1, 11, 19, 32, 746065)),
        ),
    ]
