# Generated by Django 5.1.7 on 2025-03-29 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_users', '0005_follow_status_alter_follow_follower_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='public_profile',
            field=models.BooleanField(default=False),
        ),
    ]
