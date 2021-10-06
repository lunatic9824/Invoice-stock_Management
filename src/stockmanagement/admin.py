from django.contrib import admin
from .models import *
from .forms import StockCreateForm

# Register your models here.

class StockCreateAdmin(admin.ModelAdmin):
   list_display = ['category', 'item_name', 'quantity','price']
   form = StockCreateForm
   list_filter = ['category','item_name','quantity','price']
   # search_fields = ['category', 'item_name']

admin.site.register(Stock,StockCreateAdmin)
admin.site.register(Category)
admin.site.register(StockHistory)

admin.site.register(CustomerDetails)
admin.site.register(Invoice_Details)
admin.site.register(Product)
admin.site.register(UserDetails)


