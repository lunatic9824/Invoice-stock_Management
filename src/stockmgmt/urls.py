"""stockmgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from stockmanagement import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    # path('accounts/', include('registration.backends.default.urls')),
    path('list_items/',views.list_view,name='list_items'),
    path('add_items/', views.add_items, name='add_items'),
    path('update_items/<str:pk>/', views.update_items, name="update_items"),
    path('customer_update/<str:pk>/', views.update_customer, name="update_customer"),
    path('delete_items/<str:pk>/', views.delete_items, name="delete_items"),
    path('delete_customer/<str:pk>/', views.delete_Customer, name="delete_customer"),
    path('view_invoice/<str:id>/', views.view_Invoice,name="view_invoice"),

    path('stock_detail/<str:pk>/', views.stock_detail, name="stock_details"),
    path('issue_items/<str:pk>/', views.issue_items, name="issue_items"),
    path('receive_items/<str:pk>/', views.receive_items, name="receive_items"),
    path('reorder_level/<str:pk>/', views.reorder_level, name="reorder_level"),
    path('list_history/', views.list_history, name='list_history'),
    # path('accounts/', include('registration.backends.default.urls')),
    path('add_category/', views.add_category, name='add_category'),
    path('customer_form/', views.CustomerFormView, name='customer_form'),
    path('customer_view/', views.CustomerView, name='customer_view'),
    path('add_invoice/', views.add_invoice, name='add_invoice'),
    path('productform/', views.ProductForm, name='productform'),
    path('invoicepage/<str:id>/', views.InvoicePage, name='Invoicepage'),
    path('PDFs/<str:id>/',views.Shop_PDF,name='PDFs'),
    path('invoiceDelete/<int:invo_del>/',views.InvoiceDelete,name='InvoDel'),


    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),






]
