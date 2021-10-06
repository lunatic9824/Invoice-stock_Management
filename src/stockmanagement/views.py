from django.shortcuts import render,redirect
from django.http import HttpResponse
import csv
from .models import *
from .forms import *
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
import pdfkit
from io import BytesIO


# Create your views here.

def home(request):
        title = 'Welcome to the Invoice & Stock management  '
        context = {
        "title": title,
        }
        # return redirect('/list_items')
        return render(request, "home.html",context)

#@login_required
def list_view(request):
    header = 'List of items'
    form = StockSearchForm(request.POST or None)
    queryset=Stock.objects.all()
    context = {
    "header": header,
    "queryset":queryset,
    "form": form,

    }
    if request.method == 'POST':
           category = form['category'].value()
        
           queryset = Stock.objects.filter(
                                           item_name__icontains=form['item_name'].value(),
                                           price__icontains=form['price'].value()
                                            )
           if (category != ''):
                            queryset = queryset.filter(category_id=category)

           if form['export_to_CSV'].value() == True:
               response = HttpResponse(content_type='text/csv')
               response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
               writer = csv.writer(response)
               writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY','PRICE'])
               instance = queryset
               for stock in instance:
                 writer.writerow([stock.category, stock.item_name, stock.quantity,stock.price])
               return response

    context = {
    "form": form,
    "header": header,
    "queryset": queryset,}
    return render(request, "list_item.html",context)

#@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)

#@login_required
def update_items(request, pk):
        queryset = Stock.objects.get(id=pk)
        form = StockUpdateForm(instance=queryset)
        if request.method == 'POST':
            form = StockUpdateForm(request.POST, instance=queryset)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully Updated')
                return redirect('/list_items')
        context = {
            'form':form,
            'title':"Update Item"
        }
        return render(request, 'add_items.html', context)

#@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
                queryset.delete()
                messages.success(request, 'Successfully Deleted')
                return redirect('/list_items')
    return render(request, 'delete_items.html')
#@login_required
def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"queryset": queryset,
	}
	return render(request, "stock_details.html", context)

#@login_required
def issue_items(request, pk):
       queryset = Stock.objects.get(id=pk)
       form = IssueForm(request.POST or None, instance=queryset)
       if form.is_valid():
           instance = form.save(commit=False)
        #    instance.receive_quantity = 0
           instance.quantity -= instance.issue_quantity
           instance.issue_by = str(request.user)
           messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
           instance.save()
           issue_history = StockHistory(
               # id = instance.id, 
                last_updated = instance.last_updated,
                category_id = instance.category_id,
                item_name = instance.item_name, 
                quantity = instance.quantity, 
                issue_to = instance.issue_to, 
                issue_by = instance.issue_by, 
                issue_quantity = instance.issue_quantity, 
                )
           issue_history.save()
           return redirect('/stock_detail/'+str(instance.id))
           # return HttpResponseRedirect(instance.get_absolute_url())

       context = {
           "title": 'Issue ' + str(queryset.item_name),
           "queryset": queryset,
           "form": form,
           "username": 'Issue By: ' + str(request.user),
       }
       return render(request, "add_items.html", context)


#@login_required
def receive_items(request, pk):
       queryset = Stock.objects.get(id=pk)
       form = ReceiveForm(request.POST or None, instance=queryset)
       if form.is_valid():
            instance = form.save(commit=False)
            # instance.issue_quantity = 0
            instance.quantity += instance.receive_quantity
            instance.receive_by = str(request.user)
            instance.save()
            receive_history = StockHistory(
               # id = instance.id, 
                last_updated = instance.last_updated,
                category_id = instance.category_id,
                item_name = instance.item_name, 
                quantity = instance.quantity, 
                price = instance.price,
                receive_quantity = instance.receive_quantity, 
                receive_by = instance.receive_by
                )
            receive_history.save()
            messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

            return redirect('/stock_detail/'+str(instance.id))
            # return HttpResponseRedirect(instance.get_absolute_url())
       context = {
                "title": 'Reaceive ' + str(queryset.item_name),
                "instance": queryset,
                "form": form,
                "username": 'Receive By: ' + str(request.user),
            }
       return render(request, "add_items.html", context)

#@login_required
def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

		return redirect("/list_items")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_items.html", context)


#@login_required
def list_history(request):
            header = 'HISTORY OF ITEMS'
            queryset = StockHistory.objects.all()
            form = StockHistorySearchForm(request.POST or None)
            context = {
                    "header": header,
                    "form": form,
                    "queryset": queryset,
                }
            if request.method == 'POST':
                        category = form['category'].value()
                        queryset = StockHistory.objects.filter(
                        item_name__icontains=form['item_name'].value(),
                            last_updated__range=[
                                                form['start_date'].value(),
                                                form['end_date'].value()
                                            ]
                            )

                        if (category != ''):
                            queryset = queryset.filter(category_id=category)

            if form['export_to_CSV'].value() == True:
                        response = HttpResponse(content_type='text/csv')
                        response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
                        writer = csv.writer(response)
                        writer.writerow(
                            ['CATEGORY', 
                            'ITEM NAME',
                            'QUANTITY', 
                            'PRICE',
                            'ISSUE QUANTITY', 
                            'RECEIVE QUANTITY', 
                            'RECEIVE BY', 
                            'ISSUE BY', 
                            'LAST UPDATED'])
                        instance = queryset
                        for stock in instance:
                            writer.writerow(
                            [stock.category, 
                            stock.item_name, 
                            stock.quantity, 
                            stock.price,
                            stock.issue_quantity, 
                            stock.receive_quantity, 
                            stock.receive_by, 
                            stock.issue_by, 
                            stock.last_updated])
                        return response

            context = {
                        "form": form,
                        "header": header,
                        "queryset": queryset,
            }
            return render(request, "list_history.html",context)


def add_category(request):
	form = CategoryCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Successfully Created')
		return redirect('/list_items')
	context = {
		"form": form,
		"title": "Add Category",
	}
	return render(request, "add_items.html", context)


def CustomerFormView(request):
        form=CustomerForm(request.POST or None)
        if form.is_valid():
            cust = CustomerDetails()
            cust.cust_name = request.POST['cust_name']
            cust.contact_num = request.POST['contact_num']
            cust.email = request.POST['email']
            cust.address = request.POST['address']
            cust.address_2 = request.POST['address_2']
            cust.landmark = request.POST['landmark']
            cust.country = request.POST['country']
            cust.state = request.POST['state']
            cust.city = request.POST['city']
            cust.pincode = request.POST['pincode']
            cust.save()
            return redirect('customer_form')
        return render(request,'customerform.html',{'form':form})

def CustomerView(request):
        model = CustomerDetails.objects.all()
        header="Customer"
        return render(request,'customer.html',{'model':model,'header':header})


#@login_required
def delete_Customer(request, pk):
    queryset = CustomerDetails.objects.get(id=pk)
    if request.method == 'POST':
                queryset.delete()
                messages.success(request, 'Successfully Deleted')
                return redirect('/customer_view')
    return render(request, 'delete_customer.html')


def update_customer(request, pk):
        queryset = CustomerDetails.objects.get(id=pk)
        form = CustomerUpdateForm(instance=queryset)
        if request.method == 'POST':
            form = CustomerUpdateForm(request.POST, instance=queryset)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully Updated')
                return redirect('/customer_view')
        context = {
            'form':form,
            'title':"Update Customer details"
        }
        return render(request, 'customerform.html', context)


def add_invoice(request):
        cust = CustomerDetails.objects.all()
        form = invoiceForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/customer_view')
        context = {
            'form':form,
            'title':"Add Invoice",
             'cust':cust,
        }
        return render(request, 'Invoice.html', context)


def ProductForm(request):
        invo = Invoice_Details.objects.all()
        stock = Stock.objects.all()
        if request.POST:
            prod = Product()
            prod.Invoice = Invoice_Details.objects.get(Invoice_num=request.POST['Invoice'])
            prod.Product_name = request.POST['Product_name']
            prod.Qty = request.POST['Qty']
            prod.Price = request.POST['Price']
            prod.Discount = request.POST['Discount']
            prod.Cgst = request.POST['Cgst']
            prod.Sgst = request.POST['Sgst']
            prod.Igst = request.POST['Igst']
            prod.Total = request.POST['Total']
            prod.disc_rs = request.POST['disc_rs']
            prod.save()
            messages.success(request, 'Successfully added')
            return redirect('/productform/')
        return render(request,'productform.html',{'invo':invo,'stock':stock})




def InvoicePage(request,id):
        cust_data = CustomerDetails.objects.get(id=id)
        in_data = Invoice_Details.objects.filter(Cust_name=cust_data)
        invo = []
        pro = []
        pro_tot = []
        
        for i in in_data:
            print(i)
            invo.append(i)
            pro_count = Product.objects.filter(Invoice=i).count()
            print(pro_count)
            pro.append(pro_count)
            t = 0
            pro_data = Product.objects.filter(Invoice=i)
            for i in pro_data:
                t += float(i.Total)
            pro_tot.append(t)
            
            
        data = zip(invo,pro,pro_tot)
        request.session['pro_tot'] = t
        return render(request,'invoice_list.html',{'cust':cust_data,'invo':data})
        

def view_Invoice(request,id):
         in_data = Invoice_Details.objects.get(Invoice_num=id)
         prod=Product.objects.filter(Invoice=in_data)
         t=0
         list=[]
         for i in prod:
             t+=float(i.Total)
             list.append(i)
         print(list,t)
         data = {"rec":in_data,'prod':list,'pr':prod,'pro_tot':t}
         return render(request,'viewinvoice.html',data)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def Shop_PDF(request,id):
        in_data = Invoice_Details.objects.get(Invoice_num=id)
        prod=Product.objects.filter(Invoice=in_data)
        t=0
        list=[]
        for i in prod:
            t+=float(i.Total)
            list.append(i)
        print(list,t)
        # pro_tot=request.session['pro_tot']
        data = {"rec":in_data,'prod':list,'pr':prod,'pro_tot':t}
        pdf = render_to_pdf('GeneratePdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


def InvoiceDelete(request,invo_del):
        data = Invoice_Details.objects.get(Invoice_num=invo_del)
        data.delete()
        return redirect('customer_view')




def signup(request):
    form=userForm(request.POST or None)
    users=UserDetails.objects.all()
    if request.POST:
        model=UserDetails()
        model.name=request.POST['name']
        model.email=request.POST['email']
        model.phone=request.POST['phone']
        model.user_id=request.POST['user_id']
        model.password_1=request.POST['password_1']
        model.password_2=request.POST['password_2']
        for i in users:
            if(model.email== i.email):
                messages.error(request,'Email already Registered')
                return redirect ("signup")   
            else:
                model.save()    
        return redirect("login")
    return render(request,"signup.html",{'form':form})



def login(request):
    if request.POST:
        # try:
            user_id=request.POST['user_id']
            Password=request.POST['Password']
            obj=UserDetails.objects.get(user_id=user_id)
            if obj.password_1==Password:
                return redirect('list_items')
            else:
                messages.error(request,'Wrong Password')
                return redirect('login')
                
        # except:
        #     return HttpResponse('No user')
    return render(request,'login.html')