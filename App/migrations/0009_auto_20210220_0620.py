# Generated by Django 3.1.6 on 2021-02-20 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_auto_20210220_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='date',
            field=models.DateTimeField(),
        ),
    ]