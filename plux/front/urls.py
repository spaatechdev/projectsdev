from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('myProfile', views.myProfile, name='myProfile'),
    path('userList', views.userList, name='userList'),
    path('forgot/', views.forgot, name='forgot'),
    path('enter_otp/',views.enter_otp,name='enter_otp'),
    path('password_reset/',views.password_reset,name='password_reset'),



    path('customerList', views.customerList, name='customerList'),
    path('customerAdd', views.customerAdd, name='customerAdd'),
    path('customerEdit/<int:id>', views.customerEdit, name='customerEdit'),
    path('customerDelete/<int:id>', views.customerDelete, name='customerDelete'),
    path('customerImport', views.customerImport, name='customerImport'),
    path('downloadCustomerExcel', views.downloadCustomerExcel, name='downloadCustomerExcel'),

    path('salespersonList', views.salespersonList, name='salespersonList'),
    path('salespersonAdd', views.salespersonAdd, name='salespersonAdd'),
    path('salespersonEdit/<int:id>', views.salespersonEdit, name='salespersonEdit'),
    path('salespersonDelete/<int:id>', views.salespersonDelete, name='salespersonDelete'),
    path('salespersonImport', views.salespersonImport, name='salespersonImport'),
    path('downloadSalespersonExcel', views.downloadSalespersonExcel, name='downloadSalespersonExcel'),
    
    path('uomList', views.uomList, name='uomList'),
    path('uomAdd', views.uomAdd, name='uomAdd'),
    path('uomEdit/<int:id>', views.uomEdit, name='uomEdit'),
    path('uomDelete/<int:id>', views.uomDelete, name='uomDelete'),
    path('uomImport', views.uomImport, name='uomImport'),
    path('downloadUomExcel', views.downloadUomExcel, name='downloadUomExcel'),
    
    path('storeList', views.storeList, name='storeList'),
    path('storeImport', views.storeImport, name='storeImport'),
    path('downloadStoreExcel', views.downloadStoreExcel, name='downloadStoreExcel'),

    path('vendorList', views.vendorList, name='vendorList'),
    path('vendorAdd', views.vendorAdd, name='vendorAdd'),
    path('vendorEdit/<int:id>', views.vendorEdit, name='vendorEdit'),
    path('vendorDelete/<int:id>', views.vendorDelete, name='vendorDelete'),
    path('vendorImport', views.vendorImport, name='vendorImport'),
    path('downloadVendorExcel', views.downloadVendorExcel, name='downloadVendorExcel'),

    path('uomList', views.uomList, name='uomList'),

    path('storeList', views.storeList, name='storeList'),
    path('storeAdd', views.storeAdd, name='storeAdd'),
    path('storeEdit/<int:id>', views.storeEdit, name='storeEdit'),
    path('storeDelete/<int:id>', views.storeDelete, name='storeDelete'),
    
    path('itemCategoryList', views.itemCategoryList, name='itemCategoryList'),
    path('itemCategoryAdd', views.itemCategoryAdd, name='itemCategoryAdd'),
    path('itemCategoryEdit/<int:id>', views.itemCategoryEdit, name='itemCategoryEdit'),
    path('itemCategoryDelete/<int:id>', views.itemCategoryDelete, name='itemCategoryDelete'),
    path('itemCategoryImport', views.itemCategoryImport, name='itemCategoryImport'),
    path('downloaditemCategoryExcel', views.downloaditemCategoryExcel, name='downloaditemCategoryExcel'),
    
    path('plyDimensionList', views.plyDimensionList, name='plyDimensionList'),
    path('plyDimensionAdd', views.plyDimensionAdd, name='plyDimensionAdd'),
    path('plyDimensionEdit/<int:id>', views.plyDimensionEdit, name='plyDimensionEdit'),
    path('plyDimensionDelete/<int:id>', views.plyDimensionDelete, name='plyDimensionDelete'),
    path('plyDimensionImport', views.plyDimensionImport, name='plyDimensionImport'),
    path('downloadplyDimensionExcel', views.downloadplyDimensionExcel, name='downloadplyDimensionExcel'),

    path('itemList', views.itemList, name='itemList'),
    path('itemAdd', views.itemAdd, name='itemAdd'),
    path('itemEdit/<int:id>', views.itemEdit, name='itemEdit'),
    path('itemDelete/<int:id>', views.itemDelete, name='itemDelete'),
    path('itemImport', views.itemImport, name='itemImport'),
    path('downloadItemExcel', views.downloadItemExcel, name='downloadItemExcel'),

    path('storeItemList', views.storeItemList, name='storeItemList'),
    path('storeItemAdd', views.storeItemAdd, name='storeItemAdd'),
    path('storeItemEdit/<int:id>', views.storeItemEdit, name='storeItemEdit'),
    path('storeItemDelete/<int:id>', views.storeItemDelete, name='storeItemDelete'),
    path('storeItemImport', views.storeItemImport, name='storeItemImport'),
    path('downloadstoreItemExcel', views.downloadstoreItemExcel, name='downloadstoreItemExcel'),

    path('purchaseOrderList', views.purchaseOrderList, name='purchaseOrderList'),
    path('purchaseOrderAdd', views.purchaseOrderAdd, name='purchaseOrderAdd'),
    path('purchaseOrderEdit/<int:id>', views.purchaseOrderEdit, name='purchaseOrderEdit'),
    path('purchaseOrderDelete/<int:id>', views.purchaseOrderDelete, name='purchaseOrderDelete'),
    path('purchaseOrderDetailsList/<int:header_id>', views.purchaseOrderDetailsList, name='purchaseOrderDetailsList'),


    path('salesOrderList', views.salesOrderList, name='salesOrderList'),
    path('salesOrderAdd', views.salesOrderAdd, name='salesOrderAdd'),
    path('salesOrderEdit/<int:id>', views.salesOrderEdit, name='salesOrderEdit'),
    path('salesOrderDelete/<int:id>', views.salesOrderDelete, name='salesOrderDelete'),
    path('salesOrderDetailsList/<int:header_id>', views.salesOrderDetailsList, name='salesOrderDetailsList'),

    path('standardTermList', views.standardTermList, name='standardTermList'),
    path('standardTermAdd', views.standardTermAdd, name='standardTermAdd'),
    path('standardTermEdit/<int:id>', views.standardTermEdit, name='standardTermEdit'),
    path('standardTermDelete/<int:id>', views.standardTermDelete, name='standardTermDelete'),

    path('storeTransactionList', views.storeTransactionList, name='storeTransactionList'),
    path('storeTransactionAdd', views.storeTransactionAdd, name='storeTransactionAdd'),
    path('storeTransactionEdit/<int:id>', views.storeTransactionEdit, name='storeTransactionEdit'),
    path('storeTransactionDelete/<int:id>', views.storeTransactionDelete, name='storeTransactionDelete'),
    path('storeTransactionDetailsList/<int:header_id>', views.storeTransactionDetailsList, name='storeTransactionDetailsList'),

    path('onTransitOrderList', views.onTransitOrderList, name='onTransitOrderList'),
    path('onTransitOrderDetailsList/<int:header_id>', views.onTransitOrderDetailsList, name='onTransitOrderDetailsList'),

    path('invoiceList', views.invoiceList, name='invoiceList'),
    path('invoiceAdd', views.invoiceAdd, name='invoiceAdd'),
    path('invoiceDetailsList/<int:header_id>', views.invoiceDetailsList, name='invoiceDetailsList'),

    path('getVendorPurchaseOrders', csrf_exempt(views.getVendorPurchaseOrders), name='getVendorPurchaseOrders'),
    path('getPurchaseOrderDetails', csrf_exempt(views.getPurchaseOrderDetails), name='getPurchaseOrderDetails'),
    path('getTransactionType', csrf_exempt(views.getTransactionType), name='getTransactionType'),
    path('getExceptStores', csrf_exempt(views.getExceptStores), name='getExceptStores'),
    path('getItemsDetailsByStore', csrf_exempt(views.getItemsDetailsByStore), name='getItemsDetailsByStore'),
    path('getExceptedStoreItems', csrf_exempt(views.getExceptedStoreItems), name='getExceptedStoreItems'),
    path('getTransferDetails', csrf_exempt(views.getTransferDetails), name='getTransferDetails'),
    
    path('getStatesByCountry', views.getStatesByCountry, name='getStatesByCountry'),
    path('getCitiesByState', views.getCitiesByState, name='getCitiesByState'),
]
