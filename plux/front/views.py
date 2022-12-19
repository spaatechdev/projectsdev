from django.shortcuts import render, redirect
from django.http import HttpResponse
from .decorators import login_required
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from front.backends import AuthBackend
from . import models
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
import environ
import os
from plux.settings import MEDIA_ROOT
from django.core.files.storage import FileSystemStorage
import csv
env = environ.Env()
environ.Env.read_env()

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the Front index.")


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
    paginator = Paginator(customers, env("PER_PAGE_DATA"))
    customers = paginator.page(page)
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
                        name__contains=row['Country']).first()
                    state_obj = models.States.objects.filter(
                        name__contains=row['State']).first()
                    city_obj = models.Cities.objects.filter(
                        name__contains=row['City']).first()
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
def userList(request):
    page = request.GET.get('page', 1)
    users = models.User.objects.all()
    paginator = Paginator(users, env("PER_PAGE_DATA"))
    users = paginator.page(page)
    context = {'users': users}
    return render(request, 'user/list.html', context)


@login_required
def vendorList(request):
    page = request.GET.get('page', 1)
    vendors = models.VendorMaster.objects.filter(deleted=0)
    paginator = Paginator(vendors, env("PER_PAGE_DATA"))
    vendors = paginator.page(page)
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
                        name__contains=row['Country']).first()
                    state_obj = models.States.objects.filter(
                        name__contains=row['State']).first()
                    city_obj = models.Cities.objects.filter(
                        name__contains=row['City']).first()
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
    paginator = Paginator(stores, env("PER_PAGE_DATA"))
    stores = paginator.page(page)
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
            'code': 501,
            'status': 'ERROR',
            'message': 'There should be post method.'
        })


@login_required
def uomList(request):
    page = request.GET.get('page', 1)
    uoms = models.UomMaster.objects.filter(deleted=0)
    paginator = Paginator(uoms, env("PER_PAGE_DATA"))
    uoms = paginator.page(page)
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
def itemCategoryList(request):
    page = request.GET.get('page', 1)
    itemCategories = models.ItemCtegory.objects.filter(deleted=0)
    paginator = Paginator(itemCategories, env("PER_PAGE_DATA"))
    itemCategories = paginator.page(page)
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
def plyDimensionList(request):
    page = request.GET.get('page', 1)
    plyDimensions = models.PlyDimensionMaster.objects.filter(deleted=0)
    paginator = Paginator(plyDimensions, env("PER_PAGE_DATA"))
    plyDimensions = paginator.page(page)
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
def itemList(request):
    page = request.GET.get('page', 1)
    items = models.ItemMaster.objects.filter(deleted=0)
    paginator = Paginator(items, env("PER_PAGE_DATA"))
    items = paginator.page(page)
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
        messages.success(request, 'Item Created Successfully.')
        return redirect('itemList')
    return render(request, 'item/add.html', context)


@login_required
def itemEdit(request, id):
    context = {}
    item = models.ItemMaster.objects.get(pk=id)
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
def storeItemList(request):
    page = request.GET.get('page', 1)
    storeItems = models.StoreItemMaster.objects.filter(deleted=0)
    paginator = Paginator(storeItems, env("PER_PAGE_DATA"))
    storeItems = paginator.page(page)
    context = {'storeItems': storeItems}
    return render(request, 'storeItem/list.html', context)


@login_required
def storeItemAdd(request):
    context = {}
    stores = models.StoreMaster.objects.filter(deleted=0)
    existing_items = models.StoreItemMaster.objects.filter(deleted=0).values('item_id')
    item_ids = []
    for ei in existing_items:
        item_ids.append(ei['item_id'])
    items = models.ItemMaster.objects.filter(deleted=0).exclude(id__in=item_ids)
    context.update({'items': items, 'stores': stores})
    if request.method == "POST":
        storeItem = models.StoreItemMaster()
        storeItem.opening_qty = request.POST['opening_qty']
        # storeItem.on_hand_qty = request.POST['on_hand_qty']
        storeItem.on_hand_qty = 0
        storeItem.closing_qty = request.POST['closing_qty']
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
        storeItem.on_hand_qty = 0
        storeItem.closing_qty = request.POST['closing_qty']
        storeItem.item_id = request.POST['item_id']
        storeItem.store_id = request.POST['store_id']
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
def purchaseOrderList(request):
    page = request.GET.get('page', 1)
    purchaseOrders = models.PurchaseOrderHeader.objects.filter(deleted=0)
    paginator = Paginator(purchaseOrders, env("PER_PAGE_DATA"))
    purchaseOrders = paginator.page(page)
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
    context.update({'purchaseOrder': purchaseOrder, 'items': items, 'vendors': vendors})
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
def storeTransactionList(request):
    page = request.GET.get('page', 1)
    storeTransactions = models.StoreTransactionHeader.objects.filter(deleted=0)
    paginator = Paginator(storeTransactions, env("PER_PAGE_DATA"))
    storeTransactions = paginator.page(page)
    context = {'storeTransactions': storeTransactions}
    return render(request, 'storeTransaction/list.html', context)


@login_required
def storeTransactionAdd(request):
    context = {}
    vendors = models.VendorMaster.objects.filter(deleted=0)
    stores = models.StoreMaster.objects.filter(deleted=0)
    transactionTypes = models.TransactionType.objects.filter(deleted=0)
    purchaseOrders = models.PurchaseOrderHeader.objects.filter(deleted=0)
    items = models.ItemMaster.objects.filter(deleted=0)
    context.update({'vendors': vendors, 'stores': stores, 'items': items, 'transactionTypes': transactionTypes, 'purchaseOrders': purchaseOrders})
    if request.method == "POST":
        print(request.POST)
        exit()
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
    return render(request, 'storeTransaction/add.html', context)


@login_required
def getPurchaseOrderDetails(request):
    if request.method == "POST":
        purchase_order_header_id = request.POST['purchase_order_header_id']
        purchase_order_details = list(models.PurchaseOrderDetails.objects.filter(purchase_order_header_id=purchase_order_header_id).values('id', 'ammend_no', 'quantity', 'unit_price', 'amount', 'item_id'))
        items = list(models.ItemMaster.objects.filter(deleted=0).values('id', 'description'))
        purchase_order_details = list(models.PurchaseOrderDetails.objects.filter(purchase_order_header_id=purchase_order_header_id).values('id', 'ammend_no', 'quantity', 'unit_price', 'amount', 'item_id'))
        return JsonResponse({
            'code': 200,
            'status': 'SUCCESS',
            'data': purchase_order_details,
            'items': items,
        })
    else:
        return JsonResponse({
            'code': 501,
            'status': 'ERROR',
            'message': 'There should be post method.'
        })


@login_required
def storeTransactionEdit(request, id):
    context = {}
    purchaseOrder = models.PurchaseOrderHeader.objects.prefetch_related(
        'purchaseorderdetails_set').get(pk=id)
    items = models.ItemMaster.objects.filter(deleted=0)
    vendors = models.VendorMaster.objects.filter(deleted=0)
    stores = models.StoreMaster.objects.filter(deleted=0)
    context.update({'purchaseOrder': purchaseOrder,
                   'items': items, 'vendors': vendors, 'stores': stores})
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
def storeTransactionDelete(request, id):
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
def standardTermList(request):
    page = request.GET.get('page', 1)
    standardTerms = models.StandardTermMaster.objects.filter(deleted=0)
    paginator = Paginator(standardTerms, env("PER_PAGE_DATA"))
    standardTerms = paginator.page(page)
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
