# Generated by Django 4.1 on 2022-08-21 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TmiPage',
            fields=[
                ('tmi_origin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='posts.birthdaypage')),
                ('year', models.IntegerField(null=True)),
                ('state', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TmiMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('like', models.IntegerField(default=0)),
                ('like_state', models.BooleanField(default=False, verbose_name='게시글좋아요')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tmies.tmipage')),
            ],
        ),
    ]
