<<<<<<< Updated upstream
# Generated by Django 4.1 on 2022-08-08 14:45
=======
# Generated by Django 4.1 on 2022-08-09 10:48
>>>>>>> Stashed changes

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< Updated upstream
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
=======
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
>>>>>>> Stashed changes
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
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]