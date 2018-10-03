from django.db.models import Sum
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import *
from .forms import *

now = timezone.now()
def home(request):
   return render(request, 'crm/home.html',
                 {'crm': home})

@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/customer_list.html',
                 {'customers': customer})

@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/customer_list.html',
                         {'customers': customer})
   else:
        # edit
       form = CustomerForm(instance=customer)
       return render(request, 'crm/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('crm:customer_list')

@login_required
def service_list(request):
   services = Service.objects.filter(created_date__lte=timezone.now())
   return render(request, 'crm/service_list.html', {'services': services})

@login_required
def service_new(request):
   if request.method == "POST":
       form = ServiceForm(request.POST)
       if form.is_valid():
           service = form.save(commit=False)
           service.created_date = timezone.now()
           service.save()
           services = Service.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/service_list.html',
                         {'services': services})
   else:
       form = ServiceForm()
       # print("Else")
   return render(request, 'crm/service_new.html', {'form': form})

@login_required
def service_edit(request, pk):
   service = get_object_or_404(Service, pk=pk)
   if request.method == "POST":
       form = ServiceForm(request.POST, instance=service)
       if form.is_valid():
           service = form.save()
           # service.customer = service.id
           service.updated_date = timezone.now()
           service.save()
           services = Service.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/service_list.html', {'services': services})
   else:
       # print("else")
       form = ServiceForm(instance=service)
   return render(request, 'crm/service_edit.html', {'form': form})

@login_required
def service_delete(request, pk):
   service = get_object_or_404(Service, pk=pk)
   service.delete()
   return redirect('crm:service_list')

@login_required
def product_list(request):
   products = Product.objects.filter(created_date__lte=timezone.now())
   return render(request, 'crm/product_list.html', {'products': products})

@login_required
def product_new(request):
   if request.method == "POST":
       form = ProductForm(request.POST)
       if form.is_valid():
           product = form.save(commit=False)
           product.created_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/product_list.html',
                         {'products': products})
   else:
       form = ProductForm()
       # print("Else")
   return render(request, 'crm/product_new.html', {'form': form})

@login_required
def product_edit(request, pk):
   product = get_object_or_404(Product, pk=pk)
   if request.method == "POST":
       form = ProductForm(request.POST, instance=product)
       if form.is_valid():
           product = form.save()
           # service.customer = service.id
           product.updated_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/product_list.html', {'products': products})
   else:
       # print("else")
       form = ProductForm(instance=product)
   return render(request, 'crm/product_edit.html', {'form': form})

@login_required
def product_delete(request, pk):
   product = get_object_or_404(Product, pk=pk)
   product.delete()
   return redirect('crm:product_list')

@login_required
def summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    services = Service.objects.filter(cust_name=pk)
    products = Product.objects.filter(cust_name=pk)
    sum_service_charge = Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
    sum_product_charge = Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))
    return render(request, 'crm/summary.html', {'customers': customers,
                                                    'products': products,
                                                    'services': services,
                                                    'sum_service_charge': sum_service_charge,
                                                    'sum_product_charge': sum_product_charge,})


def password_reset(request):
    return render(request, 'home/password_reset.html',
    {'registration': password_reset})


def password_reset_confirm(request):
    return render(request, 'home/password_reset_confirm.html',
    {'registration': password_reset_confirm})

def password_reset_email(request):
    return render(request, 'home/password_reset_email.html',
    {'registration': password_reset_email})

def password_reset_complete(request):
    return render(request, 'home/password_reset_complete.html',
    {'registration': password_reset_complete})


from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from django.template.loader import get_template


"""def admin_summary_pdf(request, pk):
    # Task to send an e-mail notification when an order is successfully created.
   # email_success = 'false'
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    services = Service.objects.filter(cust_name=pk)
    products = Product.objects.filter(cust_name=pk)
    sum_service_charge = Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
    sum_product_charge = Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))

    context = {'products': products, 'customer': customer,
               'services': services,
               'sum_service_charge': sum_service_charge,
               'sum_product_charge': sum_product_charge, }

    message = 'Dear ' + customer.cust_name + ', Maverick Food Service Summary.'
    subject = 'Maverick Food Service Customer Summary : ' + str(customer.cust_name)
    #to_email_id = request.user.email

    summarypdf = generate_summary_pdf(request, pk, context)
    summaryFileName = 'Summary_' + str(customer.cust_name) + '.pdf'
    #msg = EmailMessage(subject, message, from_email="mavstaruno@gmail.com", to=['manushah@unomaha.edu'])
    #msg.attach(summaryFileName, summarypdf, 'application/pdf')
    # msg.content_subtype = "html"
    #msg.send()
    #email_success = 'true'
    return render(request, 'crm/summary.html', {'customer': customer,
                                                'products': products,
                                                'services': services,
                                                'sum_service_charge': sum_service_charge,
                                                'sum_product_charge': sum_product_charge})
                                                #'email_success': email_success})
    #return redirect('crm:home')"""

#class admin_summary_pdf(View):
def admin_summary_pdf(request, pk):
        template = get_template('crm/pdf.html')
        customer = get_object_or_404(Customer, pk=pk)
        customers = Customer.objects.filter(created_date__lte=timezone.now())
        services = Service.objects.filter(cust_name=pk)
        products = Product.objects.filter(cust_name=pk)
        sum_service_charge = Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
        sum_product_charge = Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))
        context = {'products': products, 'customer': customer,
                   'services': services,
                   'sum_service_charge': sum_service_charge,
                   'sum_product_charge': sum_product_charge, }
        html = template.render(context)

        # 'email_success': email_success})
        pdf = render_to_pdf('crm/pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = 'Summary_' + str(customer.cust_name) + '.pdf'
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("not found")

@login_required
def generate_summary_pdf(request, pk, context):
    customer = get_object_or_404(Customer, pk=pk)
    template = get_template('crm/pdf.html')

    html = template.render(context)
    pdf = render_to_pdf('crm/pdf.html', context)
    if pdf:
        response =  HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename= "summary_{}.pdf"'.format(customer.cust_name)
        #return response
        #return HttpResponse(pdf, content_type='application/octet-stream')
        return pdf
    return HttpResponse("Not Found")