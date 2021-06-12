# Generated by Django 3.2.3 on 2021-06-05 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0004_auto_20210605_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_name', models.CharField(max_length=50, null=True)),
                ('vehicle_number', models.CharField(max_length=50, null=True)),
                ('pick_up_date_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inv_no', models.CharField(max_length=50, null=True)),
                ('inv_date', models.DateField(null=True)),
                ('inv_amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('code', models.CharField(max_length=20, null=True, unique=True)),
                ('details', models.CharField(max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('contact', models.CharField(max_length=50, null=True)),
                ('gstin', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Packing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('contact', models.CharField(max_length=50, null=True)),
                ('gstin', models.CharField(max_length=20, null=True)),
                ('date_added', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('code', models.CharField(max_length=10, null=True)),
                ('date_added', models.DateField()),
                ('office_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.office')),
            ],
        ),
        migrations.CreateModel(
            name='StorageReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('final_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('inv_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('payment_type', models.CharField(choices=[('Bank Transfer', 'Bank Transfer'), ('Cash', 'Cash'), ('Other', 'Other')], max_length=20, null=True)),
                ('other_details', models.CharField(max_length=200)),
                ('delivery_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.deliveryorder')),
                ('storage_receipt_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.storagereceipt')),
                ('trader_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.trader')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_name', models.CharField(max_length=50, null=True)),
                ('manufacturer_name', models.CharField(max_length=50, null=True)),
                ('manufacturing_date', models.DateField(null=True)),
                ('expiry_date', models.DateField(null=True)),
                ('quantity', models.IntegerField(null=True)),
                ('unit_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('inv_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.invoice')),
                ('item_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.item')),
                ('packing_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.packing')),
                ('warehouse_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.warehouse')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='trader_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.trader'),
        ),
        migrations.AddField(
            model_name='deliveryorder',
            name='consignee_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='dashboard.trader'),
        ),
        migrations.AddField(
            model_name='deliveryorder',
            name='consignor_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='dashboard.trader'),
        ),
        migrations.AddField(
            model_name='deliveryorder',
            name='inv_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.invoice'),
        ),
        migrations.AddField(
            model_name='deliveryorder',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]