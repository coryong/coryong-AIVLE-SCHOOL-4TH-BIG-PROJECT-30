# Generated by Django 4.2.7 on 2024-01-04 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crawling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawling',
            name='body',
            field=models.TextField(null=True),
        ),
    ]
