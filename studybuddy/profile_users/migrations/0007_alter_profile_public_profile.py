# Generated by Django 5.1.7 on 2025-03-29 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_users', '0006_alter_profile_public_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='public_profile',
            field=models.BooleanField(default=True),
        ),
    ]
