# Generated by Django 5.1.3 on 2024-12-11 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_ordered_number_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordered',
            name='number_ordered',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
