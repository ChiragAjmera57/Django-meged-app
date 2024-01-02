# Generated by Django 4.2.7 on 2023-12-28 09:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_post_audio_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HashTagPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True, unique=True)),
                ('content', models.TextField(null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('hashtagsm2m', models.ManyToManyField(blank=True, to='blog.hashtag')),
            ],
        ),
    ]