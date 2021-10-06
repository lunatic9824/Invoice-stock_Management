from django import forms
from .models import *
from bootstrap_datepicker_plus import DatePickerInput


class StockCreateForm(forms.ModelForm):
   class Meta:
     model = Stock
     fields = ['category', 'item_name', 'quantity','price']
   def clean_category(self):
        category = self.cleaned_data.get('category')
        item_name = self.cleaned_data.get('item_name')
        if not category:
          raise forms.ValidationError('This field is required')
        return category


   def clean_item_name(self):
        category = self.cleaned_data.get('category')
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
           raise forms.ValidationError('This field is required')
        for instance in Stock.objects.all():
             if instance.category == category and instance.item_name == item_name:
               raise forms.ValidationError(str(item_name) + ' is already created')
        return item_name

class StockSearchForm(forms.ModelForm):
  export_to_CSV = forms.BooleanField(required=False)
  class Meta:
     model = Stock
     fields = ['category', 'item_name','price']

class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['category', 'item_name', 'quantity','price']

class IssueForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['issue_quantity', 'issue_to']


class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity']

class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']

class StockHistorySearchForm(forms.ModelForm):
	export_to_CSV = forms.BooleanField(required=False)
	start_date = forms.DateTimeField(required=True)
	end_date = forms.DateTimeField(required=True)
	class Meta:
		model = StockHistory
		fields = ['category', 'item_name', 'start_date', 'end_date']


class CategoryCreateForm(forms.ModelForm):
    class Meta:
      model = Category
      fields = ['name']

    def clean_category(self):
          name = self.cleaned_data.get('name')
          for i in Category.objects.all():
            if i.name == name:
              raise forms.ValidationError(str(name) + ' is already created')
          return name





class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerDetails
        fields = '__all__'


class CustomerUpdateForm(forms.ModelForm):
	class Meta:
		model = CustomerDetails
		fields = '__all__'


class invoiceForm(forms.ModelForm):
  Due_date = forms.DateTimeField(required=False,widget = forms.SelectDateWidget)
  class Meta:
    model = Invoice_Details
    fields = ['Cust_name','Invoice_type','Invoice_num','Due_date','note']



class userForm(forms.ModelForm):
  password_1 = forms.CharField(widget=forms.PasswordInput)
  password_2 = forms.CharField(widget=forms.PasswordInput)
  class Meta:
        model = UserDetails
        fields = ['name','email','phone','user_id','password_1','password_2']
  def clean_password_2(self):
        password_1 = self.cleaned_data.get('password_1')
        password_2 = self.cleaned_data.get('password_2')
        if (password_1 != password_2):
          raise forms.ValidationError("Passwords don't match")
        return password_2