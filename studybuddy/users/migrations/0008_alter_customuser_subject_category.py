# Generated by Django 5.1.7 on 2025-04-01 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_customuser_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='subject_category',
            field=models.CharField(blank=True, choices=[('mathematics', 'Mathematics'), ('science', 'Science'), ('history', 'History'), ('english', 'English'), ('computers', 'Computer Science'), ('arts', 'Arts')], default='mathematics', max_length=20, null=True),
        ),
    ]
