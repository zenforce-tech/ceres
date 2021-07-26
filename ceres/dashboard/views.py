import decimal

from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django import template
from .models import *
from .forms import *
import re


# Base URLS
# Strip HTML Tags
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.groups.filter(name="Trader").exists():
                s = "Welcome back, " + user.username
                messages.success(request, s)
                login(request, user)
                return redirect('tindex')
            elif user.groups.filter(name="Employee").exists():
                s = "Welcome back, " + user.username
                messages.success(request, s)
                login(request, user)
                return redirect('index')
            elif user.groups.filter(name="Manager").exists():
                s = "Welcome back, " + user.username
                messages.success(request, s)
                login(request, user)
                return redirect('index')
        else:
            s = "Invalid credentials"
            messages.error(request, s)
    context = {}
    return render(request, 'dashboard/login.html', context)


@login_required(login_url='login')
def index(request):
    if checkUserGroup(request.user) != "Trader":
        return render(request, "dashboard/index.html")
    else:
        return render(request, "dashboard/t-index.html")


@login_required(login_url='login')
def tindex(request):
    return render(request, "dashboard/t-index.html")


def logoutUser(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('loginPage')


# Check user group for page authentications
def checkUserGroup(user):
    if user.groups.filter(name="Trader").exists():
        return "Trader"
    elif user.groups.filter(name="Employee").exists():
        return "Employee"
    elif user.groups.filter(name="Manager").exists():
        return "Manager"


############################################ Read
@login_required(login_url='login')
def viewInvoice(request):
    pageTitle = "Invoice | ProVentory - IMS"
    pageHeading = "Invoice"
    createButtonText = "Create new invoice"
    invoices = Invoice.objects.all()
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            currentInvoice = form.save()
            messages.success(request, "Invoice created. You can add items now.")
            return redirect(reverse('invoice-items', kwargs={"invoice": currentInvoice.id}))
        else:
            if form.errors:
                for err in form.errors:
                    messages.error(request, cleanhtml(str(form.errors[err])))
    else:
        form = InvoiceForm()
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "invoices": invoices,
        "form": form,
    }
    return render(request, "dashboard/view-invoice.html", context)


@login_required(login_url='login')
def viewInvoiceItems(request, invoice):
    pageTitle = "Add challan items | ProVentory - IMS"
    pageHeading = "Challan Items"
    createButtonText = ""
    currentInvoice = Invoice.objects.get(pk=invoice)
    invoiceItems = InvoiceItems.objects.filter(invoice=currentInvoice.id)
    total_amount = 0
    gst = 0
    grand_total = 0
    if InvoiceItems.objects.filter(invoice=currentInvoice.id).count() > 0:
        total_amount = round(
            InvoiceItems.objects.filter(invoice=currentInvoice.id).aggregate(Sum('total_amount'))['total_amount__sum'],
            2)
        gst = round(total_amount * decimal.Decimal(0.18), 2)
        grand_total = total_amount + gst
    if request.method == "POST":
        form = AddInvoiceItemsForm(request.POST)
        if form.is_valid():
            newItem = form.save(commit=False)
            newItem.invoice = currentInvoice
            newItem.total_amount = newItem.quantity * newItem.unit_amount
            newItem.save()
            messages.success(request, "Item added successfully")
            return redirect(reverse('invoice-items', kwargs={'invoice': currentInvoice.id}))
        else:
            if form.errors:
                for err in form.errors:
                    messages.error(request, cleanhtml(str(form.errors[err])))
    else:
        form = AddInvoiceItemsForm()
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "currentInvoice": currentInvoice,
        "invoiceItems": invoiceItems,
        "addInvoiceItemsForm": form,
        "total_amount": total_amount,
        "gst": gst,
        "grand_total": grand_total
    }
    return render(request, "dashboard/invoice-items.html", context)


@login_required(login_url='login')
def viewOrder(request):
    pageTitle = "Delivery order | ProVentory - IMS"
    pageHeading = "Delivery order"
    createButtonText = "Create new Order"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/view-order.html", context)


@login_required(login_url='login')
def viewTrader(request):
    pageTitle = "Traders | ProVentory - IMS"
    pageHeading = "Traders"
    createButtonText = "Add new trader"
    traders = Trader.objects.all()
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "traders": traders,
    }
    return render(request, "dashboard/view-trader.html", context)


@login_required(login_url='login')
def viewItem(request):
    pageTitle = "Items | ProVentory - IMS"
    pageHeading = "Items"
    createButtonText = "Create new item"
    items = Item.objects.all()
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item added successfully")
            return redirect('view-item')
        else:
            if form.errors:
                for err in form.errors:
                    messages.error(request, cleanhtml(str(form.errors[err])))
            return redirect('view-item')
    else:
        form = ItemForm()
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "form": form,
        "items": items,
    }
    return render(request, "dashboard/view-item.html", context)


@login_required(login_url='login')
def viewPackaging(request):
    pageTitle = "Packaging | ProVentory - IMS"
    pageHeading = "Packaging Types"
    createButtonText = "Add new packaging"
    packing = Packing.objects.all()
    if request.method == "POST":
        form = PackingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Packing type added successfully")
            return redirect('view-packaging')
        else:
            if form.errors:
                for err in form.errors:
                    messages.error(request, cleanhtml(str(form.errors[err])))
            return redirect('view-packaging')
    else:
        form = PackingForm()

    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "form": form,
        "packing": packing
    }
    return render(request, "dashboard/view-packing-type.html", context)


@login_required(login_url='login')
def viewChallan(request):
    x = 1


@login_required(login_url='login')
def viewPayment(request):
    pageTitle = "Payments | ProVentory - IMS"
    pageHeading = "Payments"
    createButtonText = "Add new payment"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/view-payment.html", context)


@login_required(login_url='login')
def offices(request):
    pageTitle = "Offices | ProVentory - IMS"
    pageHeading = "Offices"
    createButtonText = "Create Office"
    offices = Office.objects.all()
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "offices": offices
    }
    return render(request, "dashboard/office.html", context)


@login_required(login_url='login')
def viewWarehouse(request):
    pageTitle = "Warehouses | ProVentory - IMS"
    pageHeading = "Warehouses"
    createButtonText = "Add new warehouse"
    warehouses = Warehouse.objects.all()
    if request.method == "POST":
        form = WarehouseForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Warehouse added successfully")
            print("Object Id = ", obj.id)
            return redirect('view-warehouse')
        else:
            if form.errors:
                for err in form.errors:
                    messages.error(request, cleanhtml(str(form.errors[err])))
            return redirect('view-warehouse')
    else:
        form = WarehouseForm()

    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "warehouses": warehouses,
        "form": form,
    }
    return render(request, "dashboard/warehouse.html", context)


@login_required(login_url='login')
def employee(request):
    pageTitle = "Employees | ProVentory - IMS"
    pageHeading = "Employees"
    createButtonText = "Add Employee"
    users = User.objects.all()
    traders = Trader.objects.all()
    tusers = TraderUser.objects.all()
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "users": users,
        "traders": traders,
        "tusers": tusers,
    }
    return render(request, 'dashboard/employee.html', context)


############################################ Create

@login_required(login_url='login')
def createChallan(request):
    pageTitle = "Inward Challan | ProVentory - IMS"
    pageHeading = "Create Inward Challan"
    createButtonText = ""

    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/create-challan.html", context)


@login_required(login_url='login')
def createOrder(request):
    pageTitle = "Deliver Order | ProVentory - IMS"
    pageHeading = "Create Delivery Order"
    createButtonText = ""
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/create-order.html", context)


@login_required(login_url='login')
def createTrader(request):
    pageTitle = "Trader | ProVentory - IMS"
    pageHeading = "Create Trader"
    createButtonText = ""
    if request.method == "POST":
        form = TraderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Trader added successfully")
            return redirect('view-trader')
        else:
            if form.errors:
                for err in form.errors:
                    messages.error(request, cleanhtml(str(form.errors[err])))
    else:
        form = TraderForm()
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "form": form,
    }
    return render(request, "dashboard/create-trader.html", context)


@login_required(login_url='login')
def createPayment(request):
    pageTitle = "Payment | ProVentory - IMS"
    pageHeading = "Add Payment"
    createButtonText = ""
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/add-payment.html", context)


@login_required(login_url='login')
def createOffice(request):
    pageTitle = "Office | ProVentory - IMS"
    pageHeading = "Create Office"
    createButtonText = ""
    if request.method == "POST":
        form = OfficeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Office created successfully")
            return redirect('offices')
        else:
            if form.errors:
                for err in form.errors:
                    messages.error(request, cleanhtml(str(form.errors[err])))
    else:
        form = OfficeForm()
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "form": form,
    }
    return render(request, "dashboard/create-office.html", context)


@login_required(login_url='login')
def createUser(request):
    if request.user.groups.filter(name="Manager").exists():
        traders = Trader.objects.all()
        context = {
            "traders": traders,
        }
        return render(request, 'dashboard/create-user.html', context)
    else:
        messages.warning(request, "You do not have rights to create new user. Please contact admin.")
        return redirect('employee')


############################################ Update


@login_required(login_url='login')
def updateInvoice(request, pk):
    pageTitle = "Trader | ProVentory - IMS"
    pageHeading = "Update Invoice"
    createButtonText = ""
    invoice = Invoice.objects.get(id=pk)
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, "Invoice updated successfully")
            return redirect('view-invoice')
        else:
            if form.errors:
                for err in form.errors:
                    messages.error(request, cleanhtml(str(form.errors[err])))
    else:
        form = InvoiceForm(instance=invoice)
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "form": form,
    }
    return render(request, "dashboard/update-invoice.html", context)


@login_required(login_url='login')
def updateInvoiceItem(request, pk):
    pageTitle = "Trader | ProVentory - IMS"
    pageHeading = "Update Invoice Item"
    createButtonText = ""
    item = InvoiceItems.objects.get(id=pk)
    invoice = Invoice.objects.get(id=item.invoice.id)
    if request.method == "POST":
        itemform = AddInvoiceItemsForm(request.POST, instance=item)
        if itemform.is_valid():
            x = itemform.save(commit=False)
            x.total_amount = x.quantity * x.unit_amount
            x.save()
            messages.success(request, "Item updated successfully")
            return redirect(reverse('invoice-items', kwargs={'invoice': invoice.id}))
        else:
            if itemform.errors:
                for err in itemform.errors:
                    messages.error(request, cleanhtml(str(itemform.errors[err])))
    else:
        itemform = AddInvoiceItemsForm(instance=item)
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "itemform": itemform,
        "invoice": invoice
    }
    return render(request, "dashboard/update-invoice-item.html", context)


@login_required(login_url='login')
def updateTrader(request, pk):
    pageTitle = "Trader | ProVentory - IMS"
    pageHeading = "Update Trader"
    createButtonText = ""
    trader = Trader.objects.get(id=pk)
    if request.method == "POST":
        form = TraderForm(request.POST, instance=trader)
        if form.is_valid():
            form.save()
            messages.success(request, "Trader updated successfully")
            return redirect('view-trader')
        else:
            if form.errors:
                for err in form.errors:
                    messages.error(request, cleanhtml(str(form.errors[err])))
    else:
        form = TraderForm(instance=trader)
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "form": form,
    }
    return render(request, "dashboard/update-trader.html", context)


@login_required(login_url='login')
def updateItem(request, pk):
    pageTitle = "Packaging | ProVentory - IMS"
    pageHeading = "Update Item"
    createButtonText = ""
    try:
        item = Item.objects.get(id=pk)
        if request.method == "POST":
            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                messages.success(request, "Item updated successfully")
                return redirect('view-item')
            else:
                if form.errors:
                    for err in form.errors:
                        messages.error(request, cleanhtml(str(form.errors[err])))
                return redirect('view-item')
        else:
            form = ItemForm(instance=item)
    except Exception as e:
        messages.error(request, e)
        return redirect('view-item')
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "form": form,
    }
    return render(request, "dashboard/update-item.html", context)


@login_required(login_url='login')
def updatePackaging(request, pk):
    pageTitle = "Packaging | ProVentory - IMS"
    pageHeading = "Update Packaging Type"
    createButtonText = ""
    try:
        packing = Packing.objects.get(id=pk)
        if request.method == "POST":
            form = PackingForm(request.POST, instance=packing)
            if form.is_valid():
                form.save()
                messages.success(request, "Packing type updated successfully")
                return redirect('view-packaging')
            else:
                if form.errors:
                    for err in form.errors:
                        messages.error(request, cleanhtml(str(form.errors[err])))
                return redirect('view-packaging')
        else:
            form = PackingForm(instance=packing)
    except Exception as e:
        messages.error(request, e)
        return redirect('view-packaging')

    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "form": form,
    }
    return render(request, "dashboard/update-packing-type.html", context)


@login_required(login_url='login')
def updateOffice(request, pk):
    pageTitle = "Offices | ProVentory - IMS"
    pageHeading = "Update Office"
    createButtonText = ""
    office = Office.objects.get(id=pk)
    if request.method == "POST":
        form = OfficeForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            messages.success(request, "Office details updated successfully")
            return redirect('offices')
        else:
            if form.errors:
                for err in form.errors:
                    messages.error(request, cleanhtml(str(form.errors[err])))
    else:
        form = OfficeForm(instance=office)
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "form": form,
    }
    return render(request, "dashboard/update-office.html", context)


@login_required(login_url='login')
def updateWarehouse(request, pk):
    pageTitle = "Warhouse | ProVentory - IMS"
    pageHeading = "Update Warhouse"
    createButtonText = ""
    wh = Warehouse.objects.get(id=pk)
    if request.method == "POST":
        form = WarehouseForm(request.POST, instance=wh)
        if form.is_valid():
            form.save()
            messages.success(request, "Warehouse details updated successfully")
            return redirect('view-warehouse')
        else:
            if form.errors:
                for err in form.errors:
                    messages.error(request, cleanhtml(str(form.errors[err])))
    else:
        form = WarehouseForm(instance=wh)
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
        "form": form,
    }
    return render(request, "dashboard/update-warehouse.html", context)


############################################ Delete

@login_required(login_url='login')
def deleteInvoice(request, pk):
    pageTitle = "Invoice | ProVentory - IMS"
    pageHeading = "Delete Invoice"
    createButtonText = ""
    invoice = Invoice.objects.get(id=pk)
    try:
        if request.method == "POST":
            invoice.delete()
            messages.success(request, "Invoice deleted successfully")
            return redirect('view-invoice')
    except Exception as e:
        messages.error(request, e)
        return redirect('view-invoice')
    return render(request, "dashboard/delete-invoice.html")


@login_required(login_url='login')
def deleteInvoiceItem(request, pk):
    pageTitle = "Invoice Items | ProVentory - IMS"
    pageHeading = "Delete Invoice Item"
    createButtonText = ""
    item = InvoiceItems.objects.get(id=pk)
    invoice = Invoice.objects.get(id=item.invoice.id)
    context = {
        "invoice": invoice
    }
    try:
        if request.method == "POST":
            item.delete()
            messages.success(request, "Invoice line item deleted successfully")
            return redirect(reverse('invoice-items', kwargs={'invoice': invoice.id}))
    except Exception as e:
        messages.error(request, e)
        return redirect('view-invoice')
    return render(request, "dashboard/delete-invoice-item.html", context)


@login_required(login_url='login')
def deleteTrader(request, pk):
    pageTitle = "Trader | ProVentory - IMS"
    pageHeading = "Delete Trader"
    createButtonText = ""
    trader = Trader.objects.get(id=pk)
    try:
        if request.method == "POST":
            trader.delete()
            messages.success(request, "Trader deleted successfully")
            return redirect('view-trader')
    except Exception as e:
        messages.error(request, e)
        return redirect('view-trader')
    return render(request, "dashboard/delete-trader.html")


@login_required(login_url='login')
def deleteItem(request, pk):
    pageTitle = "Packaging | ProVentory - IMS"
    pageHeading = "Delete Item"
    createButtonText = ""
    item = Item.objects.get(id=pk)
    try:
        if request.method == "POST":
            item.delete()
            messages.success(request, "Item deleted successfully")
            return redirect('view-item')
    except Exception as e:
        messages.error(request, e)
        return redirect('view-item')
    return render(request, "dashboard/delete-item.html")


@login_required(login_url='login')
def deletePackaging(request, pk):
    pageTitle = "Packaging | ProVentory - IMS"
    pageHeading = "Delete Packaging Type"
    createButtonText = ""
    packing = Packing.objects.get(id=pk)
    try:
        if request.method == "POST":
            packing.delete()
            messages.success(request, "Packing type deleted successfully")
            return redirect('view-packaging')
    except Exception as e:
        messages.error(request, e)
        return redirect('view-packaging')
    return render(request, "dashboard/delete-packing-type.html")


@login_required(login_url='login')
def deleteOffice(request, pk):
    pageTitle = "Office | ProVentory - IMS"
    pageHeading = "Delete Office"
    createButtonText = "Create new office"
    office = Office.objects.get(id=pk)
    try:
        if request.method == "POST":
            office.delete()
            messages.success(request, "Office deleted successfully")
            return redirect('offices')
    except Exception as e:
        messages.error(request, e)
        return redirect('offices')
    return render(request, "dashboard/delete-office.html")


@login_required(login_url='login')
def deleteWarehouse(request, pk):
    pageTitle = "Warehouse | ProVentory - IMS"
    pageHeading = "Delete Warehouse"
    createButtonText = "Create new Warehouse"
    warehouse = Warehouse.objects.get(id=pk)
    try:
        if request.method == "POST":
            warehouse.delete()
            messages.success(request, "Office deleted successfully")
            return redirect('view-warehouse')
    except Exception as e:
        messages.error(request, e)
        return redirect('view-warehouse')
    return render(request, "dashboard/delete-warehouse.html")


# Create new user


# Reports
@login_required(login_url='login')
def stockReport(request):
    pageTitle = "Stock Report | ProVentory - IMS"
    pageHeading = "Stock Report"
    createButtonText = "Download PDF"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/report-stock.html", context)


@login_required(login_url='login')
def earningsReport(request):
    pageTitle = "Earnings Report | ProVentory - IMS"
    pageHeading = "Earnings Report"
    createButtonText = "Download PDF"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/report-earnings.html", context)


@login_required(login_url='login')
def paymentReport(request):
    pageTitle = "Payment Report | ProVentory - IMS"
    pageHeading = "Payment Report"
    createButtonText = "Download PDF"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/report-payment-summary.html", context)
