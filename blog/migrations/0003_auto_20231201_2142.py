# Generated by Django 3.2.23 on 2023-12-01 16:12

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20231201_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='title', unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
