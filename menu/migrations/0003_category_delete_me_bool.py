# Generated by Django 2.1.5 on 2019-02-14 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20190213_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='delete_me_bool',
            field=models.BooleanField(default=False),
        ),
    ]