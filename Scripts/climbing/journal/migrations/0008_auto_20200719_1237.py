# Generated by Django 3.0.8 on 2020-07-19 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0007_auto_20200719_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.DateField(),
        ),
    ]
