<<<<<<< HEAD
<<<<<<< HEAD
# Generated by Django 4.1 on 2022-08-15 12:21
=======
# Generated by Django 4.1 on 2022-08-15 14:49
>>>>>>> yeonseo0814
=======
# Generated by Django 4.1 on 2022-08-14 03:35
>>>>>>> dongheon0814

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
=======
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
>>>>>>> dongheon0814
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='birthdaypage',
            name='owner',
<<<<<<< HEAD
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
=======
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
>>>>>>> dongheon0814
        ),
    ]
