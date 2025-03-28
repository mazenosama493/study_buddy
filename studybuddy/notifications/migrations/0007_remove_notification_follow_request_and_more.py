# Generated by Django 5.1.7 on 2025-03-29 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0011_remove_note_is_published'),
        ('notifications', '0006_notification_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='follow_request',
        ),
        migrations.AlterField(
            model_name='notification',
            name='note',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='notes.note'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('follow_request', 'Follow Request'), ('follow_accepted', 'Follow Accepted'), ('follow_rejected', 'Follow Rejected'), ('like', 'Like'), ('dislike', 'Dislike'), ('comment', 'Comment')], max_length=20),
        ),
    ]
