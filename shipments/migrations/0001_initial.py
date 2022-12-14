# Generated by Django 3.1.7 on 2022-09-08 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_shipped', models.BooleanField(db_index=True, default=False)),
                ('shipping_weight', models.PositiveSmallIntegerField(default=0)),
                ('shipping_date', models.DateTimeField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='ShipmentProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.product')),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipments.shipment')),
            ],
        ),
        migrations.AddField(
            model_name='shipment',
            name='shipping_products',
            field=models.ManyToManyField(through='shipments.ShipmentProduct', to='orders.Product'),
        ),
    ]
