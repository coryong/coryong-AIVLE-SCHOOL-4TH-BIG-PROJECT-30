# Generated by Django 4.2.7 on 2024-01-03 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_crawling_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crawling',
            name='like',
        ),
        migrations.AddField(
            model_name='crawling',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='like_posts',
            field=models.ManyToManyField(blank=True, related_name='like_users', to='user.crawling'),
        ),
    ]