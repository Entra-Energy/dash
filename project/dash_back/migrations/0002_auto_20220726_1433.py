# Generated by Django 2.2.26 on 2022-07-26 11:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_back', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlexabilitySim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provided_dev', models.CharField(max_length=300)),
                ('scheduled', models.DateTimeField(default=datetime.datetime(2022, 7, 26, 14, 33, 57, 221677))),
                ('sched_pow', models.FloatField()),
                ('sched_durration', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='flexi',
            name='response_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 26, 14, 33, 57, 220678)),
        ),
        migrations.AlterField(
            model_name='online',
            name='saved_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 26, 14, 33, 57, 220678)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 26, 14, 33, 57, 219677)),
        ),
        migrations.AlterField(
            model_name='price',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 26, 14, 33, 57, 220678)),
        ),
    ]
