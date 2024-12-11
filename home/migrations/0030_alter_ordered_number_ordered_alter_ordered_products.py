# Generated by Django 5.1.3 on 2024-12-11 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_alter_ordered_number_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordered',
            name='number_ordered',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='ordered',
            name='products',
            field=models.ManyToManyField(related_name='ordered', to='home.cartitem'),
        ),
    ]
