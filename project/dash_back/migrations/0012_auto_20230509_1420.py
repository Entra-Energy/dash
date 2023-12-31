# Generated by Django 2.2.26 on 2023-05-09 11:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_back', '0011_auto_20230503_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='CapaAsign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dev', models.CharField(max_length=100)),
                ('capacity', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='aris',
            name='timestamp_aris',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 9, 14, 20, 19, 555816)),
        ),
        migrations.AlterField(
            model_name='flexabilitysim',
            name='scheduled',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 9, 14, 20, 19, 554817)),
        ),
        migrations.AlterField(
            model_name='flexi',
            name='response_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 9, 14, 20, 19, 554817)),
        ),
        migrations.AlterField(
            model_name='hydro',
            name='timestamp_hydro',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 9, 14, 20, 19, 556816)),
        ),
        migrations.AlterField(
            model_name='neykovo',
            name='timestamp_neykovo',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 9, 14, 20, 19, 555816)),
        ),
        migrations.AlterField(
            model_name='online',
            name='saved_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 9, 14, 20, 19, 553817)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 9, 14, 20, 19, 552816)),
        ),
        migrations.AlterField(
            model_name='postforecast',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 9, 14, 20, 19, 553817)),
        ),
        migrations.AlterField(
            model_name='price',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 9, 14, 20, 19, 554817)),
        ),
    ]
