from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "email", "phone"),
            },
        ),
    )

    list_display = ("email", "first_name", "last_name", "phone")
    list_filter = ('email', 'first_name', 'last_name')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'city', 'state', 'pin',
                    'gst_no', 'contact_no', 'contact_name', 'contact_email')
    list_display_links = ['id', 'customer_name',
                          'contact_no', 'contact_name', 'contact_email']
    list_filter = ('customer_name', 'gst_no', 'contact_no',
                   'contact_name', 'contact_email')
    search_fields = ('customer_name', 'gst_no', 'contact_no',
                     'contact_name', 'contact_email')
    list_per_page = 25


class ItemCtegoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    list_display_links = ['id', 'description']
    list_filter = ('description',)
    search_fields = ('description',)
    list_per_page = 25


class PlyDimensionMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'length_ft', 'breadth_ft',
                    'length_mt', 'breadth_mt', 'square_ft', 'square_mt')
    list_display_links = ['id', 'description', 'length_ft',
                          'breadth_ft', 'length_mt', 'breadth_mt', 'square_ft', 'square_mt']
    list_filter = ('description', 'length_ft',
                   'breadth_ft', 'length_mt', 'breadth_mt', 'square_ft', 'square_mt')
    search_fields = ('description', 'length_ft',
                     'breadth_ft', 'length_mt', 'breadth_mt', 'square_ft', 'square_mt')
    list_per_page = 25


class UomMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    list_display_links = ['id', 'description']
    list_filter = ('description',)
    search_fields = ('description',)
    list_per_page = 25


class ItemMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_category', 'description', 'uom',
                    'ply_dimension', 'unit_price', 'hsn_code', 'gst_percentage')
    list_display_links = ['id', 'item_category', 'description', 'uom',
                          'ply_dimension', 'unit_price', 'hsn_code', 'gst_percentage']
    list_filter = ('item_category', 'description', 'uom',
                   'ply_dimension', 'unit_price', 'hsn_code', 'gst_percentage')
    search_fields = ('item_category', 'description', 'uom',
                     'ply_dimension', 'unit_price', 'hsn_code', 'gst_percentage')
    list_per_page = 25


class VendorMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'state', 'pin', 'gst_no',
                    'contact_no', 'contact_name', 'contact_email')
    list_display_links = ['id', 'name', 'contact_no',
                          'contact_name', 'contact_email']
    list_filter = ('name', 'gst_no', 'contact_no',
                   'contact_name', 'contact_email')
    search_fields = ('name', 'gst_no', 'contact_no',
                     'contact_name', 'contact_email')
    list_per_page = 25


class StoreMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'state', 'pin', 'gst_no',
                    'contact_no', 'contact_name', 'contact_email', 'manager_name')
    list_display_links = ['id', 'name', 'contact_no',
                          'contact_name', 'contact_email', 'manager_name']
    list_filter = ('name', 'gst_no', 'contact_no',
                   'contact_name', 'contact_email', 'manager_name')
    search_fields = ('name', 'gst_no', 'contact_no',
                     'contact_name', 'contact_email', 'manager_name')
    list_per_page = 25


class StoreItemMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'item', 'opening_qty', 'closing_qty')
    list_display_links = ['id', 'store', 'item', 'opening_qty', 'closing_qty']
    list_filter = ('store', 'item', 'opening_qty', 'closing_qty')
    search_fields = ('store', 'item', 'opening_qty', 'closing_qty')
    list_per_page = 25


class StandardTermMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    list_display_links = ['id', 'description']
    list_filter = ('description',)
    search_fields = ('description',)
    list_per_page = 25


class PurchaseOrderHeaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'ammend_no', 'purchase_order_date',
                    'vendor', 'notes', 'total_amount')
    list_display_links = ['id', 'ammend_no', 'purchase_order_date',
                          'vendor', 'notes', 'total_amount']
    list_filter = ('ammend_no', 'purchase_order_date',
                   'vendor', 'notes', 'total_amount')
    search_fields = ('ammend_no', 'purchase_order_date',
                     'vendor', 'notes', 'total_amount')
    list_per_page = 25


class PurchaseOrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'ammend_no', 'item', 'quantity',
                    'unit_price', 'amount', 'delivery_date')
    list_display_links = ['id', 'ammend_no', 'item',
                          'quantity', 'unit_price', 'amount', 'delivery_date']
    list_filter = ('ammend_no', 'item', 'quantity',
                   'unit_price', 'amount', 'delivery_date')
    search_fields = ('ammend_no', 'item', 'quantity',
                     'unit_price', 'amount', 'delivery_date')
    list_per_page = 25


class PurchaseOrderTermsAdmin(admin.ModelAdmin):
    list_display = ('id', 'ammend_no', 'terms')
    list_display_links = ['id', 'ammend_no', 'terms']
    list_filter = ('ammend_no', 'terms')
    search_fields = ('ammend_no', 'terms')
    list_per_page = 25


class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ['id', 'name']
    list_filter = ('id', 'name')
    search_fields = ('id', 'name')
    list_per_page = 25


admin.site.register(Customer, CustomerAdmin)
admin.site.register(ItemCtegory, ItemCtegoryAdmin)
admin.site.register(PlyDimensionMaster, PlyDimensionMasterAdmin)
admin.site.register(UomMaster, UomMasterAdmin)
admin.site.register(ItemMaster, ItemMasterAdmin)
admin.site.register(VendorMaster, VendorMasterAdmin)
admin.site.register(StoreMaster, StoreMasterAdmin)
admin.site.register(StoreItemMaster, StoreItemMasterAdmin)
admin.site.register(StandardTermMaster, StandardTermMasterAdmin)
admin.site.register(PurchaseOrderHeader, PurchaseOrderHeaderAdmin)
admin.site.register(PurchaseOrderDetails, PurchaseOrderDetailsAdmin)
admin.site.register(PurchaseOrderTerms, PurchaseOrderTermsAdmin)
admin.site.register(TransactionType, TransactionTypeAdmin)
