# Generated by Django 4.2.7 on 2023-11-30 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20231129_2158'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(max_length=60)),
                ('Password', models.CharField(max_length=60)),
                ('FullName', models.CharField(max_length=60, null=True)),
                ('MobileNo', models.PositiveIntegerField(null=True, unique=True)),
                ('Email', models.CharField(max_length=80, null=True, unique=True)),
                ('Address', models.TextField(null=True, unique=True)),
            ],
        ),
    ]
