# Generated by Django 5.1.7 on 2025-03-29 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profile_users', '0007_alter_profile_public_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='shared_notes',
        ),
    ]
