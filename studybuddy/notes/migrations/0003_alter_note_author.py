# Generated by Django 4.2.19 on 2025-03-22 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0002_comment_parent_alter_comment_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='author',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
