# Generated by Django 2.2.26 on 2023-09-26 12:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_back', '0014_auto_20230612_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='postforecast',
            name='mean_abs_error',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='postforecast',
            name='model_loss',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='aris',
            name='timestamp_aris',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 26, 15, 24, 16, 760715)),
        ),
        migrations.AlterField(
            model_name='flexabilitysim',
            name='scheduled',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 26, 15, 24, 16, 759714)),
        ),
        migrations.AlterField(
            model_name='flexi',
            name='response_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 26, 15, 24, 16, 759714)),
        ),
        migrations.AlterField(
            model_name='hydro',
            name='timestamp_hydro',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 26, 15, 24, 16, 761714)),
        ),
        migrations.AlterField(
            model_name='neykovo',
            name='timestamp_neykovo',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 26, 15, 24, 16, 760715)),
        ),
        migrations.AlterField(
            model_name='online',
            name='saved_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 26, 15, 24, 16, 758716)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 26, 15, 24, 16, 757715)),
        ),
        migrations.AlterField(
            model_name='postforecast',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 26, 15, 24, 16, 758716)),
        ),
        migrations.AlterField(
            model_name='postforecastmonth',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 26, 15, 24, 16, 758716)),
        ),
        migrations.AlterField(
            model_name='price',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 26, 15, 24, 16, 759714)),
        ),
    ]
