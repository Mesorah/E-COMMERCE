# Generated by Django 5.1.3 on 2025-01-08 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_alter_products_price_alter_products_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='slug',
            field=models.SlugField(default='<django.db.models.fields.CharField><django.db.models.fields.PositiveIntegerField>', unique=True),
        ),
    ]
