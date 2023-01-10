from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.utils.timezone import now
from django.core.validators import RegexValidator
from django.utils.text import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=155,
        unique=True,
        error_messages={'unique': 'A user with that email already exists.'},
        help_text='Required. 150 characters or fewer. Letters, digits and @/./_ only.',
    )
    pswd_token = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    # removes email from REQUIRED_FIELDS
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    manager = UserManager()

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser


class Countries(models.Model):
    sortname = models.CharField(max_length=3)
    name = models.CharField(max_length=150)
    phonecode = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'countries'
        verbose_name_plural = 'countries'


class States(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(
        Countries, related_name='CountryState', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'states'
        verbose_name_plural = 'states'


class Cities(models.Model):
    name = models.CharField(max_length=30)
    state = models.ForeignKey(
        States, related_name='StateCity', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'cities'
        verbose_name_plural = 'cities'


class Customer(models.Model):
    customer_name = models.CharField(max_length=60, blank=False, null=False)
    address_1 = models.CharField(max_length=60, blank=False, null=False)
    address_2 = models.CharField(max_length=60, blank=True, null=True)
    country = models.ForeignKey(
        Countries, related_name='CountryCustomer', on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(
        States, related_name='StateCustomer', on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(
        Cities, related_name='CityCustomer', on_delete=models.CASCADE, blank=True, null=True)
    pin = models.CharField(max_length=6, validators=[
                           RegexValidator('^[0-9]{6}$', _('Invalid Pin Number'))])
    gst_no = models.CharField(max_length=16, blank=True, null=True)
    contact_no = models.CharField(max_length=250, blank=True, null=True)
    contact_name = models.CharField(max_length=40, blank=True, null=True)
    contact_email = models.CharField(max_length=250, blank=True, null=True)
    existing_invoice_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.customer_name

    class Meta:
        managed = True
        db_table = 'customer'
        verbose_name_plural = 'customer'


class SalesPerson(models.Model):
    salesperson_name = models.CharField(max_length=60, blank=False, null=False)
    address_1 = models.CharField(max_length=60, blank=False, null=False)
    address_2 = models.CharField(max_length=60, blank=True, null=True)
    country = models.ForeignKey(
        Countries, related_name='CountrySalesperson', on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(
        States, related_name='StateSalesperson', on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(
        Cities, related_name='CitySalesperson', on_delete=models.CASCADE, blank=True, null=True)
    pin = models.CharField(max_length=6, validators=[
                           RegexValidator('^[0-9]{6}$', _('Invalid Pin Number'))])
    contact_no = models.CharField(max_length=250, blank=True, null=True)
    contact_name = models.CharField(max_length=40, blank=True, null=True)
    contact_email = models.CharField(max_length=250, blank=True, null=True)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.salesperson_name

    class Meta:
        managed = True
        db_table = 'sales_person'
        verbose_name_plural = 'sales_person'


class ItemCtegory(models.Model):
    description = models.CharField(max_length=30, blank=False, null=False)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.description

    class Meta:
        managed = True
        db_table = 'item_category'
        verbose_name_plural = 'item_category'


class PlyDimensionMaster(models.Model):
    description = models.CharField(max_length=30, blank=False, null=False)
    length_ft = models.DecimalField(max_digits=10, decimal_places=2)
    breadth_ft = models.DecimalField(max_digits=10, decimal_places=2)
    length_mt = models.DecimalField(max_digits=10, decimal_places=2)
    breadth_mt = models.DecimalField(max_digits=10, decimal_places=2)
    square_ft = models.DecimalField(max_digits=10, decimal_places=2)
    square_mt = models.DecimalField(max_digits=10, decimal_places=2)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.description

    class Meta:
        managed = True
        db_table = 'ply_dimension_master'
        verbose_name_plural = 'ply_dimension_master'


class UomMaster(models.Model):
    description = models.CharField(max_length=30, blank=False, null=False)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.description

    class Meta:
        managed = True
        db_table = 'uom_master'
        verbose_name_plural = 'uom_master'


class ItemMaster(models.Model):
    item_category = models.ForeignKey(
        ItemCtegory, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=False, null=False)
    uom = models.ForeignKey(
        UomMaster, related_name='UomItem', on_delete=models.CASCADE, blank=True, null=True)
    ply_dimension = models.ForeignKey(
        PlyDimensionMaster, related_name='PlyItem', on_delete=models.CASCADE, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    hsn_code = models.IntegerField()
    gst_percentage = models.IntegerField()
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.description

    class Meta:
        managed = True
        db_table = 'item_master'
        verbose_name_plural = 'item_master'


class ItemAttributes(models.Model):
    item = models.ForeignKey(
        ItemMaster, on_delete=models.CASCADE, blank=True, null=True)
    attribute_name = models.CharField(max_length=30, blank=True, null=True)
    attribute_value = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.attribute_name + "=>" + self.attribute_value

    class Meta:
        managed = True
        db_table = 'item_attributes'
        verbose_name_plural = 'item_attributes'


class VendorMaster(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    address_1 = models.CharField(max_length=60, blank=False, null=False)
    address_2 = models.CharField(max_length=60, blank=True, null=True)
    country = models.ForeignKey(
        Countries, related_name='CountryVendor', on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(
        States, related_name='StateVendor', on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(
        Cities, related_name='CityVendor', on_delete=models.CASCADE, blank=True, null=True)
    pin = models.CharField(max_length=6, validators=[
                           RegexValidator('^[0-9]{6}$', _('Invalid Pin Number'))])
    gst_no = models.CharField(max_length=16, blank=True, null=True)
    contact_no = models.CharField(max_length=250, blank=True, null=True)
    contact_name = models.CharField(max_length=40, blank=True, null=True)
    contact_email = models.CharField(max_length=250, blank=True, null=True)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'vendor_master'
        verbose_name_plural = 'vendor_master'


class StoreMaster(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    address_1 = models.CharField(max_length=60, blank=False, null=False)
    address_2 = models.CharField(max_length=60, blank=True, null=True)
    country = models.ForeignKey(
        Countries, related_name='CountryStore', on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(
        States, related_name='StateStore', on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(
        Cities, related_name='CityStore', on_delete=models.CASCADE, blank=True, null=True)
    pin = models.CharField(max_length=6, validators=[
                           RegexValidator('^[0-9]{6}$', _('Invalid Pin Number'))])
    gst_no = models.CharField(max_length=16, blank=True, null=True)
    contact_no = models.CharField(max_length=250, blank=True, null=True)
    contact_name = models.CharField(max_length=40, blank=True, null=True)
    contact_email = models.CharField(max_length=250, blank=True, null=True)
    manager_name = models.CharField(max_length=40, blank=True, null=True)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'store_master'
        verbose_name_plural = 'store_master'


class StoreItemMaster(models.Model):
    store = models.ForeignKey(
        StoreMaster, related_name='StoreItemStore', on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(
        ItemMaster, related_name='StoreItemItem', on_delete=models.CASCADE, blank=True, null=True)
    opening_qty = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    on_hand_qty = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    closing_qty = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.store.name + "=>" + self.item.description

    class Meta:
        managed = True
        db_table = 'store_item_master'
        verbose_name_plural = 'store_item_master'


class StandardTermMaster(models.Model):
    description = models.TextField(blank=True, null=True)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.description

    class Meta:
        managed = True
        db_table = 'standard_term_master'
        verbose_name_plural = 'standard_term_master'


class PurchaseOrderHeader(models.Model):
    ammend_no = models.CharField(max_length=50, blank=True, null=True)
    purchase_order_no = models.CharField(max_length=15, blank=False, null=False)
    purchase_order_date = models.DateField(blank=True, null=True)
    vendor = models.ForeignKey(
        VendorMaster, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    # store = models.ForeignKey(StoreMaster, related_name='PurchaseStore', on_delete=models.CASCADE, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(default=1)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.purchase_order_no

    class Meta:
        managed = True
        db_table = 'purchase_order_header'
        verbose_name_plural = 'purchase_order_header'


class PurchaseOrderDetails(models.Model):
    ammend_no = models.CharField(max_length=50, blank=True, null=True)
    purchase_order_header = models.ForeignKey(
        PurchaseOrderHeader, on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(
        ItemMaster, related_name='PurchaseItem', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateField(blank=True, null=True)
    delivered_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.purchase_order_header.purchase_order_no

    class Meta:
        managed = True
        db_table = 'purchase_order_details'
        verbose_name_plural = 'purchase_order_details'


class PurchaseOrderTerms(models.Model):
    ammend_no = models.IntegerField(default=0)
    terms = models.ForeignKey(
        StandardTermMaster, related_name='PurchaseTerm', on_delete=models.CASCADE, blank=True, null=True)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.item.ammend_no + self.terms.description

    class Meta:
        managed = True
        db_table = 'purchase_order_terms'
        verbose_name_plural = 'purchase_order_terms'


class TransactionType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'transaction_types'
        verbose_name_plural = 'transaction_types'


class OnTransitHeader(models.Model):
    store_from = models.ForeignKey(
        StoreMaster, related_name='TransitFromStore', on_delete=models.CASCADE, blank=True, null=True)
    store_to = models.ForeignKey(
        StoreMaster, related_name='TransitToStore', on_delete=models.CASCADE, blank=True, null=True)
    transfer_number = models.CharField(max_length=15, blank=True, null=True)
    transfer_date = models.DateField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.transfer_number

    class Meta:
        managed = True
        db_table = 'on_transit_header'
        verbose_name_plural = 'on_transit_header'


class OnTransitDetails(models.Model):
    on_transit_header = models.ForeignKey(
        OnTransitHeader, on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(ItemMaster, related_name='TransitItem',
                             on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    delivered_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    delivery_date = models.DateField(blank=True, null=True)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.on_transit_header.transfer_number

    class Meta:
        managed = True
        db_table = 'on_transit_details'
        verbose_name_plural = 'on_transit_details'


class PhysicalStockHeader(models.Model):
    store = models.ForeignKey(StoreMaster, related_name='PhysicalStockStore',
                              on_delete=models.CASCADE, blank=True, null=True)
    physical_stock_check_number = models.CharField(
        max_length=15, blank=True, null=True)
    physical_stock_check_date = models.DateField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.physical_stock_check_number

    class Meta:
        managed = True
        db_table = 'physical_stock_header'
        verbose_name_plural = 'physical_stock_header'


class PhysicalStockDetails(models.Model):
    physical_stock_header = models.ForeignKey(
        PhysicalStockHeader, on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(ItemMaster, related_name='PhysicalStockItem',
                             on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    original_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.physical_stock_header.physical_stock_check_number

    class Meta:
        managed = True
        db_table = 'physical_stock_details'
        verbose_name_plural = 'physical_stock_details'


class SalesOrderHeader(models.Model):
    ammend_no = models.CharField(max_length=50, blank=True, null=True)
    sales_order_no = models.CharField(max_length=15, blank=False, null=False)
    sales_order_date = models.DateField(blank=True, null=True)
    sales_person = models.ForeignKey(
        SalesPerson, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    status = models.IntegerField(default=1)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.sales_order_no

    class Meta:
        managed = True
        db_table = 'sales_order_header'
        verbose_name_plural = 'sales_order_header'


class SalesOrderDetails(models.Model):
    ammend_no = models.CharField(max_length=50, blank=True, null=True)
    sales_order_header = models.ForeignKey(
        SalesOrderHeader, on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(
        ItemMaster, related_name='SalesItem', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateField(blank=True, null=True)
    delivered_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.sales_order_header.sales_order_no

    class Meta:
        managed = True
        db_table = 'sales_order_details'
        verbose_name_plural = 'sales_order_details'


class TransportHeader(models.Model):
    transporter_name = models.CharField(max_length=100, blank=False, null=False)
    vehicle_number = models.CharField(max_length=10, blank=False, null=False)
    vehicle_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.transporter_name

    class Meta:
        managed = True
        db_table = 'transport_header'
        verbose_name_plural = 'transport_header'


class DeliveryChallanHeader(models.Model):
    delivery_challan_number = models.CharField(max_length=15, blank=False, null=False)
    sales_order_header = models.ForeignKey(
        SalesOrderHeader, on_delete=models.CASCADE, blank=True, null=True)
    transport_header = models.ForeignKey(
        TransportHeader, on_delete=models.CASCADE, default=1)
    delivery_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.IntegerField(default=1)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.delivery_challan_number

    class Meta:
        managed = True
        db_table = 'delivery_challan_header'
        verbose_name_plural = 'delivery_challan_header'


class DeliveryChallanDetails(models.Model):
    delivery_challan_header = models.ForeignKey(
        DeliveryChallanHeader, on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(ItemMaster, related_name='DeliveryItem',
                             on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.delivery_challan_header.delivery_challan_number

    class Meta:
        managed = True
        db_table = 'delivery_challan_details'
        verbose_name_plural = 'delivery_challan_details'


class InvoiceHeader(models.Model):
    store = models.ForeignKey(StoreMaster, related_name='InvoiceStore',
                              on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(
        Customer, related_name='InvoiceCustomer', on_delete=models.CASCADE, blank=True, null=True)
    invoice_number = models.CharField(max_length=15, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    invoice_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    invoice_gst_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    carrying_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    status = models.SmallIntegerField(default=1)
    invoice_type = models.SmallIntegerField(default=1)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.invoice_number

    class Meta:
        managed = True
        db_table = 'invoice_header'
        verbose_name_plural = 'invoice_header'


class InvoiceDetails(models.Model):
    invoice_header = models.ForeignKey(
        InvoiceHeader, on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(ItemMaster, related_name='InvoiceItem',
                             on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice_item_value = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    invoice_item_gst_value = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.invoice_header.invoice_number

    class Meta:
        managed = True
        db_table = 'invoice_details'
        verbose_name_plural = 'invoice_details'


class InvoiceTerms(models.Model):
    invoice_header = models.ForeignKey(
        InvoiceHeader, on_delete=models.CASCADE, blank=True, null=True)
    term = models.ForeignKey(
        StandardTermMaster, on_delete=models.CASCADE, blank=True, null=True)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.invoice_header.invoice_number + " " + self.term.description

    class Meta:
        managed = True
        db_table = 'invoice_terms'
        verbose_name_plural = 'invoice_terms'


class PaymentMethods(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'payment_methods'
        verbose_name_plural = 'payment_methods'


class InvoicePayments(models.Model):
    invoice_header = models.ForeignKey(
        InvoiceHeader, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True)
    invoice_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gst_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    carrying_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    payment_method = models.ForeignKey(
        PaymentMethods, on_delete=models.CASCADE, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.customer.customer_name + "=>" + self.invoice_header.invoice_number

    class Meta:
        managed = True
        db_table = 'invoice_payments'
        verbose_name_plural = 'invoice_payments'


class StoreTransactionHeader(models.Model):
    vendor = models.ForeignKey(
        VendorMaster, on_delete=models.CASCADE, blank=True, null=True)
    transaction_number = models.CharField(max_length=15, blank=True, null=True)
    purchase_order_header = models.ForeignKey(
        PurchaseOrderHeader, on_delete=models.CASCADE, blank=True, null=True)
    on_transit_header = models.ForeignKey(
        OnTransitHeader, on_delete=models.CASCADE, blank=True, null=True)
    physical_stock_header = models.ForeignKey(
        PhysicalStockHeader, on_delete=models.CASCADE, blank=True, null=True)
    invoice_header = models.ForeignKey(
        InvoiceHeader, on_delete=models.CASCADE, blank=True, null=True)
    transaction_date = models.DateField(blank=True, null=True)
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE, blank=True, null=True)
    store = models.ForeignKey(
        StoreMaster, on_delete=models.CASCADE, blank=True, null=True)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_gst_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.transaction_number

    class Meta:
        managed = True
        db_table = 'store_transaction_header'
        verbose_name_plural = 'store_transaction_header'


class StoreTransactionDetails(models.Model):
    store_transaction_header = models.ForeignKey(
        StoreTransactionHeader, on_delete=models.CASCADE, default=1)
    item = models.ForeignKey(ItemMaster, related_name='StoreItem',
                             on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gst_percentage = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gst_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_date = models.DateField(blank=True, null=True)
    deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.store_transaction_header.transaction_number

    class Meta:
        managed = True
        db_table = 'store_transaction_details'
        verbose_name_plural = 'store_transaction_details'
