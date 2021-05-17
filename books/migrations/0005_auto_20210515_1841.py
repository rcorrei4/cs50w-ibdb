# Generated by Django 3.1.1 on 2021-05-15 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20210503_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AlterField(
            model_name='book',
            name='protection',
            field=models.BooleanField(default=False, max_length=128),
        ),
    ]
