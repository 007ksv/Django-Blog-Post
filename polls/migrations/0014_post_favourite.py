# Generated by Django 3.0.9 on 2020-09-02 07:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0013_auto_20200901_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='favourite',
            field=models.ManyToManyField(related_name='favourites', to=settings.AUTH_USER_MODEL),
        ),
    ]