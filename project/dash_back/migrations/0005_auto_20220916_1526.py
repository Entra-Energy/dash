# Generated by Django 2.2.26 on 2022-09-16 12:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_back', '0004_auto_20220915_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hydro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_hydro', models.DateTimeField(default=datetime.datetime(2022, 9, 16, 15, 26, 57, 760575))),
                ('hydro_pow', models.FloatField()),
                ('guide_vains', models.FloatField()),
                ('level', models.FloatField()),
                ('gen_temp', models.FloatField()),
                ('gen_curr', models.FloatField()),
                ('gen_vol', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='aris',
            name='timestamp_aris',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 16, 15, 26, 57, 759577)),
        ),
        migrations.AlterField(
            model_name='flexabilitysim',
            name='scheduled',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 16, 15, 26, 57, 759577)),
        ),
        migrations.AlterField(
            model_name='flexi',
            name='response_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 16, 15, 26, 57, 758587)),
        ),
        migrations.AlterField(
            model_name='neykovo',
            name='timestamp_neykovo',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 16, 15, 26, 57, 760575)),
        ),
        migrations.AlterField(
            model_name='online',
            name='saved_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 16, 15, 26, 57, 757580)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 16, 15, 26, 57, 756590)),
        ),
        migrations.AlterField(
            model_name='price',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 16, 15, 26, 57, 758587)),
        ),
        migrations.AlterField(
            model_name='userip',
            name='user_ip',
            field=models.CharField(max_length=900),
        ),
    ]