# Generated by Django 3.1 on 2020-10-14 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0002_auto_20201013_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='price'),
        ),
    ]
