from django import forms
from django.forms import Textarea

from .models import *


# Date Input function for WarehouseForm
class DateInput(forms.DateInput):
    input_type = 'date'


class WarehouseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WarehouseForm, self).__init__(*args, **kwargs)
        self.fields['office_id'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['code'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['name'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['date_added'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['office_id'].label = "Office Branch"
        self.fields['code'].label = "Warehouse code"
        self.fields['name'].label = "Warehouse name"
        self.fields['date_added'].label = "Warehouse First Date"

    class Meta:
        model = Warehouse
        fields = ['office_id', 'code', 'name', 'date_added']
        widgets = {
            'date_added': DateInput(),
        }


class OfficeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OfficeForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Office Name"
        self.fields['gstin'].label = "GST Number"
        self.fields['name'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['address'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['email'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['contact'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['gstin'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['name'].widget.attrs['placeholder'] = "Office Name"
        self.fields['address'].widget.attrs['placeholder'] = "Billing Address"
        self.fields['email'].widget.attrs['placeholder'] = "Official Email ID"
        self.fields['contact'].widget.attrs['placeholder'] = "Official contact"
        self.fields['gstin'].widget.attrs['placeholder'] = "GST Number"

    class Meta:
        model = Office
        fields = ['name', 'address', 'email', 'contact', 'gstin']
        widgets = {
            'address': Textarea(attrs={'cols': 20, 'rows': 3}),
        }


class TraderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TraderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Trader Name"
        self.fields['gstin'].label = "GST Number"
        self.fields['name'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['address'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['email'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['contact'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['gstin'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['name'].widget.attrs['placeholder'] = "Trader Company name"
        self.fields['address'].widget.attrs['placeholder'] = "Trader Address"
        self.fields['email'].widget.attrs['placeholder'] = "Trader Email ID"
        self.fields['contact'].widget.attrs['placeholder'] = "Trader contact"
        self.fields['gstin'].widget.attrs['placeholder'] = "Trader GST Number"

    class Meta:
        model = Trader
        fields = ['name', 'address', 'email', 'contact', 'gstin']
        widgets = {
            'address': Textarea(attrs={'cols': 20, 'rows': 3}),
        }


class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['style'] = "width:100%"
        self.fields['name'].widget.attrs['style'] = "width:100%"
        self.fields['details'].widget.attrs['style'] = "width:100%"

    class Meta:
        model = Item
        fields = ['code', 'name', 'details']
        widgets = {
            'details': Textarea(attrs={'cols': 20, 'rows': 3}),
        }


class PackingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PackingForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"

    class Meta:
        model = Packing
        fields = ['type']


class InvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['trader_id'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['inv_no'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['inv_date'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['inv_amount'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['trader_id'].label = "Trader Name"
        self.fields['inv_no'].label = "Trader Invoice Number"
        self.fields['inv_date'].label = "Invoice Date"
        self.fields['inv_amount'].label = "Invoice Total Amount"

    class Meta:
        model = Invoice
        fields = ['trader_id', 'inv_no', 'inv_date', 'inv_amount']
        widgets = {
            'inv_date': DateInput(),
        }


class AddInvoiceItemsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddInvoiceItemsForm, self).__init__(*args, **kwargs)
        self.fields['item_id'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['packing_id'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['warehouse_id'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['batch_name'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['manufacturer_name'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['manufacturing_date'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['expiry_date'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['quantity'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"
        self.fields['unit_amount'].widget.attrs['style'] = "width:100%; margin-bottom:10px;"

    # Invoice Items (id, inv_id, item_id, packing_id, warehouse_id, batch_name, manufacturer_name, manufacturing_date,
    # expiry_date, quantity, unit_amount)

    class Meta:
        model = InvoiceItems
        fields = ['item_id', 'packing_id', 'warehouse_id', 'batch_name', 'manufacturer_name',
                  'manufacturing_date', 'expiry_date', 'quantity', 'unit_amount']
        widgets = {
            'manufacturing_date': DateInput(),
            'expiry_date': DateInput(),
        }
