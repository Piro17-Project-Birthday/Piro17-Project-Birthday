# Generated by Django 4.1 on 2022-08-12 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tmies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmimessage',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]