from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .models import Trader, TraderUser


# Base URLS
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


# Operations - Create
def createChallan(request):
    pageTitle = "Inward Challan | Ceres WMS"
    pageHeading = "Create Inward Challan"
    createButtonText = ""
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/create-challan.html", context)


@login_required(login_url='login')
def viewChallan(request):
    pageTitle = "Inward challan | Ceres WMS"
    pageHeading = "Inward challan"
    createButtonText = "Create new challan"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/view-challan.html", context)


@login_required(login_url='login')
def createOrder(request):
    pageTitle = "Deliver Order | Ceres WMS"
    pageHeading = "Create Delivery Order"
    createButtonText = ""
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/create-order.html", context)


@login_required(login_url='login')
def viewOrder(request):
    pageTitle = "Delivery order | Ceres WMS"
    pageHeading = "Delivery order"
    createButtonText = "Create new Order"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/view-order.html", context)


# Operations - Trader
@login_required(login_url='login')
def createTrader(request):
    pageTitle = "Trader | Ceres WMS"
    pageHeading = "Create Trader"
    createButtonText = ""
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/create-trader.html", context)


@login_required(login_url='login')
def viewTrader(request):
    pageTitle = "Trader | Ceres WMS"
    pageHeading = "Trader"
    createButtonText = "Add new Trader"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/view-trader.html", context)


# Operations - Inventory
@login_required(login_url='login')
def createItem(request):
    pageTitle = "Items | Ceres WMS"
    pageHeading = "Create Item"
    createButtonText = ""
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/create-item.html", context)


@login_required(login_url='login')
def viewItem(request):
    pageTitle = "Items | Ceres WMS"
    pageHeading = "Items"
    createButtonText = "Create new item"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/view-item.html", context)


@login_required(login_url='login')
def createPackaging(request):
    pageTitle = "Packaging | Ceres WMS"
    pageHeading = "Create Packaging Types"
    createButtonText = ""
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/create-packing-type.html", context)


@login_required(login_url='login')
def viewPackaging(request):
    pageTitle = "Packaging | Ceres WMS"
    pageHeading = "Packaging Types"
    createButtonText = "Add new packaging"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/view-packing-type.html", context)


# Operations - Payments
@login_required(login_url='login')
def createPayment(request):
    pageTitle = "Payment | Ceres WMS"
    pageHeading = "Add Payment"
    createButtonText = ""
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/add-payment.html", context)


@login_required(login_url='login')
def viewPayment(request):
    pageTitle = "Payments | Ceres WMS"
    pageHeading = "Payments"
    createButtonText = "Add new payment"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/view-payment.html", context)


# Administration - Company
@login_required(login_url='login')
def offices(request):
    pageTitle = "Offices | Ceres WMS"
    pageHeading = "Offices"
    createButtonText = ""
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/office.html", context)


@login_required(login_url='login')
def warehouses(request):
    pageTitle = "Warehouses | Ceres WMS"
    pageHeading = "Warehouses"
    createButtonText = "Add new warehouse"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/warehouse.html", context)


@login_required(login_url='login')
def employee(request):
    pageTitle = "Employees | Ceres WMS"
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


# Create new user
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


# Reports
@login_required(login_url='login')
def stockReport(request):
    pageTitle = "Stock Report | Ceres WMS"
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
    pageTitle = "Earnings Report | Ceres WMS"
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
    pageTitle = "Payment Report | Ceres WMS"
    pageHeading = "Payment Report"
    createButtonText = "Download PDF"
    context = {
        "title": pageTitle,
        "heading": pageHeading,
        "createButtonText": createButtonText,
    }
    return render(request, "dashboard/report-payment-summary.html", context)
