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
    context = {}
    return render(request, 'vendor/list.html', context)


@login_required
def storeList(request):
    context = {}
    return render(request, 'store/list.html', context)


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
    context = {}
    return render(request, 'uom/list.html', context)


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
