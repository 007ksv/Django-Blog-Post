# Generated by Django 3.0.9 on 2020-08-14 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20200814_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile.jpg', upload_to='profile_pics'),
        ),
    ]