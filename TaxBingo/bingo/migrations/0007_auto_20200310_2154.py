# Generated by Django 2.2.4 on 2020-03-10 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingo', '0006_auto_20200310_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='bingos',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='board',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]