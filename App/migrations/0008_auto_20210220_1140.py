# Generated by Django 3.1.6 on 2021-02-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_auto_20210220_0603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
