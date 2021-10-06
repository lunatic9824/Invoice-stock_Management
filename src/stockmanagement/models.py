from django.db import models

# Create your models here.

category_choice = (
		('Furniture', 'Furniture'),
		('IT Equipment', 'IT Equipment'),
		('Phone', 'Phone'),
	)

class Category(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	def __str__(self):
		return self.name

class Stock(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True, null=True)
	item_name = models.CharField(max_length=50, blank=True, null=True)
	quantity = models.IntegerField(default='0', blank=True, null=True)
	price = models.IntegerField(default='0' , blank=True ,null=True)
	receive_quantity = models.PositiveIntegerField(default='0', blank=True, null=True)
	receive_by = models.CharField(max_length=50, blank=True, null=True)
	issue_quantity = models.PositiveIntegerField( blank=True, null=True)
	issue_by = models.CharField(max_length=50, blank=True, null=True)
	issue_to = models.CharField(max_length=50, blank=True, null=True)
	phone_number = models.CharField(max_length=50, blank=True, null=True)
	created_by = models.CharField(max_length=50, blank=True, null=True)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


	

	def __str__(self):
		return self.item_name


class StockHistory(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	item_name = models.CharField(max_length=50, blank=True, null=True)
	quantity = models.IntegerField(default='0', blank=True, null=True)
	price = models.IntegerField(default='0' , blank=False ,null=False)
	receive_quantity = models.PositiveIntegerField(default='0', blank=True, null=True)
	receive_by = models.CharField(max_length=50, blank=True, null=True)
	issue_quantity = models.PositiveIntegerField( blank=True, null=True)
	issue_by = models.CharField(max_length=50, blank=True, null=True)
	issue_to = models.CharField(max_length=50, blank=True, null=True)
	phone_number = models.CharField(max_length=50, blank=True, null=True)
	created_by = models.CharField(max_length=50, blank=True, null=True)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
	timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)

	
	def __str__(self):
		return self.item_name



class CustomerDetails(models.Model):
    cust_name = models.CharField(max_length=50,verbose_name='Customer Name')
    contact_num = models.IntegerField(verbose_name='Contact Number')
    email = models.CharField(max_length=50,default="")
    address = models.CharField(max_length=90,verbose_name='Address Line 1')
    address_2 = models.CharField(max_length=90,verbose_name='Address Line 2')
    landmark = models.CharField(max_length=50,verbose_name='Landmark')
    country = models.CharField(max_length=50,verbose_name='Country')
    state = models.CharField(max_length=50,verbose_name='State')
    city = models.CharField(max_length=50,verbose_name='City')
    pincode = models.IntegerField(verbose_name='Pincode')
	

    def __str__(self):
        return self.cust_name



		


class Invoice_Details(models.Model):
			Cust_name = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE,default="")
			Invoice_num = models.AutoField(primary_key=True )
			Invoice_type_choice= (
					('Receipt', 'Receipt'),
					('Invoice', 'Invoice'),
				)
			Invoice_type = models.CharField(max_length=50, blank=True, null=True, choices=Invoice_type_choice)
			Date = models.DateField(auto_now_add=True)
			Due_date = models.DateField(auto_now=False,blank=True)
			note = models.TextField(max_length=50,blank=True)

			def __str__(self):
				return str(self.Invoice_num)


class Product(models.Model):
    Invoice = models.ForeignKey(Invoice_Details, on_delete=models.CASCADE,default="")
    Product_name = models.CharField(max_length = 50)
    Qty = models.IntegerField()
    Price = models.IntegerField()
    Discount = models.FloatField(default=0 , blank=True , null=True)
    Cgst = models.FloatField(default=0, blank=True, null=True)
    Sgst = models.FloatField(default=0, blank=True, null=True)
    Igst = models.FloatField(default=0, blank=True, null=True)
    disc_rs = models.FloatField()
    Total = models.FloatField()
    
    def __str__(self):
        return self.Product_name



class UserDetails(models.Model):
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    email  = models.EmailField(unique=True)
    user_id = models.CharField(max_length=40)
    password_1 = models.CharField(max_length=40)
    password_2 = models.CharField(max_length=40)
	

    def __str__(self):
        return self.name