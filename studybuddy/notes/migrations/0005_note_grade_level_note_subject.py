# Generated by Django 4.2.19 on 2025-03-22 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_remove_note_shared_with'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='grade_level',
            field=models.CharField(choices=[('Grade 1', 'Grade 1'), ('Grade 2', 'Grade 2'), ('Grade 3', 'Grade 3'), ('Grade 4', 'Grade 4'), ('Grade 5', 'Grade 5'), ('Grade 6', 'Grade 6'), ('Grade 7', 'Grade 7'), ('Grade 8', 'Grade 8'), ('Grade 9', 'Grade 9'), ('Grade 10', 'Grade 10'), ('Grade 11', 'Grade 11'), ('Grade 12', 'Grade 12')], default='Grade 1', max_length=50),
        ),
        migrations.AddField(
            model_name='note',
            name='subject',
            field=models.CharField(choices=[('math', 'Mathematics'), ('science', 'Science'), ('history', 'History'), ('english', 'English'), ('computers', 'Computer Science'), ('arts', 'Arts')], default='math', max_length=50),
        ),
    ]
