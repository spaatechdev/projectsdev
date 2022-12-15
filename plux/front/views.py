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
            return redirect('signin')
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
    customers = models.Customer.objects.filter(deleted=0)
    context = {'customers': customers}
    return render(request, 'customer/list.html', context)


@login_required
def customerAdd(request):
    context = {}
    countries = models.Countries.objects.all()
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
    countries = models.Countries.objects.all()
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
def userList(request):
    users = models.User.objects.all()
    context = {'users': users}
    return render(request, 'user/list.html', context)


@login_required
def vendorList(request):
    vendors = models.VendorMaster.objects.filter(deleted=0)
    context = {'vendors': vendors}
    return render(request, 'vendor/list.html', context)


@login_required
def vendorAdd(request):
    context = {}
    countries = models.Countries.objects.all()
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
    countries = models.Countries.objects.all()
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
def storeList(request):
    stores = models.StoreMaster.objects.filter(deleted=0)
    context = {'stores': stores}
    return render(request, 'store/list.html', context)


@login_required
def storeAdd(request):
    context = {}
    countries = models.Countries.objects.all()
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
    countries = models.Countries.objects.all()
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
    uoms = models.UomMaster.objects.filter(deleted=0)
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
    itemCategories = models.ItemCtegory.objects.filter(deleted=0)
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
    plyDimensions = models.PlyDimensionMaster.objects.filter(deleted=0)
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
    items = models.ItemMaster.objects.filter(deleted=0)
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
    storeItems = models.StoreItemMaster.objects.filter(deleted=0)
    context = {'storeItems': storeItems}
    return render(request, 'storeItem/list.html', context)


@login_required
def storeItemAdd(request):
    context = {}
    stores = models.StoreMaster.objects.filter(deleted=0)
    items = models.ItemMaster.objects.filter(deleted=0)
    context.update({'items': items, 'stores': stores})
    if request.method == "POST":
        storeItem = models.StoreItemMaster()
        storeItem.opening_qty = request.POST['opening_qty']
        storeItem.on_hand_qty = request.POST['on_hand_qty']
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
    items = models.ItemMaster.objects.filter(deleted=0)
    context.update({'storeItem': storeItem, 'items': items, 'stores': stores})
    if request.method == "POST":
        storeItem = models.StoreItemMaster.objects.get(pk=request.POST['id'])
        storeItem.opening_qty = request.POST['opening_qty']
        storeItem.on_hand_qty = request.POST['on_hand_qty']
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
    purchaseOrders = models.PurchaseOrderHeader.objects.filter(deleted=0)
    context = {'purchaseOrders': purchaseOrders}
    return render(request, 'purchaseOrder/list.html', context)


@login_required
def purchaseOrderAdd(request):
    context = {}
    vendors = models.VendorMaster.objects.filter(deleted=0)
    stores = models.StoreMaster.objects.filter(deleted=0)
    context.update({'vendors': vendors, 'stores': stores})
    if request.method == "POST":
        purchaseOrder = models.PurchaseOrderHeader()
        purchaseOrder.ammend_no = request.POST['ammend_no']
        purchaseOrder.purchase_order_date = request.POST['purchase_order_date']
        purchaseOrder.notes = request.POST['notes']
        purchaseOrder.total_amount = request.POST['total_amount']
        purchaseOrder.store_id = request.POST['store_id']
        purchaseOrder.vendor_id = request.POST['vendor_id']
        purchaseOrder.save()
        messages.success(request, 'Purchase Order Created Successfully.')
        return redirect('purchaseOrderList')
    return render(request, 'purchaseOrder/add.html', context)


@login_required
def purchaseOrderEdit(request, id):
    context = {}
    purchaseOrder = models.PurchaseOrderHeader.objects.get(pk=id)
    vendors = models.VendorMaster.objects.filter(deleted=0)
    stores = models.StoreMaster.objects.filter(deleted=0)
    context.update({'purchaseOrder': purchaseOrder,
                   'vendors': vendors, 'stores': stores})
    if request.method == "POST":
        purchaseOrder = models.PurchaseOrderHeader.objects.get(
            pk=request.POST['id'])
        purchaseOrder.ammend_no = request.POST['ammend_no']
        purchaseOrder.purchase_order_date = request.POST['purchase_order_date']
        purchaseOrder.notes = request.POST['notes']
        purchaseOrder.total_amount = request.POST['total_amount']
        purchaseOrder.store_id = request.POST['store_id']
        purchaseOrder.vendor_id = request.POST['vendor_id']
        purchaseOrder.save()
        messages.success(request, 'Purchase Order Updated Successfully.')
        return redirect('purchaseOrderList')
    return render(request, 'purchaseOrder/edit.html', context)


@login_required
def purchaseOrderDelete(request, id):
    purchaseOrder = models.PurchaseOrderHeader.objects.get(pk=id)
    purchaseOrder.deleted = 1
    purchaseOrder.save()
    return redirect('purchaseOrderList')
