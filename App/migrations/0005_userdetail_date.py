# Generated by Django 3.1.6 on 2021-02-19 16:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_answervotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]