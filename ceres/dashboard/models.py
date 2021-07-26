from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


# Office (id, name, address, contact, gstn)
class Office(models.Model):
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    contact = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    gstin = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


# Warehouse (id, office_id, name, code)
class Warehouse(models.Model):
    office_id = models.ForeignKey(Office, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=10, null=True, unique=True)
    date_added = models.DateField()

    def __str__(self):
        s = "["+self.code+"] "+self.name
        return s


# Trader (name, address, email, contact, gstin, date_added)
class Trader(models.Model):
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    contact = models.CharField(max_length=50, null=True)
    gstin = models.CharField(max_length=20, null=True)
    date_added = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


# Trader-user (id, userid, traderid)
class TraderUser(models.Model):
    user_id = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    trader_id = models.ForeignKey(Trader, null=True, on_delete=models.CASCADE)


# Items (id, name, code, details, last_edit_date_time, user_id)
class Item(models.Model):
    name = models.CharField(max_length=30, null=True)
    code = models.CharField(max_length=20, null=True, unique=True)
    details = models.CharField(max_length=80, null=True)
    def __str__(self):
        s = "["+self.code + "] "+self.name
        return s

# Making loose coupling of packing w.r.t Items
class Packing(models.Model):
    type = models.CharField(max_length=20, null=True, unique=True)

    def __str__(self):
        return self.type


# Invoice (id, trader_id, inv_no, inv_date, inv_amount)
class Invoice(models.Model):
    trader_id = models.ForeignKey(Trader, null=True, on_delete=models.CASCADE)
    inv_no = models.CharField(max_length=50, null=True)
    inv_date = models.DateField(null=True)
    inv_amount = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])
    def __str__(self):
        s = self.inv_no+" ("+self.trader_id.name+")"
        return s


# Invoice Items (id, inv_id, item_id, packing_id, warehouse_id, batch_name, manufacturer name, manufacturing_date,
# expiry_date, quantity, unit_amount)
class InvoiceItems(models.Model):
    invoice = models.ForeignKey(Invoice, null=True, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, null=True, on_delete=models.DO_NOTHING)
    packing_id = models.ForeignKey(Packing, null=True, on_delete=models.DO_NOTHING)
    warehouse_id = models.ForeignKey(Warehouse, null=True, on_delete=models.DO_NOTHING)
    batch_name = models.CharField(max_length=50, null=True)
    manufacturer_name = models.CharField(max_length=50, null=True)
    manufacturing_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    quantity = models.PositiveIntegerField(null=True)
    unit_amount = models.DecimalField(null=True, max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    total_amount = models.DecimalField(null=True, max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

# StorageReceipt (inv_id, date, final_amount, user_id, note_details)
class StorageReceipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    note_details = models.CharField(max_length=200, default="")


# AMBIGUITY ABOUT Single SR is single invoice or multiple invoice


# DO (inv_id, consignor_id, consignee_id, driver_name, vehicle_number, pick_up_date_time, user_id, note_details)
class DeliveryOrder(models.Model):
    invoice = models.ForeignKey(Invoice, null=True, on_delete=models.CASCADE)
    consignor = models.ForeignKey(Trader, null=True, on_delete=models.DO_NOTHING, related_name='+')
    consignee = models.ForeignKey(Trader, null=True, on_delete=models.DO_NOTHING, related_name='+')
    driver_name = models.CharField(max_length=50, null=True)
    vehicle_number = models.CharField(max_length=50, null=True)
    pick_up_date_time = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    note_details = models.CharField(max_length=200, default="")


pay_types = (("Bank Transfer", "Bank Transfer"),
             ("Cash", "Cash"),
             ("Other", "Other"))


# Payment (id, storage_receipt_id, delivery_order_id, trader_id, paid_amount, payment_type, other_details,user_id)
class Payment(models.Model):
    storage_receipt = models.ForeignKey(StorageReceipt, on_delete=models.CASCADE)
    delivery_order = models.ForeignKey(DeliveryOrder, on_delete=models.CASCADE)
    # Payer name who is a trader actually
    trader = models.ForeignKey(Trader, null=True, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    payment_type = models.CharField(max_length=20, choices=pay_types, null=True)
    other_details = models.CharField(max_length=200)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
