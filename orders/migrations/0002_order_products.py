# Generated by Django 3.1.7 on 2022-09-08 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='orders.Product', to='catalog.Item'),
        ),
    ]
