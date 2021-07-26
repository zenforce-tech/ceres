from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    # Basic URLS
    path('', views.loginPage, name='loginPage'),
    path('home', views.index, name='index'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('trader-home/', views.tindex, name='tindex'),

    # Operations - Create
    path('create-challan/', views.createChallan, name='create-challan'),
    path('view-challan/', views.viewChallan, name='view-challan'),
    path('view-invoice/', views.viewInvoice, name='view-invoice'),
    path('invoice/update/<int:pk>', views.updateInvoice, name='update-invoice'),
    path('invoice/delete/<int:pk>', views.deleteInvoice, name='delete-invoice'),
    path('invoice-items/<int:invoice>', views.viewInvoiceItems, name='invoice-items'),
    path('invoice-item/update/<int:pk>', views.updateInvoiceItem, name='update-invoice-item'),
    path('invoice-item/delete/<int:pk>', views.deleteInvoiceItem, name='delete-invoice-item'),

    path('create-order/', views.createOrder, name='create-order'),
    path('view-order/', views.viewOrder, name='view-order'),

    # Operations - Trader
    path('create-trader/', views.createTrader, name='create-trader'),
    path('view-trader/', views.viewTrader, name='view-trader'),
    path('trader/update/<int:pk>', views.updateTrader, name='update-trader'),
    path('trader/delete/<int:pk>', views.deleteTrader, name='delete-trader'),

    # Operations - Inventory
    path('view-item/', views.viewItem, name='view-item'),
    path('item/update/<int:pk>', views.updateItem, name='update-item'),
    path('item/delete/<int:pk>', views.deleteItem, name='delete-item'),
    path('view-packaging/', views.viewPackaging, name='view-packaging'),
    path('packaging/update/<int:pk>', views.updatePackaging, name='update-packaging'),
    path('packaging/delete/<int:pk>', views.deletePackaging, name='delete-packaging'),


    # Operations - Payments
    path('create-payment/', views.createPayment, name='create-payment'),
    path('view-payment/', views.viewPayment, name='view-payment'),

    # Administration - Company
    path('offices/', views.offices, name='offices'),
    path('create-office', views.createOffice, name='create-office'),
    path('office/update/<int:pk>', views.updateOffice, name='update-office'),
    path('office/delete/<int:pk>', views.deleteOffice, name='delete-office'),
    path('view-warehouse/', views.viewWarehouse, name='view-warehouse'),
    path('warehouse/update/<int:pk>', views.updateWarehouse, name='update-warehouse'),
    path('warehouse/delete/<int:pk>', views.deleteWarehouse, name='delete-warehouse'),
    path('employee/', views.employee, name='employee'),
    path('create-user/', views.createUser, name='create-user'),

    # Reports
    path('stock-report/', views.stockReport, name='stock-report'),
    path('earnings-report/', views.earningsReport, name='earnings-report'),
    path('payment-report/', views.paymentReport, name='payment-report')
]
