# Generated by Django 4.2.7 on 2023-12-29 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_env_remove_user_cover_letter_user_env'),
        ('Recommend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommend',
            name='env',
        ),
        migrations.AddField(
            model_name='recommend',
            name='env',
            field=models.ManyToManyField(blank=True, to='user.env'),
        ),
    ]