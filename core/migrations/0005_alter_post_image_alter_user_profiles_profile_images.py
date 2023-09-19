# Generated by Django 4.1.10 on 2023-09-19 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_post_image_user_profiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='static/default-blog.png', upload_to='static/img'),
        ),
        migrations.AlterField(
            model_name='user_profiles',
            name='profile_images',
            field=models.ImageField(default='static/profile_image.jpg', upload_to='static/img'),
        ),
    ]
