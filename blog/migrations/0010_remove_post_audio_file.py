# Generated by Django 4.2.7 on 2023-12-27 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_audio_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='audio_file',
        ),
    ]
