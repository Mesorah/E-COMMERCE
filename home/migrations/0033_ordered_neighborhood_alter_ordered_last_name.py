# Generated by Django 5.1.3 on 2024-12-11 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_alter_ordered_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordered',
            name='neighborhood',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='ordered',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
    ]
