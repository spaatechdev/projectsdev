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
    
    path('vendorList', views.vendorList, name='vendorList'),
    
    path('uomList', views.uomList, name='uomList'),
    path('uomAdd', views.uomAdd, name='uomAdd'),
    path('uomEdit/<int:id>', views.uomEdit, name='uomEdit'),
    path('uomDelete/<int:id>', views.uomDelete, name='uomDelete'),
    
    path('storeList', views.storeList, name='storeList'),

    path('itemCategoryList', views.itemCategoryList, name='itemCategoryList'),
    path('itemCategoryAdd', views.itemCategoryAdd, name='itemCategoryAdd'),
    path('itemCategoryEdit/<int:id>', views.itemCategoryEdit, name='itemCategoryEdit'),
    path('itemCategoryDelete/<int:id>', views.itemCategoryDelete, name='itemCategoryDelete'),
    
    path('plyDimensionList', views.plyDimensionList, name='plyDimensionList'),
    path('plyDimensionAdd', views.plyDimensionAdd, name='plyDimensionAdd'),
    path('plyDimensionEdit/<int:id>', views.plyDimensionEdit, name='plyDimensionEdit'),
    path('plyDimensionDelete/<int:id>', views.plyDimensionDelete, name='plyDimensionDelete'),

    path('getStatesByCountry', views.getStatesByCountry, name='getStatesByCountry'),
    path('getCitiesByState', views.getCitiesByState, name='getCitiesByState'),
]
