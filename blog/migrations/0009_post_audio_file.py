# Generated by Django 4.2.7 on 2023-12-27 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_post_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='audio_file',
            field=models.FileField(blank=True, null=True, upload_to='audio/'),
        ),
    ]
