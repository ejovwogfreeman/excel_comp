# Generated by Django 4.1.4 on 2022-12-12 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Bio',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='profile_pics'),
        ),
    ]