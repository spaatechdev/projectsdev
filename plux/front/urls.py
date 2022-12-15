from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('myProfile', views.myProfile, name='myProfile'),
    path('userList', views.userList, name='userList'),

    path('customerList', views.customerList, name='customerList'),
    path('customerAdd', views.customerAdd, name='customerAdd'),
    path('customerEdit/<int:id>', views.customerEdit, name='customerEdit'),
    path('customerDelete/<int:id>', views.customerDelete, name='customerDelete'),
    
    path('uomList', views.uomList, name='uomList'),
    path('uomAdd', views.uomAdd, name='uomAdd'),
    path('uomEdit/<int:id>', views.uomEdit, name='uomEdit'),
    path('uomDelete/<int:id>', views.uomDelete, name='uomDelete'),
    
    path('storeList', views.storeList, name='storeList'),

    path('vendorList', views.vendorList, name='vendorList'),
    path('vendorAdd', views.vendorAdd, name='vendorAdd'),
    path('vendorEdit/<int:id>', views.vendorEdit, name='vendorEdit'),
    path('vendorDelete/<int:id>', views.vendorDelete, name='vendorDelete'),

    path('uomList', views.uomList, name='uomList'),

    path('storeList', views.storeList, name='storeList'),
    path('storeAdd', views.storeAdd, name='storeAdd'),
    path('storeEdit/<int:id>', views.storeEdit, name='storeEdit'),
    path('storeDelete/<int:id>', views.storeDelete, name='storeDelete'),
    
    path('itemCategoryList', views.itemCategoryList, name='itemCategoryList'),
    path('itemCategoryAdd', views.itemCategoryAdd, name='itemCategoryAdd'),
    path('itemCategoryEdit/<int:id>', views.itemCategoryEdit, name='itemCategoryEdit'),
    path('itemCategoryDelete/<int:id>', views.itemCategoryDelete, name='itemCategoryDelete'),
    
    path('plyDimensionList', views.plyDimensionList, name='plyDimensionList'),
    path('plyDimensionAdd', views.plyDimensionAdd, name='plyDimensionAdd'),
    path('plyDimensionEdit/<int:id>', views.plyDimensionEdit, name='plyDimensionEdit'),
    path('plyDimensionDelete/<int:id>', views.plyDimensionDelete, name='plyDimensionDelete'),

    path('itemList', views.itemList, name='itemList'),
    path('itemAdd', views.itemAdd, name='itemAdd'),
    path('itemEdit/<int:id>', views.itemEdit, name='itemEdit'),
    path('itemDelete/<int:id>', views.itemDelete, name='itemDelete'),

    path('storeItemList', views.storeItemList, name='storeItemList'),
    path('storeItemAdd', views.storeItemAdd, name='storeItemAdd'),
    path('storeItemEdit/<int:id>', views.storeItemEdit, name='storeItemEdit'),
    path('storeItemDelete/<int:id>', views.storeItemDelete, name='storeItemDelete'),

    path('standardTermList', views.standardTermList, name='standardTermList'),
    path('standardTermAdd', views.standardTermAdd, name='standardTermAdd'),
    path('standardTermEdit/<int:id>', views.standardTermEdit, name='standardTermEdit'),
    path('standardTermDelete/<int:id>', views.standardTermDelete, name='standardTermDelete'),
    
    path('getStatesByCountry', views.getStatesByCountry, name='getStatesByCountry'),
    path('getCitiesByState', views.getCitiesByState, name='getCitiesByState'),
]
