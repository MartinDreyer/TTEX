# Generated by Django 5.0.3 on 2024-12-18 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0006_alter_transcription_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transcription',
            name='uuid',
        ),
    ]
