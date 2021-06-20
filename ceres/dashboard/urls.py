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
    path('create-order/', views.createOrder, name='create-order'),
    path('view-order/', views.viewOrder, name='view-order'),

    # Operations - Trader
    path('create-trader/', views.createTrader, name='create-trader'),
    path('view-trader/', views.viewTrader, name='view-trader'),

    # Operations - Inventory
    path('create-item/', views.createItem, name='create-item'),
    path('view-item/', views.viewItem, name='view-item'),
    path('create-packaging/', views.createPackaging, name='create-packaging'),
    path('view-packaging/', views.viewPackaging, name='view-packaging'),

    # Operations - Payments
    path('create-payment/', views.createPayment, name='create-payment'),
    path('view-payment/', views.viewPayment, name='view-payment'),

    # Administration - Company
    path('offices/', views.offices, name='offices'),
    path('warehouses/', views.warehouses, name='warehouses'),
    path('employee/', views.employee, name='employee'),
    path('create-user/', views.createUser, name='create-user'),

    # Reports
    path('stock-report/', views.stockReport, name='stock-report'),
    path('earnings-report/', views.earningsReport, name='earnings-report'),
    path('payment-report/', views.paymentReport, name='payment-report')
]
