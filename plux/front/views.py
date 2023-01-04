from django.shortcuts import render, redirect
from decimal import Decimal
from django.http import HttpResponse
from .decorators import login_required
from django.core.mail import send_mail
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from front.backends import AuthBackend
from . import models
from django.db.models import Count, Sum
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
import environ
import os
import json
from plux.settings import MEDIA_ROOT
from plux import settings
from django.core.files.storage import FileSystemStorage
import csv
import math
import random

from decimal import Decimal
env = environ.Env()
environ.Env.read_env()

# Create your views here.


def changePassword(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        newpassword = request.POST['newpassword']
        renewpassword = request.POST['renewpassword']
        user = models.User.objects.filter(email=email).first()
        if user is None:
            messages.error(request, 'User not found by this email.')
            return redirect('myProfile')
        if newpassword == renewpassword:
            if check_password(password, user.password) == True:
                user.pswd_token = newpassword
                user.password = make_password(newpassword)
                user.save()
                messages.success(request, 'Passord Updated.')
                return redirect('myProfile')
            else:
                messages.error(request, 'Wrong Password Provided.')
                return redirect('myProfile')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('myProfile')


def index(request):
    return HttpResponse("Hello, world. You're at the Front index.")


def getTransactionType(request):
    if request.method == "POST":
        context = {}
        transaction_type = request.POST['transaction_type_id']
        if int(transaction_type) == 1:
            vendors = models.VendorMaster.objects.filter(deleted=0)
            stores = models.StoreMaster.objects.filter(deleted=0)
            items = models.ItemMaster.objects.filter(deleted=0)
            context.update(
                {'vendors': vendors, 'stores': stores, 'items': items})
            return JsonResponse({
                'code': 200,
                'status': "SUCCESS",
                'transactionType': render_to_string('transactionType/receipt.html', context)
            })
        elif int(transaction_type) == 2:
            return JsonResponse({
                'code': 200,
                'status': "SUCCESS",
                'transactionType': render_to_string('transactionType/issue.html', context)
            })
        elif int(transaction_type) == 3:
            return JsonResponse({
                'code': 200,
                'status': "SUCCESS",
                'transactionType': render_to_string('transactionType/return.html', context)
            })
        elif int(transaction_type) == 4:
            stores = models.StoreMaster.objects.filter(deleted=0)
            context.update({'stores': stores})
            return JsonResponse({
                'code': 200,
                'status': "SUCCESS",
                'transactionType': render_to_string('transactionType/transferOut.html', context)
            })
        elif int(transaction_type) == 5:
            onTransitOrders = models.OnTransitHeader.objects.filter(
                deleted=0).exclude(status=3)
            context.update({'onTransitOrders': onTransitOrders})
            return JsonResponse({
                'code': 200,
                'status': "SUCCESS",
                'transactionType': render_to_string('transactionType/transferIn.html', context)
            })
        elif int(transaction_type) == 6:
            stores = models.StoreMaster.objects.filter(deleted=0)
            context.update({'stores': stores})
            return JsonResponse({
                'code': 200,
                'status': "SUCCESS",
                'transactionType': render_to_string('transactionType/physicalStock.html', context)
            })
        else:
            return JsonResponse({
                'code': 506,
                'status': "ERROR",
                'message': "Transaction Type not found."
            })
    else:
        return JsonResponse({
            'code': 505,
            'status': "ERROR",
            'message': "There should be ajax method."
        })


def getInvoiceType(request):
    if request.method == "POST":
        context = {}
        customer_id = request.POST['customer_id']
        invoice_type = request.POST['invoice_type']
        customer = models.Customer.objects.get(pk=customer_id)
        if invoice_type != "gst":
            stores = models.StoreMaster.objects.filter(deleted=0)
            terms = models.StandardTermMaster.objects.filter(deleted=0)
            sales_orders = list(models.SalesOrderHeader.objects.filter(
                customer_id=customer_id, deleted=0).exclude(status__in=[3]).values('id', 'sales_order_no'))
            invoicePayments = models.InvoicePayments.objects.filter(
                customer_id=customer.id).exclude(status=3)
            due_amount = 0
            for invoicePayment in invoicePayments:
                due_amount += (invoicePayment.total_amount -
                               invoicePayment.paid_amount)
            context.update({'stores': stores, 'terms': terms,
                           'sales_orders': sales_orders, 'due_amount': due_amount})
            return JsonResponse({
                'code': 200,
                'status': "SUCCESS",
                'invoiceType': render_to_string('invoiceType/nonGst.html', context)
            })
        else:
            if customer.state.name.lower() == env("CLIENT_STATE").lower():
                stores = models.StoreMaster.objects.filter(deleted=0)
                terms = models.StandardTermMaster.objects.filter(deleted=0)
                sales_orders = list(models.SalesOrderHeader.objects.filter(
                    customer_id=customer_id, deleted=0).exclude(status__in=[3]).values('id', 'sales_order_no'))
                invoicePayments = models.InvoicePayments.objects.filter(
                    customer_id=customer.id).exclude(status=3)
                due_amount = 0
                for invoicePayment in invoicePayments:
                    due_amount += (invoicePayment.total_amount -
                                   invoicePayment.paid_amount)
                context.update({'stores': stores, 'terms': terms,
                                'sales_orders': sales_orders, 'due_amount': due_amount})
                return JsonResponse({
                    'code': 200,
                    'status': "SUCCESS",
                    'invoiceType': render_to_string('invoiceType/stateSame.html', context)
                })
            else:
                stores = models.StoreMaster.objects.filter(deleted=0)
                terms = models.StandardTermMaster.objects.filter(deleted=0)
                sales_orders = list(models.SalesOrderHeader.objects.filter(
                    customer_id=customer_id, deleted=0).exclude(status__in=[3]).values('id', 'sales_order_no'))
                invoicePayments = models.InvoicePayments.objects.filter(
                    customer_id=customer.id).exclude(status=3)
                due_amount = 0
                for invoicePayment in invoicePayments:
                    due_amount += (invoicePayment.total_amount -
                                   invoicePayment.paid_amount)
                context.update({'stores': stores, 'terms': terms,
                               'sales_orders': sales_orders, 'due_amount': due_amount})
                return JsonResponse({
                    'code': 200,
                    'status': "SUCCESS",
                    'invoiceType': render_to_string('invoiceType/stateDifferent.html', context)
                })
    else:
        return JsonResponse({
            'code': 514,
            'status': "ERROR",
            'message': "There should be ajax method."
        })


@login_required
def getExceptStores(request):
    if request.method == "POST":
        store_from_id = request.POST['store_from_id']
        exceptStore = list(models.StoreMaster.objects.filter(
            deleted=0).exclude(id=store_from_id).values('id', 'name'))
        storeItems = list(models.StoreItemMaster.objects.filter(
            deleted=0, store_id=store_from_id, on_hand_qty__gt=0).values('id', 'item_id', 'on_hand_qty', 'item__description'))
        return JsonResponse({
            'code': 200,
            'status': 'SUCCESS',
            'exceptStore': exceptStore,
            'storeItems': storeItems
        })
    else:
        return JsonResponse({
            'code': 507,
            'status': "ERROR",
            'message': "There should be ajax method."
        })


@login_required
def getItemsDetailsByStore(request):
    if request.method == "POST":
        store_from_id = request.POST['store_from_id']
        store_item = request.POST['store_item']
        storeItem = list(models.StoreItemMaster.objects.filter(store_id=store_from_id, item_id=store_item).values(
            'id', 'on_hand_qty', 'item__unit_price', 'item__gst_percentage'))[0]
        return JsonResponse({
            'code': 200,
            'status': 'SUCCESS',
            'storeItems': storeItem
        })
    else:
        return JsonResponse({
            'code': 508,
            'status': "ERROR",
            'message': "There should be ajax method."
        })


@login_required
def getExceptedStoreItems(request):
    if request.method == "POST":
        store_id = request.POST['store_id']
        existing_items = models.StoreItemMaster.objects.filter(
            store_id=store_id, deleted=0).values('item_id')
        item_ids = []
        for ei in existing_items:
            item_ids.append(ei['item_id'])
        items = list(models.ItemMaster.objects.exclude(
            id__in=item_ids).values('id', 'description', 'unit_price'))
        return JsonResponse({
            'code': 200,
            'status': 'SUCCESS',
            'items': items
        })
    else:
        return JsonResponse({
            'code': 511,
            'status': "ERROR",
            'message': "There should be ajax method."
        })


@login_required
def getTransferDetails(request):
    if request.method == "POST":
        transfer_number = request.POST['transfer_number']
        onTransitHeader = list(models.OnTransitHeader.objects.filter(id=transfer_number).values(
            'id', 'transfer_number', 'transfer_date', 'store_from_id', 'store_from__name', 'store_to_id', 'store_to__name'))[0]
        onTransitDetails = list(models.OnTransitDetails.objects.filter(deleted=0, on_transit_header_id=transfer_number).values(
            'id', 'quantity', 'item__description', 'item_id', 'delivered_quantity'))
        items = list(models.ItemMaster.objects.filter(
            deleted=0).values('id', 'description'))
        return JsonResponse({
            'code': 200,
            'status': 'SUCCESS',
            'onTransitHeader': onTransitHeader,
            'onTransitDetails': onTransitDetails,
            'items': items
        })
    else:
        return JsonResponse({
            'code': 512,
            'status': "ERROR",
            'message': "There should be ajax method."
        })


@login_required
def getItemDetails(request):
    if request.method == "POST":
        item_id = request.POST['item_id']
        itemDetails = list(models.ItemMaster.objects.filter(
            id=item_id).values('id', 'description', 'unit_price'))[0]
        return JsonResponse({
            'code': 200,
            'status': 'SUCCESS',
            'itemDetails': itemDetails
        })
    else:
        return JsonResponse({
            'code': 513,
            'status': "ERROR",
            'message': "There should be ajax method."
        })


def signin(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser == 1 and request.user.is_active == 1:
            login(request, request.user)
            return redirect('dashboard')
        else:
            return redirect('signout')
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = AuthBackend.authenticate(
            request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Please Provide Valid Credentials.')
            return redirect('signin')
    return render(request, 'signin.html', context)

# class forgot(views):
#     def get(self, request):
#         return render(request, "forgot_password.html")


def forgot(request):
    context={}
    if request.method == "POST":
        email = request.POST['email']
        user = models.User.objects.filter(email=email).first()
        if user is not None:
            digits = [i for i in range(0, 10)]
            otp = ""
            for i in range(6):
                index = math.floor(random.random() * 10)
                otp += str(digits[index])
            request.session['OTP'] = otp
            request.session['FORGOT_EMAIL'] = email
            subject = 'OTP for Password Reset'
            message = otp
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email']]
            print(request.session['OTP'])
            print(request.session['FORGOT_EMAIL'])
            # send_mail(subject, message, email_from, recipient_list)
            return redirect('enter_otp')
        else:
            messages.error(request, 'User not found by this email.')
            return redirect('forgot')
    return render(request, "forgot_password.html", context)


# class enter_otp(View):
#     def get(self, request):
#         return render(request, "enter_otp.html")

def enter_otp(request):
    context={}
    if request.method == "POST":
        if (request.POST['verify_otp'] == request.session['OTP']):
            messages.success(request, "OTP verified!!")
            return redirect('password_reset')
        else:
            messages.error(request, "OTP is not correct")
            return redirect('enter_otp')
    return render(request, "enter_otp.html", context)


def password_reset(request):
    context={}
    if request.method == "POST":
        if (request.POST['password'] == request.POST['confirmpassword']):
            user = models.User.objects.get(
                email=request.session['FORGOT_EMAIL'])
            user.pswd_token = request.POST['password']
            user.password = make_password(request.POST['password'])
            user.save()
            try:
                del request.session
            except:
                pass
            messages.success(request, "Password updated!!")
            return redirect('signin')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('password_reset')
    return render(request, "password_reset.html", context)


def signup(request):
    context = {}
    if request.method == "POST":
        try:
            exist_email = models.User.objects.get(email=request.POST['email'])
        except:
            exist_email = None
        if exist_email is None:
            user = models.User()
            user.username = request.POST['email']
            user.email = request.POST['email']
            user.phone = request.POST['phone']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.pswd_token = request.POST['password']
            user.password = make_password(request.POST['password'])
            user.is_superuser = 0
            user.is_active = 1
            user.date_joined = datetime.now()
            user.save()
            messages.success(
                request, 'Thank you for registering. Please Signin and continue to dashboard')
            return redirect('signin')
        else:
            messages.error(request, 'This Email is already exists.')
            return redirect('signup')
    return render(request, 'signup.html', context)


def signout(request):
    logout(request)
    try:
        del request.session
    except:
        pass
    try:
        storage = get_messages(request)
        for message in storage:
            message = ''
        storage.used = False
    except:
        pass
    messages.warning(request, 'Logout Successfully.')
    return redirect('signin')


def top5(request):
    top_items = models.InvoiceDetails.objects.values(
        'item_id', 'item__description', 'item__unit_price').annotate(item_count=Count('item_id')).order_by('-item_count')[:5]
    top_5_items = []
    for elem in top_items:
        single_item_row = {}
        single_item_row['name'] = elem['item__description']
        single_item_row['y'] = elem['item_count']
        top_5_items.append(single_item_row)

    top_customers = models.InvoiceHeader.objects.values('customer_id', 'customer__customer_name', 'customer__contact_email').annotate(customer_amount=Sum('total_amount')).order_by('-customer_amount')[:5]
    top_5_customers = []
    for elem in top_customers:
        single_customer_row = {}
        single_customer_row['name'] = elem['customer__customer_name']
        single_customer_row['y'] = float(elem['customer_amount'])
        top_5_customers.append(single_customer_row)

    top_sales_persons = models.SalesOrderHeader.objects.values('sales_person_id', 'sales_person__salesperson_name', 'sales_person__contact_email').annotate(sales_person_amount=Sum('total_amount')).order_by('-sales_person_amount')[:5]
    top_5_sales_person = []
    for item in top_sales_persons:
        sales_persons = {}
        sales_persons['name'] = item['sales_person__salesperson_name']
        sales_persons['id'] = item['sales_person_id']
        sales_persons['data'] = []
        top_5_sales_person.append(sales_persons)

    now = datetime.now()
    result = [now.strftime("%b %Y")]
    for _ in range(0, 11):
        now = now.replace(day=1) - timedelta(days=1)
        result.insert(0, now.strftime("%b %Y"))
    
    for elem in top_5_sales_person:
        for month in result:
            amount_value = models.SalesOrderHeader.objects.filter(sales_person_id=elem['id'], sales_order_date__year=datetime.strptime(month, '%b %Y').strftime("%Y"), sales_order_date__month=datetime.strptime(month, '%b %Y').strftime("%m")).values('sales_person_id').annotate(sales_person_amount=Sum('total_amount')).first()
            if amount_value is not None:
                elem['data'].append(float(amount_value['sales_person_amount']))
            else:
                elem['data'].append(0)
    top_5_salesman = {}
    top_5_salesman['categories'] = result
    top_5_salesman['series'] = top_5_sales_person
    return JsonResponse({'top_5_items': top_5_items, 'top_5_customers': top_5_customers, 'top_5_salesman': top_5_salesman})


@login_required
def dashboard(request):
    context = {}
    return render(request, 'dashboard.html', context)


@login_required
def myProfile(request):
    context = {}
    return render(request, 'my_profile.html', context)


@login_required
def customerList(request):
    page = request.GET.get('page', 1)
    customers = models.Customer.objects.filter(deleted=0)
    # paginator = Paginator(customers, env("PER_PAGE_DATA"))
    # customers = paginator.page(page)
    context = {'customers': customers}
    return render(request, 'customer/list.html', context)


@login_required
def customerAdd(request):
    context = {}
    countries = models.Countries.objects.filter(id=101)
    context.update({'countries': countries})
    if request.method == "POST":
        customer = models.Customer()
        customer.customer_name = request.POST['customer_name']
        customer.address_1 = request.POST['address_1']
        customer.address_2 = request.POST['address_2']
        customer.pin = request.POST['pin']
        customer.gst_no = request.POST['gst_no']
        customer.contact_no = request.POST['contact_no']
        customer.contact_name = request.POST['contact_name']
        customer.contact_email = request.POST['contact_email']
        customer.country_id = request.POST['country']
        customer.state_id = request.POST['state']
        customer.city_id = request.POST['city']
        customer.save()
        messages.success(request, 'Customer Created Successfully.')
        return redirect('customerList')
    return render(request, 'customer/add.html', context)


@login_required
def customerEdit(request, id):
    context = {}
    countries = models.Countries.objects.filter(id=101)
    customer = models.Customer.objects.get(pk=id)
    context.update({'countries': countries, 'customer': customer})
    if request.method == "POST":
        customer = models.Customer.objects.get(pk=request.POST['id'])
        customer.customer_name = request.POST['customer_name']
        customer.address_1 = request.POST['address_1']
        customer.address_2 = request.POST['address_2']
        customer.pin = request.POST['pin']
        customer.gst_no = request.POST['gst_no']
        customer.contact_no = request.POST['contact_no']
        customer.contact_name = request.POST['contact_name']
        customer.contact_email = request.POST['contact_email']
        customer.country_id = request.POST['country']
        customer.state_id = request.POST['state']
        customer.city_id = request.POST['city']
        customer.save()
        messages.success(request, 'Customer Updated Successfully.')
        return redirect('customerList')
    return render(request, 'customer/edit.html', context)


@login_required
def customerDelete(request, id):
    customer = models.Customer.objects.get(pk=id)
    customer.deleted = 1
    customer.save()
    return redirect('customerList')


@login_required
def customerImport(request):
    context = {}
    if request.method == "POST":
        customer_list = []
        if request.FILES.get('excel', None):
            file = request.FILES['excel']
            tmpname = str(datetime.now().microsecond) + \
                os.path.splitext(str(file))[1]
            fs = FileSystemStorage(
                MEDIA_ROOT + "excels/customers/", MEDIA_ROOT + "/excels/customers/")
            fs.save(tmpname, file)
            file_name = "excels/customers/" + tmpname

            with open(MEDIA_ROOT + file_name, newline='', mode='r', encoding='ISO-8859-1') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row['Customer Name']:
                        break
                    country_obj = models.Countries.objects.filter(
                        name=row['Country']).first()
                    state_obj = models.States.objects.filter(
                        name=row['State']).first()
                    city_obj = models.Cities.objects.filter(
                        name=row['City']).first()
                    country_id = country_obj.id if country_obj is not None else None
                    state_id = state_obj.id if state_obj is not None else None
                    city_id = city_obj.id if city_obj is not None else None
                    customer_email_qs = models.Customer.objects.filter(
                        contact_email=row['Contact Email'])
                    if (not customer_email_qs.exists()):
                        customer_list.append(models.Customer(customer_name=row['Customer Name'], address_1=row['Address 1'], address_2=row['Address 2'], gst_no=row['GST Number'], contact_no=row[
                                             'Contact Number'], contact_name=row['Contact Name'], contact_email=row['Contact Email'], pin=row['Pin'], country_id=country_id, state_id=state_id, city_id=city_id))
                models.Customer.objects.bulk_create(customer_list)
                csvfile.close()
                os.remove(MEDIA_ROOT + file_name)
            messages.success(request, 'Customers Created Successfully.')
            return redirect('customerList')
    return render(request, 'customer/import.html', context)


@login_required
def downloadCustomerExcel(request):
    file_path = (MEDIA_ROOT + "excels/downloadable/" + "customers.csv")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                # fh.read(), content_type="application/vnd.ms-excel")
                fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response


@login_required
def salespersonList(request):
    page = request.GET.get('page', 1)
    salespersons = models.SalesPerson.objects.filter(deleted=0)
    # paginator = Paginator(salespersons, env("PER_PAGE_DATA"))
    # salespersons = paginator.page(page)
    context = {'salespersons': salespersons}
    return render(request, 'salesperson/list.html', context)


@login_required
def salespersonAdd(request):
    context = {}
    countries = models.Countries.objects.filter(id=101)
    context.update({'countries': countries})
    if request.method == "POST":
        salesperson = models.SalesPerson()
        salesperson.salesperson_name = request.POST['salesperson_name']
        salesperson.address_1 = request.POST['address_1']
        salesperson.address_2 = request.POST['address_2']
        salesperson.pin = request.POST['pin']
        salesperson.contact_no = request.POST['contact_no']
        salesperson.contact_name = request.POST['contact_name']
        salesperson.contact_email = request.POST['contact_email']
        salesperson.country_id = request.POST['country']
        salesperson.state_id = request.POST['state']
        salesperson.city_id = request.POST['city']
        salesperson.save()
        messages.success(request, 'Salesperson Created Successfully.')
        return redirect('salespersonList')
    return render(request, 'salesperson/add.html', context)


@login_required
def salespersonEdit(request, id):
    context = {}
    countries = models.Countries.objects.filter(id=101)
    salesperson = models.SalesPerson.objects.get(pk=id)
    context.update({'countries': countries, 'salesperson': salesperson})
    if request.method == "POST":
        salesperson = models.SalesPerson.objects.get(pk=request.POST['id'])
        salesperson.salesperson_name = request.POST['salesperson_name']
        salesperson.address_1 = request.POST['address_1']
        salesperson.address_2 = request.POST['address_2']
        salesperson.pin = request.POST['pin']
        salesperson.contact_no = request.POST['contact_no']
        salesperson.contact_name = request.POST['contact_name']
        salesperson.contact_email = request.POST['contact_email']
        salesperson.country_id = request.POST['country']
        salesperson.state_id = request.POST['state']
        salesperson.city_id = request.POST['city']
        salesperson.save()
        messages.success(request, 'Salesperson Updated Successfully.')
        return redirect('salespersonList')
    return render(request, 'salesperson/edit.html', context)


@login_required
def salespersonDelete(request, id):
    salesperson = models.SalesPerson.objects.get(pk=id)
    salesperson.deleted = 1
    salesperson.save()
    return redirect('salespersonList')


@login_required
def salespersonImport(request):
    context = {}
    if request.method == "POST":
        salesperson_list = []
        if request.FILES.get('excel', None):
            file = request.FILES['excel']
            tmpname = str(datetime.now().microsecond) + \
                os.path.splitext(str(file))[1]
            fs = FileSystemStorage(
                MEDIA_ROOT + "excels/salespersons/", MEDIA_ROOT + "/excels/salespersons/")
            fs.save(tmpname, file)
            file_name = "excels/salespersons/" + tmpname

            with open(MEDIA_ROOT + file_name, newline='', mode='r', encoding='ISO-8859-1') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row['Salesperson Name']:
                        break
                    country_obj = models.Countries.objects.filter(
                        name=row['Country']).first()
                    state_obj = models.States.objects.filter(
                        name=row['State']).first()
                    city_obj = models.Cities.objects.filter(
                        name=row['City']).first()
                    country_id = country_obj.id if country_obj is not None else None
                    state_id = state_obj.id if state_obj is not None else None
                    city_id = city_obj.id if city_obj is not None else None
                    salesperson_email_qs = models.SalesPerson.objects.filter(
                        contact_email=row['Contact Email'])
                    if (not salesperson_email_qs.exists()):
                        salesperson_list.append(models.SalesPerson(salesperson_name=row['Salesperson Name'], address_1=row['Address 1'], address_2=row['Address 2'], contact_no=row[
                                                'Contact Number'], contact_name=row['Contact Name'], contact_email=row['Contact Email'], pin=row['Pin'], country_id=country_id, state_id=state_id, city_id=city_id))
                models.SalesPerson.objects.bulk_create(salesperson_list)
                csvfile.close()
                os.remove(MEDIA_ROOT + file_name)
            messages.success(request, 'Salespersons Created Successfully.')
            return redirect('salespersonList')
    return render(request, 'salesperson/import.html', context)


@login_required
def downloadSalespersonExcel(request):
    file_path = (MEDIA_ROOT + "excels/downloadable/" + "salespersons.csv")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                # fh.read(), content_type="application/vnd.ms-excel")
                fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response


@login_required
def userList(request):
    page = request.GET.get('page', 1)
    users = models.User.objects.all()
    # paginator = Paginator(users, env("PER_PAGE_DATA"))
    # users = paginator.page(page)
    context = {'users': users}
    return render(request, 'user/list.html', context)


@login_required
def vendorList(request):
    page = request.GET.get('page', 1)
    vendors = models.VendorMaster.objects.filter(deleted=0)
    # paginator = Paginator(vendors, env("PER_PAGE_DATA"))
    # vendors = paginator.page(page)
    context = {'vendors': vendors}
    return render(request, 'vendor/list.html', context)


@login_required
def vendorAdd(request):
    context = {}
    countries = models.Countries.objects.filter(id=101)
    context.update({'countries': countries})
    if request.method == "POST":
        vendor = models.VendorMaster()
        vendor.name = request.POST['name']
        vendor.address_1 = request.POST['address_1']
        vendor.address_2 = request.POST['address_2']
        vendor.pin = request.POST['pin']
        vendor.gst_no = request.POST['gst_no']
        vendor.contact_no = request.POST['contact_no']
        vendor.contact_name = request.POST['contact_name']
        vendor.contact_email = request.POST['contact_email']
        vendor.city_id = request.POST['city']
        vendor.country_id = request.POST['country']
        vendor.state_id = request.POST['state']
        vendor.save()
        messages.success(request, 'vendor Created Successfully.')
        return redirect('vendorList')
    return render(request, 'vendor/add.html', context)


@login_required
def vendorEdit(request, id):
    context = {}
    countries = models.Countries.objects.filter(id=101)
    vendor = models.VendorMaster.objects.get(pk=id)
    context.update({'countries': countries, 'vendor': vendor})
    if request.method == "POST":
        vendor = models.VendorMaster.objects.get(pk=request.POST['id'])
        vendor.name = request.POST['name']
        vendor.address_1 = request.POST['address_1']
        vendor.address_2 = request.POST['address_2']
        vendor.pin = request.POST['pin']
        vendor.gst_no = request.POST['gst_no']
        vendor.contact_no = request.POST['contact_no']
        vendor.contact_name = request.POST['contact_name']
        vendor.contact_email = request.POST['contact_email']
        vendor.country_id = request.POST['country']
        vendor.state_id = request.POST['state']
        vendor.city_id = request.POST['city']
        vendor.save()
        messages.success(request, 'vendor Updated Successfully.')
        return redirect('vendorList')
    return render(request, 'vendor/edit.html', context)


@login_required
def vendorDelete(request, id):
    vendor = models.VendorMaster.objects.get(pk=id)
    vendor.deleted = 1
    vendor.save()
    return redirect('vendorList')


@login_required
def vendorImport(request):
    context = {}
    if request.method == "POST":
        vendor_list = []
        if request.FILES.get('excel', None):
            file = request.FILES['excel']
            tmpname = str(datetime.now().microsecond) + \
                os.path.splitext(str(file))[1]
            fs = FileSystemStorage(
                MEDIA_ROOT + "excels/vendors/", MEDIA_ROOT + "/excels/vendors/")
            fs.save(tmpname, file)
            file_name = "excels/vendors/" + tmpname

            with open(MEDIA_ROOT + file_name, newline='', mode='r', encoding='ISO-8859-1') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row['Name']:
                        break
                    country_obj = models.Countries.objects.filter(
                        name=row['Country']).first()
                    state_obj = models.States.objects.filter(
                        name=row['State']).first()
                    city_obj = models.Cities.objects.filter(
                        name=row['City']).first()
                    country_id = country_obj.id if country_obj is not None else None
                    state_id = state_obj.id if state_obj is not None else None
                    city_id = city_obj.id if city_obj is not None else None
                    vendor_email_qs = models.VendorMaster.objects.filter(
                        contact_email=row['Contact Email'])
                    if (not vendor_email_qs.exists()):
                        vendor_list.append(models.VendorMaster(name=row['Name'], address_1=row['Address 1'], address_2=row['Address 2'], gst_no=row['GST Number'], contact_no=row[
                            'Contact Number'], contact_name=row['Contact Name'], contact_email=row['Contact Email'], pin=row['Pin'], country_id=country_id, state_id=state_id, city_id=city_id))
                models.VendorMaster.objects.bulk_create(vendor_list)
                csvfile.close()
                os.remove(MEDIA_ROOT + file_name)
            messages.success(request, 'Vendors Created Successfully.')
            return redirect('vendorList')
    return render(request, 'vendor/import.html', context)


@login_required
def downloadVendorExcel(request):
    file_path = (MEDIA_ROOT + "excels/downloadable/" + "vendors.csv")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                # fh.read(), content_type="application/vnd.ms-excel")
                fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response


@login_required
def storeList(request):
    page = request.GET.get('page', 1)
    stores = models.StoreMaster.objects.filter(deleted=0)
    # paginator = Paginator(stores, env("PER_PAGE_DATA"))
    # stores = paginator.page(page)
    context = {'stores': stores}
    return render(request, 'store/list.html', context)


@login_required
def storeAdd(request):
    context = {}
    countries = models.Countries.objects.filter(id=101)
    context.update({'countries': countries})
    if request.method == "POST":
        store = models.StoreMaster()
        store.name = request.POST['name']
        store.address_1 = request.POST['address_1']
        store.address_2 = request.POST['address_2']
        store.pin = request.POST['pin']
        store.gst_no = request.POST['gst_no']
        store.contact_no = request.POST['contact_no']
        store.contact_name = request.POST['contact_name']
        store.contact_email = request.POST['contact_email']
        store.manager_name = request.POST['manager_name']
        store.city_id = request.POST['city']
        store.country_id = request.POST['country']
        store.state_id = request.POST['state']
        store.save()
        messages.success(request, 'store Created Successfully.')
        return redirect('storeList')
    return render(request, 'store/add.html', context)


@login_required
def storeEdit(request, id):
    context = {}
    countries = models.Countries.objects.filter(id=101)
    store = models.StoreMaster.objects.get(pk=id)
    context.update({'countries': countries, 'store': store})
    if request.method == "POST":
        store = models.StoreMaster.objects.get(pk=request.POST['id'])
        store.name = request.POST['name']
        store.address_1 = request.POST['address_1']
        store.address_2 = request.POST['address_2']
        store.pin = request.POST['pin']
        store.gst_no = request.POST['gst_no']
        store.contact_no = request.POST['contact_no']
        store.contact_name = request.POST['contact_name']
        store.contact_email = request.POST['contact_email']
        store.manager_name = request.POST['manager_name']
        store.country_id = request.POST['country']
        store.state_id = request.POST['state']
        store.city_id = request.POST['city']
        store.save()
        messages.success(request, 'store Updated Successfully.')
        return redirect('storeList')
    return render(request, 'store/edit.html', context)


@login_required
def storeDelete(request, id):
    store = models.StoreMaster.objects.get(pk=id)
    store.deleted = 1
    store.save()
    return redirect('storeList')


@login_required
def storeImport(request):
    context = {}
    if request.method == "POST":
        store_list = []
        if request.FILES.get('excel', None):
            file = request.FILES['excel']
            tmpname = str(datetime.now().microsecond) + \
                os.path.splitext(str(file))[1]
            fs = FileSystemStorage(
                MEDIA_ROOT + "excels/stores/", MEDIA_ROOT + "/excels/stores/")
            fs.save(tmpname, file)
            file_name = "excels/stores/" + tmpname

            with open(MEDIA_ROOT + file_name, newline='', mode='r', encoding='ISO-8859-1') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row['Store Name']:
                        break
                    country_obj = models.Countries.objects.filter(
                        name=row['Country']).first()
                    state_obj = models.States.objects.filter(
                        name=row['State']).first()
                    city_obj = models.Cities.objects.filter(
                        name=row['City']).first()
                    country_id = country_obj.id if country_obj is not None else None
                    state_id = state_obj.id if state_obj is not None else None
                    city_id = city_obj.id if city_obj is not None else None
                    store_email_qs = models.StoreMaster.objects.filter(
                        contact_email=row['Contact Email'])
                    if (not store_email_qs.exists()):
                        store_list.append(models.StoreMaster(name=row['Store Name'], address_1=row['Address 1'], address_2=row['Address 2'], pin=row['Pin'], gst_no=row['GST Number'], contact_no=row[
                                          'Contact Number'], contact_name=row['Contact Name'], contact_email=row['Contact Email'], manager_name=row['Manager Name'], city_id=city_id, country_id=country_id, state_id=state_id))
                models.StoreMaster.objects.bulk_create(store_list)
                csvfile.close()
                os.remove(MEDIA_ROOT + file_name)
            messages.success(request, 'Stores Created Successfully.')
            return redirect('storeList')
    return render(request, 'store/import.html', context)


@login_required
def downloadStoreExcel(request):
    file_path = (MEDIA_ROOT + "excels/downloadable/" + "stores.csv")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                # fh.read(), content_type="application/vnd.ms-excel")
                fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response


def getStatesByCountry(request):
    if request.method == "POST":
        country_id = request.POST['country_id']
        states = list(models.States.objects.filter(
            country_id=country_id).values('id', 'name'))
        return JsonResponse({
            'code': 200,
            'status': 'SUCCESS',
            'data': states
        })
    else:
        return JsonResponse({
            'code': 501,
            'status': 'ERROR',
            'message': 'There should be post method.'
        })


def getCitiesByState(request):
    if request.method == "POST":
        state_id = request.POST['state_id']
        cities = list(models.Cities.objects.filter(
            state_id=state_id).values('id', 'name'))
        return JsonResponse({
            'code': 200,
            'status': 'SUCCESS',
            'data': cities
        })
    else:
        return JsonResponse({
            'code': 502,
            'status': 'ERROR',
            'message': 'There should be post method.'
        })


@login_required
def uomList(request):
    page = request.GET.get('page', 1)
    uoms = models.UomMaster.objects.filter(deleted=0)
    # paginator = Paginator(uoms, env("PER_PAGE_DATA"))
    # uoms = paginator.page(page)
    context = {'uoms': uoms}
    return render(request, 'uom/list.html', context)


@login_required
def uomAdd(request):
    context = {}
    if request.method == "POST":
        uom = models.UomMaster()
        uom.description = request.POST['description']
        uom.save()
        messages.success(request, 'UOM Created Successfully.')
        return redirect('uomList')
    return render(request, 'uom/add.html', context)


@login_required
def uomEdit(request, id):
    context = {}
    uom = models.UomMaster.objects.get(pk=id)
    context.update({'uom': uom})
    if request.method == "POST":
        uom = models.UomMaster.objects.get(pk=request.POST['id'])
        uom.description = request.POST['description']
        uom.save()
        messages.success(request, 'UOM Updated Successfully.')
        return redirect('uomList')
    return render(request, 'uom/edit.html', context)


@login_required
def uomDelete(request, id):
    uom = models.UomMaster.objects.get(pk=id)
    uom.deleted = 1
    uom.save()
    return redirect('uomList')


@login_required
def uomImport(request):
    context = {}
    if request.method == "POST":
        uom_list = []
        if request.FILES.get('excel', None):
            file = request.FILES['excel']
            tmpname = str(datetime.now().microsecond) + \
                os.path.splitext(str(file))[1]
            fs = FileSystemStorage(
                MEDIA_ROOT + "excels/uoms/", MEDIA_ROOT + "/excels/uoms/")
            fs.save(tmpname, file)
            file_name = "excels/uoms/" + tmpname

            with open(MEDIA_ROOT + file_name, newline='', mode='r', encoding='ISO-8859-1') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    uom_list.append(models.UomMaster(
                        description=row['Description']))
                models.UomMaster.objects.bulk_create(uom_list)
                csvfile.close()
                os.remove(MEDIA_ROOT + file_name)
            messages.success(request, 'Uoms Created Successfully.')
            return redirect('uomList')
    return render(request, 'uom/import.html', context)


@login_required
def downloadUomExcel(request):
    file_path = (MEDIA_ROOT + "excels/downloadable/" + "uoms.csv")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response


@login_required
def itemCategoryList(request):
    page = request.GET.get('page', 1)
    itemCategories = models.ItemCtegory.objects.filter(deleted=0)
    # paginator = Paginator(itemCategories, env("PER_PAGE_DATA"))
    # itemCategories = paginator.page(page)
    context = {'itemCategories': itemCategories}
    return render(request, 'itemCategory/list.html', context)


@login_required
def itemCategoryAdd(request):
    context = {}
    if request.method == "POST":
        itemCategory = models.ItemCtegory()
        itemCategory.description = request.POST['description']
        itemCategory.save()
        messages.success(request, 'Item Category Created Successfully.')
        return redirect('itemCategoryList')
    return render(request, 'itemCategory/add.html', context)


@login_required
def itemCategoryEdit(request, id):
    context = {}
    itemCategory = models.ItemCtegory.objects.get(pk=id)
    context.update({'itemCategory': itemCategory})
    if request.method == "POST":
        itemCategory = models.ItemCtegory.objects.get(pk=request.POST['id'])
        itemCategory.description = request.POST['description']
        itemCategory.save()
        messages.success(request, 'Item Category Updated Successfully.')
        return redirect('itemCategoryList')
    return render(request, 'itemCategory/edit.html', context)


@login_required
def itemCategoryDelete(request, id):
    itemCategory = models.ItemCtegory.objects.get(pk=id)
    itemCategory.deleted = 1
    itemCategory.save()
    return redirect('itemCategoryList')


@login_required
def itemCategoryImport(request):
    context = {}
    if request.method == "POST":
        itemCategory_list = []
        if request.FILES.get('excel', None):
            file = request.FILES['excel']
            tmpname = str(datetime.now().microsecond) + \
                os.path.splitext(str(file))[1]
            fs = FileSystemStorage(
                MEDIA_ROOT + "excels/item categories/", MEDIA_ROOT + "/excels/item categories/")
            fs.save(tmpname, file)
            file_name = "excels/item categories/" + tmpname

            with open(MEDIA_ROOT + file_name, newline='', mode='r', encoding='ISO-8859-1') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    itemCategory_list.append(models.ItemCtegory(
                        description=row['Description']))
                models.ItemCtegory.objects.bulk_create(itemCategory_list)
                csvfile.close()
                os.remove(MEDIA_ROOT + file_name)
            messages.success(request, 'Item categories Created Successfully.')
            return redirect('itemCategoryList')
    return render(request, 'itemCategory/import.html', context)


@login_required
def downloaditemCategoryExcel(request):
    file_path = (MEDIA_ROOT + "excels/downloadable/" + "item categories.csv")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response


@login_required
def plyDimensionList(request):
    page = request.GET.get('page', 1)
    plyDimensions = models.PlyDimensionMaster.objects.filter(deleted=0)
    # paginator = Paginator(plyDimensions, env("PER_PAGE_DATA"))
    # plyDimensions = paginator.page(page)
    context = {'plyDimensions': plyDimensions}
    return render(request, 'plyDimension/list.html', context)


@login_required
def plyDimensionAdd(request):
    context = {}
    if request.method == "POST":
        plyDimension = models.PlyDimensionMaster()
        plyDimension.description = request.POST['description']
        plyDimension.length_ft = request.POST['length_ft']
        plyDimension.breadth_ft = request.POST['breadth_ft']
        plyDimension.length_mt = request.POST['length_mt']
        plyDimension.breadth_mt = request.POST['breadth_mt']
        plyDimension.square_ft = request.POST['square_ft']
        plyDimension.square_mt = request.POST['square_mt']
        plyDimension.save()
        messages.success(request, 'Ply Dimension Created Successfully.')
        return redirect('plyDimensionList')
    return render(request, 'plyDimension/add.html', context)


@login_required
def plyDimensionEdit(request, id):
    context = {}
    plyDimension = models.PlyDimensionMaster.objects.get(pk=id)
    context.update({'plyDimension': plyDimension})
    if request.method == "POST":
        plyDimension = models.PlyDimensionMaster.objects.get(
            pk=request.POST['id'])
        plyDimension.description = request.POST['description']
        plyDimension.length_ft = request.POST['length_ft']
        plyDimension.breadth_ft = request.POST['breadth_ft']
        plyDimension.length_mt = request.POST['length_mt']
        plyDimension.breadth_mt = request.POST['breadth_mt']
        plyDimension.square_ft = request.POST['square_ft']
        plyDimension.square_mt = request.POST['square_mt']
        plyDimension.save()
        messages.success(request, 'Ply Dimension Updated Successfully.')
        return redirect('plyDimensionList')
    return render(request, 'plyDimension/edit.html', context)


@login_required
def plyDimensionDelete(request, id):
    plyDimension = models.PlyDimensionMaster.objects.get(pk=id)
    plyDimension.deleted = 1
    plyDimension.save()
    return redirect('plyDimensionList')


@login_required
def plyDimensionImport(request):
    context = {}
    if request.method == "POST":
        plyDimension_list = []
        if request.FILES.get('excel', None):
            file = request.FILES['excel']
            tmpname = str(datetime.now().microsecond) + \
                os.path.splitext(str(file))[1]
            fs = FileSystemStorage(
                MEDIA_ROOT + "excels/ply dimensions/", MEDIA_ROOT + "/excels/ply dimensions/")
            fs.save(tmpname, file)
            file_name = "excels/ply dimensions/" + tmpname

            with open(MEDIA_ROOT + file_name, newline='', mode='r', encoding='ISO-8859-1') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    plyDimension_list.append(models.PlyDimensionMaster(description=row['Description'], length_ft=row['Length(Ft)'],
                                                                       breadth_ft=row['Breadth(Ft)'], length_mt=0.3048*float(
                                                                           row['Length(Ft)']),
                                                                       breadth_mt=0.3048*float(row['Breadth(Ft)']), square_ft=float(row['Length(Ft)'])*float(row['Breadth(Ft)']),
                                                                       square_mt=0.09290304*float(row['Length(Ft)'])*float(row['Breadth(Ft)'])))
                models.PlyDimensionMaster.objects.bulk_create(
                    plyDimension_list)
                csvfile.close()
                os.remove(MEDIA_ROOT + file_name)
            messages.success(request, 'Ply Dimension Created Successfully.')
            return redirect('plyDimensionList')
    return render(request, 'plyDimension/import.html', context)


@login_required
def downloadplyDimensionExcel(request):
    file_path = (MEDIA_ROOT + "excels/downloadable/" + "ply dimensions.csv")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                # fh.read(), content_type="application/vnd.ms-excel")
                fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response


@login_required
def itemList(request):
    page = request.GET.get('page', 1)
    items = models.ItemMaster.objects.filter(deleted=0)
    # paginator = Paginator(items, env("PER_PAGE_DATA"))
    # items = paginator.page(page)
    context = {'items': items}
    return render(request, 'item/list.html', context)


@login_required
def itemAdd(request):
    context = {}
    itemCategories = models.ItemCtegory.objects.filter(deleted=0)
    plyDimensions = models.PlyDimensionMaster.objects.filter(deleted=0)
    uoms = models.UomMaster.objects.filter(deleted=0)
    context.update({'itemCategories': itemCategories,
                   'plyDimensions': plyDimensions, 'uoms': uoms})
    if request.method == "POST":
        item = models.ItemMaster()
        item.description = request.POST['description']
        item.unit_price = request.POST['unit_price']
        item.hsn_code = request.POST['hsn_code']
        item.gst_percentage = request.POST['gst_percentage']
        item.item_category_id = request.POST['item_category_id']
        item.ply_dimension_id = request.POST['ply_dimension_id']
        item.uom_id = request.POST['uom_id']
        item.save()
        attribute_details = []
        for index, elem in enumerate(request.POST.getlist('attribute_name[]')):
            attribute_details.append(models.ItemAttributes(item_id=item.id, attribute_name=request.POST.getlist(
                'attribute_name[]')[index], attribute_value=request.POST.getlist('attribute_value[]')[index]))
        models.ItemAttributes.objects.bulk_create(attribute_details)
        messages.success(request, 'Item Created Successfully.')
        return redirect('itemList')
    return render(request, 'item/add.html', context)


@login_required
def itemEdit(request, id):
    context = {}
    item = models.ItemMaster.objects.prefetch_related(
        'itemattributes_set').get(pk=id)
    itemCategories = models.ItemCtegory.objects.filter(deleted=0)
    plyDimensions = models.PlyDimensionMaster.objects.filter(deleted=0)
    uoms = models.UomMaster.objects.filter(deleted=0)
    context.update({'item': item, 'itemCategories': itemCategories,
                   'plyDimensions': plyDimensions, 'uoms': uoms})
    if request.method == "POST":
        item = models.ItemMaster.objects.get(pk=request.POST['id'])
        item.description = request.POST['description']
        item.unit_price = request.POST['unit_price']
        item.hsn_code = request.POST['hsn_code']
        item.gst_percentage = request.POST['gst_percentage']
        item.item_category_id = request.POST['item_category_id']
        item.ply_dimension_id = request.POST['ply_dimension_id']
        item.uom_id = request.POST['uom_id']
        item.save()
        models.ItemAttributes.objects.filter(item_id=item.id).delete()
        attribute_details = []
        for index, elem in enumerate(request.POST.getlist('attribute_name[]')):
            attribute_details.append(models.ItemAttributes(item_id=item.id, attribute_name=request.POST.getlist(
                'attribute_name[]')[index], attribute_value=request.POST.getlist('attribute_value[]')[index]))
        models.ItemAttributes.objects.bulk_create(attribute_details)
        messages.success(request, 'Item Updated Successfully.')
        return redirect('itemList')
    return render(request, 'item/edit.html', context)


@login_required
def itemDelete(request, id):
    item = models.ItemMaster.objects.get(pk=id)
    item.deleted = 1
    item.save()
    return redirect('itemList')


@login_required
def itemImport(request):
    context = {}
    if request.method == "POST":
        item_list = []
        if request.FILES.get('excel', None):
            file = request.FILES['excel']
            tmpname = str(datetime.now().microsecond) + \
                os.path.splitext(str(file))[1]
            fs = FileSystemStorage(
                MEDIA_ROOT + "excels/items/", MEDIA_ROOT + "/excels/items/")
            fs.save(tmpname, file)
            file_name = "excels/items/" + tmpname

            with open(MEDIA_ROOT + file_name, newline='', mode='r', encoding='ISO-8859-1') as csvfile:
                reader = csv.DictReader(csvfile)
                item_list = []
                for row in reader:
                    item_category_obj = models.ItemCtegory.objects.filter(
                        description=row['Item Category']).first()
                    uom_obj = models.UomMaster.objects.filter(
                        description=row['UOM']).first()
                    ply_dimension_obj = models.PlyDimensionMaster.objects.filter(
                        description=row['Ply Dimension']).first()
                    if item_category_obj is None:
                        item_category_obj = models.ItemCtegory()
                        item_category_obj.description = row['Item Category']
                        item_category_obj.save()
                    if uom_obj is None:
                        uom_obj = models.UomMaster()
                        uom_obj.description = row['UOM']
                        uom_obj.save()
                    item_list.append(models.ItemMaster(description=row['Description'], item_category_id=item_category_obj.id, ply_dimension_id=ply_dimension_obj.id if ply_dimension_obj is not None else None,
                                     uom_id=uom_obj.id, unit_price=row['Unit Price'], hsn_code=row['HSN Code'], gst_percentage=row['GST %']))
                models.ItemMaster.objects.bulk_create(item_list)
                csvfile.close()
                os.remove(MEDIA_ROOT + file_name)
            messages.success(request, 'Items Created Successfully.')
            return redirect('itemList')
    return render(request, 'item/import.html', context)


@login_required
def downloadItemExcel(request):
    file_path = (MEDIA_ROOT + "excels/downloadable/" + "items.csv")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                # fh.read(), content_type="application/vnd.ms-excel")
                fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response


@login_required
def storeItemList(request):
    page = request.GET.get('page', 1)
    storeItems = models.StoreItemMaster.objects.filter(deleted=0)
    # paginator = Paginator(storeItems, env("PER_PAGE_DATA"))
    # storeItems = paginator.page(page)
    context = {'storeItems': storeItems}
    return render(request, 'storeItem/list.html', context)


@login_required
def storeItemAdd(request):
    context = {}
    stores = models.StoreMaster.objects.filter(deleted=0)
    # existing_items = models.StoreItemMaster.objects.filter(deleted=0).values('item_id')
    # item_ids = []
    # for ei in existing_items:
    #     item_ids.append(ei['item_id'])
    # items = models.ItemMaster.objects.filter(deleted=0).exclude(id__in=item_ids)
    context.update({'stores': stores})
    if request.method == "POST":
        storeItem = models.StoreItemMaster()
        storeItem.opening_qty = request.POST['opening_qty']
        # storeItem.on_hand_qty = request.POST['on_hand_qty']
        # storeItem.closing_qty = request.POST['closing_qty']
        storeItem.on_hand_qty = request.POST['opening_qty']
        storeItem.closing_qty = request.POST['opening_qty']
        storeItem.item_id = request.POST['item_id']
        storeItem.store_id = request.POST['store_id']
        storeItem.save()
        messages.success(request, 'Store Item Created Successfully.')
        return redirect('storeItemList')
    return render(request, 'storeItem/add.html', context)


@login_required
def storeItemEdit(request, id):
    context = {}
    storeItem = models.StoreItemMaster.objects.get(pk=id)
    stores = models.StoreMaster.objects.filter(deleted=0)
    items = models.ItemMaster.objects.filter(id=storeItem.item_id)
    context.update({'storeItem': storeItem, 'items': items, 'stores': stores})
    if request.method == "POST":
        storeItem = models.StoreItemMaster.objects.get(pk=request.POST['id'])
        storeItem.opening_qty = request.POST['opening_qty']
        # storeItem.on_hand_qty = request.POST['on_hand_qty']
        # storeItem.closing_qty = request.POST['closing_qty']
        storeItem.on_hand_qty = request.POST['opening_qty']
        storeItem.closing_qty = request.POST['opening_qty']
        # storeItem.item_id = request.POST['item_id']
        # storeItem.store_id = request.POST['store_id']
        storeItem.save()
        messages.success(request, 'Store Item Updated Successfully.')
        return redirect('storeItemList')
    return render(request, 'storeItem/edit.html', context)


@login_required
def storeItemDelete(request, id):
    storeItem = models.StoreItemMaster.objects.get(pk=id)
    storeItem.deleted = 1
    storeItem.save()
    return redirect('storeItemList')


@login_required
def storeItemImport(request):
    context = {}
    if request.method == "POST":
        storeItem_list = []
        if request.FILES.get('excel', None):
            file = request.FILES['excel']
            tmpname = str(datetime.now().microsecond) + \
                os.path.splitext(str(file))[1]
            fs = FileSystemStorage(
                MEDIA_ROOT + "excels/store items/", MEDIA_ROOT + "/excels/store items/")
            fs.save(tmpname, file)
            file_name = "excels/store items/" + tmpname

            with open(MEDIA_ROOT + file_name, newline='', mode='r', encoding='ISO-8859-1') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row['Store'] and not row['Item']:
                        break
                    store_obj = models.StoreMaster.objects.filter(
                        name=row['Store']).first()
                    item_obj = models.ItemMaster.objects.filter(
                        description=row['Item']).first()
                    store_id = store_obj.id if store_obj is not None else None
                    item_id = item_obj.id if item_obj is not None else None
                    storeItem_list.append(models.StoreItemMaster(store_id=store_id, item_id=item_id, opening_qty=Decimal(row['Opening Quantity']),
                                                                 on_hand_qty=Decimal(row['Opening Quantity']), closing_qty=Decimal(row['Opening Quantity'])))
                models.StoreItemMaster.objects.bulk_create(storeItem_list)
                csvfile.close()
                os.remove(MEDIA_ROOT + file_name)
            messages.success(request, 'Store Item Created Successfully.')
            return redirect('storeItemList')
    return render(request, 'storeItem/import.html', context)


@login_required
def downloadstoreItemExcel(request):
    file_path = (MEDIA_ROOT + "excels/downloadable/" + "store items.csv")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + \
                os.path.basename(file_path)
            return response


@login_required
def purchaseOrderList(request):
    page = request.GET.get('page', 1)
    purchaseOrders = models.PurchaseOrderHeader.objects.filter(deleted=0)
    # paginator = Paginator(purchaseOrders, env("PER_PAGE_DATA"))
    # purchaseOrders = paginator.page(page)
    context = {'purchaseOrders': purchaseOrders}
    return render(request, 'purchaseOrder/list.html', context)


@login_required
def purchaseOrderAdd(request):
    context = {}
    vendors = models.VendorMaster.objects.filter(deleted=0)
    items = models.ItemMaster.objects.filter(deleted=0)
    context.update({'vendors': vendors, 'items': items})
    if request.method == "POST":
        purchase_order_count = models.PurchaseOrderHeader.objects.filter(
            deleted=0).count()
        purchase_order_no = "PO-" + str(purchase_order_count + 1).zfill(8)
        purchaseOrder = models.PurchaseOrderHeader()
        # purchaseOrder.ammend_no = request.POST['ammend_no']
        purchaseOrder.purchase_order_no = purchase_order_no
        purchaseOrder.purchase_order_date = request.POST['purchase_order_date']
        purchaseOrder.notes = request.POST['notes']
        purchaseOrder.total_amount = request.POST['total_amount']
        purchaseOrder.vendor_id = request.POST['vendor_id']
        purchaseOrder.save()
        order_details = []
        for index, item in enumerate(request.POST.getlist('item_id[]')):
            order_details.append(models.PurchaseOrderDetails(quantity=request.POST.getlist('quantity[]')[index], unit_price=request.POST.getlist('unit_price[]')[
                                 index], amount=request.POST.getlist('amount[]')[index], purchase_order_header_id=purchaseOrder.id, item_id=request.POST.getlist('item_id[]')[index]))
        models.PurchaseOrderDetails.objects.bulk_create(order_details)
        messages.success(request, 'Purchase Order Created Successfully.')
        return redirect('purchaseOrderList')
    return render(request, 'purchaseOrder/add.html', context)


@login_required
def purchaseOrderEdit(request, id):
    context = {}
    purchaseOrder = models.PurchaseOrderHeader.objects.prefetch_related(
        'purchaseorderdetails_set').get(pk=id)
    items = models.ItemMaster.objects.filter(deleted=0)
    vendors = models.VendorMaster.objects.filter(deleted=0)
    context.update({'purchaseOrder': purchaseOrder,
                   'items': items, 'vendors': vendors})
    if request.method == "POST":
        purchaseOrder = models.PurchaseOrderHeader.objects.get(
            pk=request.POST['id'])
        # purchaseOrder.ammend_no = request.POST['ammend_no']
        purchaseOrder.purchase_order_date = request.POST['purchase_order_date']
        purchaseOrder.notes = request.POST['notes']
        purchaseOrder.total_amount = request.POST['total_amount']
        purchaseOrder.vendor_id = request.POST['vendor_id']
        purchaseOrder.save()
        models.PurchaseOrderDetails.objects.filter(
            purchase_order_header_id=purchaseOrder.id).delete()
        order_details = []
        for index, item in enumerate(request.POST.getlist('item_id[]')):
            order_details.append(models.PurchaseOrderDetails(quantity=request.POST.getlist('quantity[]')[index], unit_price=request.POST.getlist('unit_price[]')[
                                 index], amount=request.POST.getlist('amount[]')[index], purchase_order_header_id=purchaseOrder.id, item_id=request.POST.getlist('item_id[]')[index]))
        models.PurchaseOrderDetails.objects.bulk_create(order_details)
        messages.success(request, 'Purchase Order Updated Successfully.')
        return redirect('purchaseOrderList')
    return render(request, 'purchaseOrder/edit.html', context)


@login_required
def purchaseOrderDelete(request, id):
    purchaseOrder = models.PurchaseOrderHeader.objects.get(pk=id)
    purchaseOrder.deleted = 1
    purchaseOrder.save()
    models.PurchaseOrderDetails.objects.filter(
        purchase_order_header_id=purchaseOrder.id).update(deleted=1)
    return redirect('purchaseOrderList')


@login_required
def purchaseOrderDetailsList(request, header_id):
    page = request.GET.get('page', 1)
    purchaseHeader = models.PurchaseOrderHeader.objects.prefetch_related(
        'purchaseorderdetails_set').get(pk=header_id)
    context = {'purchaseHeader': purchaseHeader}
    return render(request, 'purchaseOrder/orderDetailsList.html', context)


@login_required
def salesOrderList(request):
    page = request.GET.get('page', 1)
    salesOrders = models.SalesOrderHeader.objects.filter(deleted=0)
    # paginator = Paginator(salesOrders, env("PER_PAGE_DATA"))
    # salesOrders = paginator.page(page)
    context = {'salesOrders': salesOrders}
    return render(request, 'salesOrder/list.html', context)


@login_required
def salesOrderAdd(request):
    context = {}
    salespersons = models.SalesPerson.objects.filter(deleted=0)
    customers = models.Customer.objects.filter(deleted=0)
    items = models.ItemMaster.objects.filter(deleted=0)
    context.update({'salespersons': salespersons,
                   'items': items, 'customers': customers})
    if request.method == "POST":
        sales_order_count = models.SalesOrderHeader.objects.filter(
            deleted=0).count()
        sales_order_no = "SO-" + str(sales_order_count + 1).zfill(8)
        salesOrder = models.SalesOrderHeader()
        # salesOrder.ammend_no = request.POST['ammend_no']
        salesOrder.sales_order_no = sales_order_no
        salesOrder.sales_order_date = request.POST['sales_order_date']
        salesOrder.notes = request.POST['notes']
        salesOrder.total_amount = request.POST['total_amount']
        salesOrder.commission = request.POST['commission']
        salesOrder.sales_person_id = request.POST['salesperson_id']
        salesOrder.customer_id = request.POST['customer_id']
        salesOrder.save()
        order_details = []
        for index, item in enumerate(request.POST.getlist('item_id[]')):
            order_details.append(models.SalesOrderDetails(quantity=request.POST.getlist('quantity[]')[index], unit_price=request.POST.getlist('unit_price[]')[
                                 index], amount=request.POST.getlist('amount[]')[index], sales_order_header_id=salesOrder.id, item_id=request.POST.getlist('item_id[]')[index]))
        models.SalesOrderDetails.objects.bulk_create(order_details)
        messages.success(request, 'Sales Order Created Successfully.')
        return redirect('salesOrderList')
    return render(request, 'salesOrder/add.html', context)


@login_required
def salesOrderEdit(request, id):
    context = {}
    salesOrder = models.SalesOrderHeader.objects.prefetch_related(
        'salesorderdetails_set').get(pk=id)
    items = models.ItemMaster.objects.filter(deleted=0)
    salespersons = models.SalesPerson.objects.filter(deleted=0)
    customers = models.Customer.objects.filter(deleted=0)
    context.update({'salesOrder': salesOrder, 'items': items,
                   'salespersons': salespersons, 'customers': customers})
    if request.method == "POST":
        salesOrder = models.SalesOrderHeader.objects.get(
            pk=request.POST['id'])
        # salesOrder.ammend_no = request.POST['ammend_no']
        salesOrder.sales_order_date = request.POST['sales_order_date']
        salesOrder.notes = request.POST['notes']
        salesOrder.total_amount = request.POST['total_amount']
        salesOrder.sales_person_id = request.POST['salesperson_id']
        salesOrder.commission = request.POST['commission']
        salesOrder.customer_id = request.POST['customer_id']
        salesOrder.save()
        models.SalesOrderDetails.objects.filter(
            sales_order_header_id=salesOrder.id).delete()
        order_details = []
        for index, item in enumerate(request.POST.getlist('item_id[]')):
            order_details.append(models.SalesOrderDetails(quantity=request.POST.getlist('quantity[]')[index], unit_price=request.POST.getlist('unit_price[]')[
                                 index], amount=request.POST.getlist('amount[]')[index], sales_order_header_id=salesOrder.id, item_id=request.POST.getlist('item_id[]')[index]))
        models.SalesOrderDetails.objects.bulk_create(order_details)
        messages.success(request, 'Sales Order Updated Successfully.')
        return redirect('salesOrderList')
    return render(request, 'salesOrder/edit.html', context)


@login_required
def salesOrderDelete(request, id):
    salesOrder = models.SalesOrderHeader.objects.get(pk=id)
    salesOrder.deleted = 1
    salesOrder.save()
    models.SalesOrderDetails.objects.filter(
        sales_order_header_id=salesOrder.id).update(deleted=1)
    return redirect('salesOrderList')


@login_required
def salesOrderDetailsList(request, header_id):
    page = request.GET.get('page', 1)
    salesHeader = models.SalesOrderHeader.objects.prefetch_related(
        'salesorderdetails_set').get(pk=header_id)
    context = {'salesHeader': salesHeader}
    return render(request, 'salesOrder/orderDetailsList.html', context)


@login_required
def storeTransactionList(request):
    page = request.GET.get('page', 1)
    storeTransactions = models.StoreTransactionHeader.objects.filter(deleted=0)
    # paginator = Paginator(storeTransactions, env("PER_PAGE_DATA"))
    # storeTransactions = paginator.page(page)
    context = {'storeTransactions': storeTransactions}
    return render(request, 'storeTransaction/list.html', context)


@login_required
def storeTransactionAdd(request):
    context = {}
    transactionTypes = models.TransactionType.objects.filter(
        deleted=0).exclude(id__in=[2, 3])
    context.update({'transactionTypes': transactionTypes})
    if request.method == "POST":
        if int(request.POST['transaction_type_id']) == 1:
            transaction_count = models.StoreTransactionHeader.objects.filter(
                deleted=0).count()
            transaction_number = "TR-" + str(transaction_count + 1).zfill(8)
            storeTransaction = models.StoreTransactionHeader()
            storeTransaction.transaction_number = transaction_number
            # storeTransaction.transaction_date = request.POST['transaction_date']
            storeTransaction.transaction_date = datetime.now()
            storeTransaction.purchase_order_header_id = request.POST['purchase_order_header_id']
            storeTransaction.store_id = request.POST['store_id']
            storeTransaction.transaction_type_id = request.POST['transaction_type_id']
            storeTransaction.vendor_id = request.POST['vendor_id']
            storeTransaction.total_amount = request.POST['total_amount']
            storeTransaction.save()
            order_details = []
            for index, item in enumerate(request.POST.getlist('purchase_details_id[]')):
                order_details.append(models.StoreTransactionDetails(type_id=request.POST['transaction_type_id'], quantity=request.POST.getlist('quantity[]')[index], unit_price=request.POST.getlist(
                    'unit_price[]')[index], amount=request.POST.getlist('amount[]')[index], item_id=request.POST.getlist('item_id[]')[index], store_transaction_header_id=storeTransaction.id))
                storeItem = models.StoreItemMaster.objects.filter(item_id=request.POST.getlist(
                    'item_id[]')[index], store_id=request.POST['store_id']).first()
                if storeItem is None:
                    storeItem = models.StoreItemMaster()
                    storeItem.opening_qty = Decimal(
                        request.POST.getlist('quantity[]')[index])
                    storeItem.on_hand_qty = Decimal(
                        request.POST.getlist('quantity[]')[index])
                    storeItem.closing_qty = Decimal(
                        request.POST.getlist('quantity[]')[index])
                    storeItem.item_id = request.POST.getlist('item_id[]')[
                        index]
                    storeItem.store_id = request.POST['store_id']
                    storeItem.save()
                else:
                    storeItem.on_hand_qty += Decimal(
                        request.POST.getlist('quantity[]')[index])
                    storeItem.closing_qty += Decimal(
                        request.POST.getlist('quantity[]')[index])
                    storeItem.save()
            models.StoreTransactionDetails.objects.bulk_create(order_details)
            if request.POST['purchase_order_header_id'] != "":
                for index, item in enumerate(request.POST.getlist('purchase_details_id[]')):
                    purchaseOrderItem = models.PurchaseOrderDetails.objects.get(
                        pk=request.POST.getlist('purchase_details_id[]')[index])
                    purchaseOrderItem.delivered_quantity += Decimal(
                        request.POST.getlist('quantity[]')[index])
                    purchaseOrderItem.save()
                purchaseHeader = models.PurchaseOrderHeader.objects.prefetch_related(
                    'purchaseorderdetails_set').get(pk=request.POST['purchase_order_header_id'])
                flag = True
                for purchaseOrderDetail in purchaseHeader.purchaseorderdetails_set.all():
                    if Decimal(purchaseOrderDetail.quantity) > Decimal(purchaseOrderDetail.delivered_quantity):
                        flag = False
                        break
                if flag == True:
                    purchaseHeader.status = 3
                else:
                    purchaseHeader.status = 2
                purchaseHeader.save()
        elif int(request.POST['transaction_type_id']) == 2:
            pass
        elif int(request.POST['transaction_type_id']) == 3:
            pass
        elif int(request.POST['transaction_type_id']) == 4:
            transfer_count = models.OnTransitHeader.objects.filter(
                deleted=0).count()
            transfer_number = "TF-" + str(transfer_count + 1).zfill(8)
            onTransitHeader = models.OnTransitHeader()
            onTransitHeader.transfer_number = transfer_number
            # onTransitHeader.transfer_date = request.POST['transaction_date']
            onTransitHeader.transfer_date = datetime.now()
            onTransitHeader.store_from_id = request.POST['store_from']
            onTransitHeader.store_to_id = request.POST['store_to']
            onTransitHeader.save()
            transit_details = []
            for index, item in enumerate(request.POST.getlist('item_id[]')):
                transit_details.append(models.OnTransitDetails(item_id=request.POST.getlist('item_id[]')[
                                       index], quantity=request.POST.getlist('quantity[]')[index], on_transit_header_id=onTransitHeader.id))
                storeFromItem = models.StoreItemMaster.objects.filter(item_id=request.POST.getlist(
                    'item_id[]')[index], store_id=request.POST['store_from']).first()
                storeFromItem.on_hand_qty -= Decimal(
                    request.POST.getlist('quantity[]')[index])
                storeFromItem.closing_qty -= Decimal(
                    request.POST.getlist('quantity[]')[index])
                storeFromItem.save()
            models.OnTransitDetails.objects.bulk_create(transit_details)
        elif int(request.POST['transaction_type_id']) == 5:
            transaction_count = models.StoreTransactionHeader.objects.filter(
                deleted=0).count()
            transaction_number = "TR-" + str(transaction_count + 1).zfill(8)
            storeTransaction = models.StoreTransactionHeader()
            storeTransaction.transaction_number = transaction_number
            # storeTransaction.transaction_date = request.POST['transaction_date']
            storeTransaction.transaction_date = datetime.now()
            storeTransaction.on_transit_header_id = request.POST['transfer_number']
            storeTransaction.store_id = request.POST['store_to']
            storeTransaction.transaction_type_id = request.POST['transaction_type_id']
            storeTransaction.total_amount = 0
            storeTransaction.save()
            order_details = []
            for index, item in enumerate(request.POST.getlist('on_transit_details_id[]')):
                order_details.append(models.StoreTransactionDetails(type_id=request.POST['transaction_type_id'], quantity=request.POST.getlist(
                    'quantity[]')[index], item_id=request.POST.getlist('item_id[]')[index], store_transaction_header_id=storeTransaction.id))
                transitDetails = models.OnTransitDetails.objects.get(pk=item)
                transitDetails.delivered_quantity += Decimal(
                    request.POST.getlist('quantity[]')[index])
                transitDetails.delivery_date = datetime.now()
                transitDetails.save()
                storeToItem = models.StoreItemMaster.objects.filter(item_id=request.POST.getlist(
                    'item_id[]')[index], store_id=request.POST['store_to']).first()
                if storeToItem is None:
                    storeToItem = models.StoreItemMaster()
                    storeToItem.opening_qty = Decimal(
                        request.POST.getlist('quantity[]')[index])
                    storeToItem.on_hand_qty = Decimal(
                        request.POST.getlist('quantity[]')[index])
                    storeToItem.closing_qty = Decimal(
                        request.POST.getlist('quantity[]')[index])
                    storeToItem.item_id = request.POST.getlist('item_id[]')[
                        index]
                    storeToItem.store_id = request.POST['store_to']
                    storeToItem.save()
                else:
                    storeToItem.on_hand_qty += Decimal(
                        request.POST.getlist('quantity[]')[index])
                    storeToItem.closing_qty += Decimal(
                        request.POST.getlist('quantity[]')[index])
                    storeToItem.save()
            models.StoreTransactionDetails.objects.bulk_create(order_details)
            onTransitHeader = models.OnTransitHeader.objects.prefetch_related(
                'ontransitdetails_set').get(pk=request.POST['transfer_number'])
            flag = True
            for onTransitDetail in onTransitHeader.ontransitdetails_set.all():
                if Decimal(onTransitDetail.quantity) > Decimal(onTransitDetail.delivered_quantity):
                    flag = False
                    break
            if flag == True:
                onTransitHeader.status = 3
            else:
                onTransitHeader.status = 2
            onTransitHeader.save()
        elif int(request.POST['transaction_type_id']) == 6:
            physical_stock_check_count = models.PhysicalStockHeader.objects.filter(
                deleted=0).count()
            physical_stock_check_number = "PS-" + \
                str(physical_stock_check_count + 1).zfill(8)
            physicalStockHeader = models.PhysicalStockHeader()
            physicalStockHeader.physical_stock_check_number = physical_stock_check_number
            # physicalStockHeader.physical_stock_check_date = request.POST['transaction_date']
            physicalStockHeader.physical_stock_check_date = datetime.now()
            physicalStockHeader.store_id = request.POST['store']
            physicalStockHeader.save()
            physical_stock_details = []
            for index, item in enumerate(request.POST.getlist('item_id[]')):
                storeItem = models.StoreItemMaster.objects.filter(item_id=request.POST.getlist(
                    'item_id[]')[index], store_id=request.POST['store']).first()
                physical_stock_details.append(models.PhysicalStockDetails(item_id=request.POST.getlist('item_id[]')[
                                              index], quantity=storeItem.opening_qty, original_quantity=request.POST.getlist('quantity[]')[index], physical_stock_header_id=physicalStockHeader.id))
            models.PhysicalStockDetails.objects.bulk_create(
                physical_stock_details)

            transaction_count = models.StoreTransactionHeader.objects.filter(
                deleted=0).count()
            transaction_number = "TR-" + str(transaction_count + 1).zfill(8)
            storeTransaction = models.StoreTransactionHeader()
            storeTransaction.transaction_number = transaction_number
            # storeTransaction.transaction_date = request.POST['transaction_date']
            storeTransaction.transaction_date = datetime.now()
            storeTransaction.physical_stock_header_id = physicalStockHeader.id
            storeTransaction.store_id = request.POST['store']
            storeTransaction.transaction_type_id = request.POST['transaction_type_id']
            storeTransaction.total_amount = 0
            storeTransaction.save()
            order_details = []
            for index, item in enumerate(request.POST.getlist('item_id[]')):
                order_details.append(models.StoreTransactionDetails(type_id=request.POST['transaction_type_id'], quantity=request.POST.getlist(
                    'quantity[]')[index], item_id=request.POST.getlist('item_id[]')[index], store_transaction_header_id=storeTransaction.id))
            models.StoreTransactionDetails.objects.bulk_create(order_details)
            physicalStockHeader = models.PhysicalStockHeader.objects.prefetch_related(
                'physicalstockdetails_set').get(pk=physicalStockHeader.id)
            flag = True
            for physicalDetail in physicalStockHeader.physicalstockdetails_set.all():
                if Decimal(physicalDetail.quantity) == Decimal(physicalDetail.original_quantity):
                    status = 1
                elif Decimal(physicalDetail.quantity) > Decimal(physicalDetail.original_quantity):
                    status = 2
                else:
                    status = 3
            physicalStockHeader.status = status
            physicalStockHeader.save()
        elif int(request.POST['transaction_type_id']) == 7:
            pass
        elif int(request.POST['transaction_type_id']) == 8:
            pass
        else:
            pass
        messages.success(request, 'Store Transaction Created Successfully.')
        return redirect('storeTransactionList')
    return render(request, 'storeTransaction/add.html', context)


@login_required
def storeTransactionEdit(request, id):
    context = {}
    storeTransaction = models.StoreTransactionHeader.objects.prefetch_related(
        'storetransactiondetails_set').get(pk=id)
    vendors = models.VendorMaster.objects.filter(deleted=0)
    vendorPurchaseOrders = models.PurchaseOrderHeader.objects.filter(
        vendor_id=storeTransaction.vendor_id, deleted=0)
    stores = models.StoreMaster.objects.filter(deleted=0)
    transactionTypes = models.TransactionType.objects.filter(
        deleted=0).exclude(id__in=[2, 3])
    items = models.ItemMaster.objects.filter(deleted=0)
    context.update({'storeTransaction': storeTransaction, 'vendors': vendors, 'stores': stores,
                   'items': items, 'transactionTypes': transactionTypes, 'vendorPurchaseOrders': vendorPurchaseOrders})
    if request.method == "POST":
        storeTransaction = models.StoreTransactionHeader.objects.get(
            pk=request.POST['id'])
        storeTransaction.transaction_date = request.POST['transaction_date']
        storeTransaction.purchase_order_header_id = request.POST['purchase_order_header_id']
        storeTransaction.store_id = request.POST['store_id']
        storeTransaction.transaction_type_id = request.POST['transaction_type_id']
        storeTransaction.vendor_id = request.POST['vendor_id']
        storeTransaction.total_amount = request.POST['total_amount']
        storeTransaction.save()
        models.StoreTransactionDetails.objects.filter(
            store_transaction_header_id=storeTransaction.id).delete()
        order_details = []
        for index, item in enumerate(request.POST.getlist('item_id[]')):
            order_details.append(models.StoreTransactionDetails(type_id=request.POST['transaction_type_id'], quantity=request.POST.getlist('quantity[]')[index], unit_price=request.POST.getlist(
                'unit_price[]')[index], amount=request.POST.getlist('amount[]')[index], item_id=request.POST.getlist('item_id[]')[index], store_transaction_header_id=storeTransaction.id))
            storeItem = models.StoreItemMaster.objects.filter(item_id=request.POST.getlist(
                'item_id[]')[index], store_id=request.POST['store_id']).first()
            if storeItem is None:
                storeItem = models.StoreItemMaster()
                storeItem.opening_qty = Decimal(
                    request.POST.getlist('quantity[]')[index])
                storeItem.on_hand_qty = Decimal(
                    request.POST.getlist('quantity[]')[index])
                storeItem.closing_qty = Decimal(
                    request.POST.getlist('quantity[]')[index])
                storeItem.item_id = request.POST.getlist('item_id[]')[index]
                storeItem.store_id = request.POST['store_id']
                storeItem.save()
            else:
                if int(storeTransaction.transaction_type_id) == 1:
                    storeItem.on_hand_qty += storeItem.closing_qty + \
                        Decimal(request.POST.getlist('quantity[]')[index])
                    storeItem.save()
        models.StoreTransactionDetails.objects.bulk_create(order_details)
        if request.POST['purchase_order_header_id'] != "":
            for index, item in enumerate(request.POST.getlist('purchase_details_id[]')):
                purchaseOrderItem = models.PurchaseOrderDetails.objects.get(
                    pk=request.POST.getlist('purchase_details_id[]')[index])
                purchaseOrderItem.delivered_quantity += Decimal(
                    request.POST.getlist('quantity[]')[index])
                purchaseOrderItem.save()
            purchaseOrderHeader = models.PurchaseOrderHeader.objects.get(
                pk=request.POST['purchase_order_header_id'])
            purchaseOrderHeader.status = 2
            purchaseOrderHeader.save()
        messages.success(request, 'Store Transaction Updated Successfully.')
        return redirect('storeTransactionList')
    return render(request, 'storeTransaction/edit.html', context)


@login_required
def storeTransactionDelete(request, id):
    storeTransaction = models.StoreTransactionHeader.objects.get(pk=id)
    storeTransaction.deleted = 1
    storeTransaction.save()
    models.StoreTransactionDetails.objects.filter(
        store_transaction_header_id=storeTransaction.id).update(deleted=1)
    return redirect('storeTransactionList')


@login_required
def storeTransactionDetailsList(request, header_id):
    page = request.GET.get('page', 1)
    storeTransactionHeader = models.StoreTransactionHeader.objects.prefetch_related(
        'storetransactiondetails_set').get(pk=header_id)
    for storeTransactionHeaderDetail in storeTransactionHeader.storetransactiondetails_set.all():
        if (storeTransactionHeaderDetail.type_id == 6):
            physicalStockDetails = models.PhysicalStockDetails.objects.filter(
                item_id=storeTransactionHeaderDetail.item_id, physical_stock_header_id=storeTransactionHeaderDetail.store_transaction_header.physical_stock_header_id).first()
            storeTransactionHeaderDetail.actual_quantity = physicalStockDetails.quantity
    context = {'storeTransactionHeader': storeTransactionHeader}
    return render(request, 'storeTransaction/orderDetailsList.html', context)


@login_required
def getVendorPurchaseOrders(request):
    if request.method == "POST":
        vendor_id = request.POST['vendor_id']
        purchase_orders = list(models.PurchaseOrderHeader.objects.filter(
            vendor_id=vendor_id, deleted=0).exclude(status__in=[3]).values('id', 'purchase_order_no'))
        return JsonResponse({
            'code': 200,
            'status': 'SUCCESS',
            'data': purchase_orders,
        })
    else:
        return JsonResponse({
            'code': 503,
            'status': 'ERROR',
            'message': 'There should be post method.'
        })


@login_required
def getCustomerSalesOrders(request):
    if request.method == "POST":
        customer_id = request.POST['customer_id']
        sales_orders = list(models.SalesOrderHeader.objects.filter(
            customer_id=customer_id, deleted=0).exclude(status__in=[3]).values('id', 'sales_order_no'))
        return JsonResponse({
            'code': 200,
            'status': 'SUCCESS',
            'data': sales_orders,
        })
    else:
        return JsonResponse({
            'code': 509,
            'status': 'ERROR',
            'message': 'There should be post method.'
        })


@login_required
def getPurchaseOrderDetails(request):
    if request.method == "POST":
        purchase_order_header_id = request.POST['purchase_order_header_id']
        purchase_order_details = list(models.PurchaseOrderDetails.objects.filter(
            purchase_order_header_id=purchase_order_header_id).values('id', 'ammend_no', 'quantity', 'delivered_quantity', 'unit_price', 'amount', 'item_id'))
        items = list(models.ItemMaster.objects.filter(
            deleted=0).values('id', 'description'))
        purchase_order_details = list(models.PurchaseOrderDetails.objects.filter(
            purchase_order_header_id=purchase_order_header_id).values('id', 'ammend_no', 'quantity', 'delivered_quantity', 'unit_price', 'amount', 'item_id'))
        return JsonResponse({
            'code': 200,
            'status': 'SUCCESS',
            'data': purchase_order_details,
            'items': items,
        })
    else:
        return JsonResponse({
            'code': 504,
            'status': 'ERROR',
            'message': 'There should be post method.'
        })


@login_required
def getSalesOrderDetails(request):
    if request.method == "POST":
        store_id = request.POST['store_id']
        sales_order_header_id = request.POST['sales_order_header_id']
        sales_order_details = list(models.SalesOrderDetails.objects.filter(
            sales_order_header_id=sales_order_header_id).values('id', 'quantity', 'delivered_quantity', 'unit_price', 'amount', 'item_id', 'item__gst_percentage'))
        items = list(models.ItemMaster.objects.filter(
            deleted=0).values('id', 'description'))
        sales_order_details = list(models.SalesOrderDetails.objects.filter(
            sales_order_header_id=sales_order_header_id).values('id', 'quantity', 'delivered_quantity', 'unit_price', 'amount', 'item_id', 'item__gst_percentage'))
        for sales_order in sales_order_details:
            store_item = models.StoreItemMaster.objects.filter(
                store_id=store_id, item_id=sales_order['item_id']).first()
            sales_order['store_quantity'] = 0 if store_item is None else store_item.on_hand_qty
        return JsonResponse({
            'code': 200,
            'status': 'SUCCESS',
            'data': sales_order_details,
            'items': items,
        })
    else:
        return JsonResponse({
            'code': 510,
            'status': 'ERROR',
            'message': 'There should be post method.'
        })


@login_required
def standardTermList(request):
    page = request.GET.get('page', 1)
    standardTerms = models.StandardTermMaster.objects.filter(deleted=0)
    # paginator = Paginator(standardTerms, env("PER_PAGE_DATA"))
    # standardTerms = paginator.page(page)
    context = {'standardTerms': standardTerms}
    return render(request, 'standardTerm/list.html', context)


@login_required
def standardTermAdd(request):
    context = {}
    if request.method == "POST":
        standardTerm = models.StandardTermMaster()
        standardTerm.description = request.POST['description']
        standardTerm.save()
        messages.success(request, 'Standard Term Created Successfully.')
        return redirect('standardTermList')
    return render(request, 'standardTerm/add.html', context)


@login_required
def standardTermEdit(request, id):
    context = {}
    standardTerm = models.StandardTermMaster.objects.get(pk=id)
    context.update({'standardTerm': standardTerm})
    if request.method == "POST":
        standardTerm = models.StandardTermMaster.objects.get(
            pk=request.POST['id'])
        standardTerm.description = request.POST['description']
        standardTerm.save()
        messages.success(request, 'Standard Term Updated Successfully.')
        return redirect('standardTermList')
    return render(request, 'standardTerm/edit.html', context)


@login_required
def standardTermDelete(request, id):
    standardTerm = models.StandardTermMaster.objects.get(pk=id)
    standardTerm.deleted = 1
    standardTerm.save()
    return redirect('standardTermList')


@login_required
def onTransitOrderList(request):
    page = request.GET.get('page', 1)
    onTransitOrders = models.OnTransitHeader.objects.filter(
        deleted=0).exclude(status=3)
    # paginator = Paginator(onTransitOrders, env("PER_PAGE_DATA"))
    # onTransitOrders = paginator.page(page)
    context = {'onTransitOrders': onTransitOrders}
    return render(request, 'onTransitOrder/list.html', context)


@login_required
def onTransitOrderDetailsList(request, header_id):
    page = request.GET.get('page', 1)
    onTransitOrder = models.OnTransitHeader.objects.prefetch_related(
        'ontransitdetails_set').get(pk=header_id)
    context = {'onTransitOrder': onTransitOrder}
    return render(request, 'onTransitOrder/orderDetailsList.html', context)


@login_required
def invoiceList(request):
    page = request.GET.get('page', 1)
    invoices = models.InvoiceHeader.objects.filter(deleted=0)
    # paginator = Paginator(invoices, env("PER_PAGE_DATA"))
    # invoices = paginator.page(page)
    context = {'invoices': invoices}
    return render(request, 'invoice/list.html', context)


@login_required
def invoiceAdd(request, invoice_type=None):
    context = {}
    if invoice_type == 'gst':
        customers = models.Customer.objects.filter(deleted=0).exclude(
            gst_no__isnull=True).exclude(gst_no__exact='')
    else:
        customers = models.Customer.objects.filter(deleted=0)
    stores = models.StoreMaster.objects.filter(deleted=0)
    context.update({'customers': customers, 'stores': stores,
                   'invoice_type': invoice_type})
    if request.method == "POST":
        total_item_price = 0
        total_gst_price = 0
        for index, item in enumerate(request.POST.getlist('item_total_price[]')):
            total_item_price += Decimal(item)
            if 'item_gst_price[]' in request.POST.keys():
                total_gst_price += Decimal(
                    request.POST.getlist('item_gst_price[]')[index])
            elif 'item_cgst_price[]' in request.POST.keys():
                total_gst_price += Decimal(request.POST.getlist('item_cgst_price[]')[
                                           index]) + Decimal(request.POST.getlist('item_sgst_price[]')[index])
            else:
                total_gst_price += 0
        invoice_count = models.InvoiceHeader.objects.filter(deleted=0).count()
        invoice_number = "IN-" + str(invoice_count + 1).zfill(8)
        invoiceHeader = models.InvoiceHeader()
        invoiceHeader.invoice_number = invoice_number
        invoiceHeader.vehicle_number = request.POST['vehicle_number'].upper()
        invoiceHeader.invoice_date = datetime.now()
        invoiceHeader.invoice_total = total_item_price
        invoiceHeader.invoice_gst_total = total_gst_price
        invoiceHeader.carrying_cost = request.POST['carrying_cost']
        invoiceHeader.customer_id = request.POST['customer_id']
        invoiceHeader.store_id = request.POST['store']
        invoiceHeader.due_amount = request.POST['due_amount']
        invoiceHeader.total_amount = request.POST['total_amount']
        invoiceHeader.save()
        order_details = []
        for index, item in enumerate(request.POST.getlist('item_id[]')):
            if 'item_gst_price[]' in request.POST.keys():
                order_details.append(models.InvoiceDetails(quantity=request.POST.getlist('quantity[]')[index], item_id=item, invoice_item_value=request.POST.getlist(
                    'item_total_price[]')[index], invoice_item_gst_value=request.POST.getlist('item_gst_price[]')[index], invoice_header_id=invoiceHeader.id))
            elif 'item_cgst_price[]' in request.POST.keys():
                order_details.append(models.InvoiceDetails(quantity=request.POST.getlist('quantity[]')[index], item_id=item, invoice_item_value=request.POST.getlist('item_total_price[]')[
                                     index], invoice_item_gst_value=(Decimal(request.POST.getlist('item_cgst_price[]')[index]) + Decimal(request.POST.getlist('item_sgst_price[]')[index])), invoice_header_id=invoiceHeader.id))
            else:
                order_details.append(models.InvoiceDetails(quantity=request.POST.getlist('quantity[]')[index], item_id=item, invoice_item_value=request.POST.getlist(
                    'item_total_price[]')[index], invoice_item_gst_value=0, invoice_header_id=invoiceHeader.id))
        models.InvoiceDetails.objects.bulk_create(order_details)
        terms_list = []
        for index, item in enumerate(request.POST.getlist('terms[]')):
            terms_list.append(models.InvoiceTerms(term_id=request.POST.getlist(
                'terms[]')[index], invoice_header_id=invoiceHeader.id))
        models.InvoiceTerms.objects.bulk_create(terms_list)
        transaction_count = models.StoreTransactionHeader.objects.filter(
            deleted=0).count()
        transaction_number = "TR-" + str(transaction_count + 1).zfill(8)
        storeTransaction = models.StoreTransactionHeader()
        storeTransaction.transaction_number = transaction_number
        # storeTransaction.transaction_date = request.POST['transaction_date']
        storeTransaction.transaction_date = datetime.now()
        storeTransaction.invoice_header_id = invoiceHeader.id
        storeTransaction.store_id = request.POST['store']
        storeTransaction.transaction_type_id = 7
        storeTransaction.total_amount = total_item_price
        storeTransaction.total_gst_price = total_gst_price
        storeTransaction.save()
        transaction_order_details = []
        for index, item in enumerate(request.POST.getlist('item_id[]')):
            if 'item_gst_price[]' in request.POST.keys():
                transaction_order_details.append(models.StoreTransactionDetails(type_id=7, quantity=request.POST.getlist('quantity[]')[index], item_id=request.POST.getlist('item_id[]')[index], unit_price=request.POST.getlist('unit_price[]')[
                                                 index], amount=request.POST.getlist('item_total_price[]')[index], gst_price=request.POST.getlist('item_gst_price[]')[index], gst_percentage=request.POST.getlist('gst_percentage[]')[index], store_transaction_header_id=storeTransaction.id))
            elif 'item_cgst_price[]' in request.POST.keys():
                transaction_order_details.append(models.StoreTransactionDetails(type_id=7, quantity=request.POST.getlist('quantity[]')[index], item_id=request.POST.getlist('item_id[]')[index], unit_price=request.POST.getlist('unit_price[]')[index], amount=request.POST.getlist('item_total_price[]')[index], gst_price=(
                    Decimal(request.POST.getlist('item_cgst_price[]')[index]) + Decimal(request.POST.getlist('item_sgst_price[]')[index])), gst_percentage=(Decimal(request.POST.getlist('cgst_percentage[]')[index]) + Decimal(request.POST.getlist('sgst_percentage[]')[index])), store_transaction_header_id=storeTransaction.id))
            else:
                transaction_order_details.append(models.StoreTransactionDetails(type_id=7, quantity=request.POST.getlist('quantity[]')[index], item_id=request.POST.getlist('item_id[]')[
                                                 index], unit_price=request.POST.getlist('unit_price[]')[index], amount=request.POST.getlist('item_total_price[]')[index], gst_price=0, gst_percentage=0, store_transaction_header_id=storeTransaction.id))
            storeItem = models.StoreItemMaster.objects.filter(item_id=request.POST.getlist(
                'item_id[]')[index], store_id=request.POST['store']).first()
            if storeItem is None:
                storeItem = models.StoreItemMaster()
                storeItem.opening_qty = Decimal(
                    request.POST.getlist('quantity[]')[index])
                storeItem.on_hand_qty = Decimal(
                    request.POST.getlist('quantity[]')[index])
                storeItem.closing_qty = Decimal(
                    request.POST.getlist('quantity[]')[index])
                storeItem.item_id = request.POST.getlist('item_id[]')[index]
                storeItem.store_id = request.POST['store']
                storeItem.save()
            else:
                storeItem.on_hand_qty -= Decimal(
                    request.POST.getlist('quantity[]')[index])
                storeItem.closing_qty -= Decimal(
                    request.POST.getlist('quantity[]')[index])
                storeItem.save()
        models.StoreTransactionDetails.objects.bulk_create(
            transaction_order_details)
        if 'sales_order_header_id' in request.POST.keys() and request.POST['sales_order_header_id'] != "":
            for index, item in enumerate(request.POST.getlist('sales_details_id[]')):
                salesOrderItem = models.SalesOrderDetails.objects.get(
                    pk=request.POST.getlist('sales_details_id[]')[index])
                salesOrderItem.delivered_quantity += Decimal(
                    request.POST.getlist('quantity[]')[index])
                salesOrderItem.save()
            salesHeader = models.SalesOrderHeader.objects.prefetch_related(
                'salesorderdetails_set').get(pk=request.POST['sales_order_header_id'])
            flag = True
            for salesOrderDetail in salesHeader.salesorderdetails_set.all():
                if Decimal(salesOrderDetail.quantity) > Decimal(salesOrderDetail.delivered_quantity):
                    flag = False
                    break
            if flag == True:
                salesHeader.status = 3
            else:
                salesHeader.status = 2
            salesHeader.save()
        messages.success(request, 'Invoice Created Successfully.')
        return redirect('invoiceList')
    return render(request, 'invoice/add.html', context)


@login_required
def invoiceDetailsList(request, header_id):
    page = request.GET.get('page', 1)
    invoiceOrder = models.InvoiceHeader.objects.prefetch_related(
        'invoicedetails_set').get(pk=header_id)
    context = {'invoiceOrder': invoiceOrder}
    return render(request, 'invoice/orderDetailsList.html', context)


@login_required
def printInvoice(request, header_id):
    client_details = {
        'client_name': env("CLIENT_NAME"),
        'client_address': env("CLIENT_ADDRESS"),
        'client_address_2': env("CLIENT_ADDRESS_2"),
        'client_pin': env("CLIENT_PIN"),
        'client_mobile': env("CLIENT_MOBILE"),
        'client_email': env("CLIENT_EMAIL"),
    }
    page = request.GET.get('page', 1)
    invoiceOrder = models.InvoiceHeader.objects.prefetch_related(
        'invoicedetails_set', 'invoiceterms_set').get(pk=header_id)
    invoicePayments = models.InvoicePayments.objects.filter(
        customer_id=invoiceOrder.customer_id).exclude(status=3)
    due_payment = 0
    for invoicePayment in invoicePayments:
        due_payment += (invoicePayment.total_amount -
                        invoicePayment.paid_amount)
    context = {'invoiceOrder': invoiceOrder,
               'due_payment': due_payment, 'client_details': client_details}
    return render(request, 'invoice/printInvoice.html', context)


@login_required
def pendingInvoiceList(request):
    page = request.GET.get('page', 1)
    invoices = models.InvoiceHeader.objects.filter(deleted=0).exclude(status=3)
    # paginator = Paginator(invoices, env("PER_PAGE_DATA"))
    # invoices = paginator.page(page)
    context = {'invoices': invoices}
    return render(request, 'pendingInvoice/list.html', context)


@login_required
def pendingInvoicePayment(request, invoice_id):
    invoiceHeader = models.InvoiceHeader.objects.prefetch_related(
        'invoicedetails_set', 'invoiceterms_set').get(pk=invoice_id)
    paymentMethods = models.PaymentMethods.objects.filter(deleted=0)
    invoicePayments = models.InvoicePayments.objects.filter(
        customer_id=invoiceHeader.customer_id).exclude(status=3)
    due_payment = 0
    for invoicePayment in invoicePayments:
        due_payment += (invoicePayment.total_amount -
                        invoicePayment.paid_amount)
    context = {
        'invoiceHeader': invoiceHeader,
        'paymentMethods': paymentMethods,
        'due_payment': due_payment,
    }
    if request.method == "POST":
        invoicePayment = models.InvoicePayments()
        invoicePayment.invoice_header_id = request.POST['invoice_header_id']
        invoicePayment.customer_id = request.POST['customer_id']
        invoicePayment.payment_method_id = request.POST['payment_method']
        invoicePayment.reference_number = request.POST['reference_number']
        invoicePayment.invoice_amount = request.POST['invoice_amount']
        invoicePayment.gst_price = request.POST['gst_price']
        invoicePayment.carrying_cost = request.POST['carrying_cost']
        invoicePayment.due_amount = request.POST['due_amount']
        invoicePayment.total_amount = request.POST['total_amount']
        invoicePayment.paid_amount = request.POST['paid_amount']
        invoicePayment.save()
        invoiceHeader = models.InvoiceHeader.objects.get(
            pk=request.POST['invoice_header_id'])
        invoiceHeader.paid_amount = request.POST['paid_amount']
        invoiceHeader.save()
        messages.success(request, 'Payment Receipt Created Successfully.')
        return redirect('pendingInvoiceList')
    return render(request, 'pendingInvoice/payment.html', context)
