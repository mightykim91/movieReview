# Generated by Django 2.1.15 on 2020-05-20 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(),
        ),
    ]
