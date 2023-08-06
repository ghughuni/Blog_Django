# Generated by Django 4.1.10 on 2023-08-06 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='total_likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='total_unlikes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]