# Generated by Django 4.2.7 on 2023-12-27 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_rename_is_staff_user_is_admin_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupation_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TechnologyStack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stack_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_admin',
            new_name='is_staff',
        ),
        migrations.AddField(
            model_name='user',
            name='cover_letter',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='occupation',
            field=models.ManyToManyField(blank=True, to='user.occupation'),
        ),
        migrations.AddField(
            model_name='user',
            name='technology_stacks',
            field=models.ManyToManyField(blank=True, to='user.technologystack'),
        ),
    ]
