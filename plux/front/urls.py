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
    path('storeList', views.storeList, name='storeList'),
    path('getStatesByCountry', views.getStatesByCountry, name='getStatesByCountry'),
    path('getCitiesByState', views.getCitiesByState, name='getCitiesByState'),
]
