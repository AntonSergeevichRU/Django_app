# Generated by Django 4.2 on 2023-08-18 11:15

from django.db import migrations, models
import my_auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(null=True, upload_to=my_auth.models.user_avatar_directory_path),
        ),
    ]