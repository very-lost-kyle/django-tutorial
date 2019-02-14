# Generated by Django 2.1.5 on 2019-02-05 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_text', models.CharField(max_length=10)),
                ('name_text', models.CharField(max_length=50)),
                ('shiny_bool', models.BooleanField(default=False)),
                ('level_int', models.IntegerField(default=1)),
            ],
        ),
    ]