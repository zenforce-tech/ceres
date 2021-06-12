from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = 'Ceres IMS'


# Office (id, name, address, contact, gstn)
@admin.register(Office)
class OfficeA(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'contact', 'address', 'gstin')


# Warehouse (id, office_id, name, code)
@admin.register(Warehouse)
class WarehouseA(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'date_added')


# Trader (name, address, email, contact, gstin, date_added)
@admin.register(Trader)
class TraderA(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'email', 'contact', 'gstin', 'date_added')

# Items (id, name, code, details, last_edit_date_time, user_id)
@admin.register(Item)
class ItemA(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'details')


# Packing (type)
@admin.register(Packing)
class PackingA(admin.ModelAdmin):
    list_display = ('id', 'type')


# Invoice (id, trader, number, date, amount)
@admin.register(Invoice)
class InvoiceA(admin.ModelAdmin):
    list_display = ('id', 'trader_id', 'inv_no', 'inv_date', 'inv_amount')


# Invoice Items (id, inv_id, item_id, packing_id, warehouse_id, batch_name, manufacturer name, manufacturing_date, expiry_date,
# quantity, unit_amount)
@admin.register(InvoiceItems)
class InvoiceItems(admin.ModelAdmin):
    list_display = (
    'id', 'inv_id', 'item_id', 'packing_id', 'warehouse_id', 'batch_name', 'manufacturer_name', 'manufacturing_date',
    'expiry_date', 'quantity', 'unit_amount')


# StorageReceipt (inv_id, date, final_amount, user_id, note_details)
@admin.register(StorageReceipt)
class StorageReceiptA(admin.ModelAdmin):
    list_display = ('id', 'inv_id', 'date', 'final_amount', 'user_id', 'note_details')


# DO (invoice_no, consignor, consignee, driver, vehicle, pickupdatetime)
@admin.register(DeliveryOrder)
class DeliveryOrderA(admin.ModelAdmin):
    list_display = (
    'inv_id', 'consignor_id', 'consignee_id', 'driver_name', 'vehicle_number', 'pick_up_date_time', 'user_id',
    'note_details')


# Payment (id, storage_receipt_id, delivery_order_id, trader_id, paid_amount, payment_type, other_details,user_id)
@admin.register(Payment)
class PaymentA(admin.ModelAdmin):
    list_display = (
    'id', 'storage_receipt_id', 'delivery_order_id', 'trader_id', 'paid_amount', 'payment_type', 'other_details',
    'user_id')
