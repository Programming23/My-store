from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group


admin.site.site_header = 'لوحة التحكم'
admin.site.site_title = 'لوحة التحكم'


class CartProductInline(admin.TabularInline):
    model = CartProduct

# admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(SettingSite)
class SettingSiteAdmin(ImportExportModelAdmin):
    list_display = ['pk', 'site_title', 'phone', 'email']
    fieldsets = [
        ('معلومات الموقع', {
            'fields': ['site_title', 'site_name', 'description', 'keywords', 'currency', 'color'],
        }),
        ('الصور والرموز', {
            'fields': ['icon', 'logo', 'main_image', 'about_us_image'],
        }),
        ('معلومات التواصل', {
            'fields': ['address', 'phone', 'email', 'whatsapp', 'instagram', 'facebook', 'phone_feature',],
        }),
        ('صفحة استلام الطلبية', {
            'fields': ['imogie', 'contact_section', 'end_order', 'created_on'],
        }),
    ]

    def has_add_permission(self, request, obj=None):
        n = SettingSite.objects.all()
        if len(n) > 0:
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False
    
@admin.register(Constants)
class ContstantsAdmin(ImportExportModelAdmin):
    list_display = ['pk', 'about_us_title', 'subscription_title', 'title_products']
    fieldsets = (
        (' قسم من نحن', {
            'fields': ('about_us_title', 'about_us_content'),
        }),
        ('عناوين متنوعة', {
            'fields': ('subscription_title', 'title_products', 'title_special_products', 'title_lists', 'title_footer'),
        }),
        ('عناوين صفحة الاتصال', {
            'fields': ('contact_title', 'contact_form_title')}),
        
        ('عناوين صفحة استلام الطلبية', {
            'fields': ('command_title', 'command_details', 'contact_note', 'phone_button'),
        }),
        ('عناوين صفحة تأكيد الطلبية', {
            'fields': ('checkout_title', 'checkout_button', 'created_on'),
        }),
    )

    def has_add_permission(self, request, obj=None):
        n = Constants.objects.all()
        if len(n) > 0:
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False
    

@admin.register(Message)
class MessageAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'name', 'phone', 'subject')
    search_fields = ['name', 'phone', 'subject']

@admin.register(Subscription)
class SubscriptionAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'name', 'phone', 'created_on')
    search_fields = ['name', 'phone']

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ('pk', 'name', 'price', 'created_on')

@admin.register(BigProduct)
class BigProductAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'product', 'created_on')

@admin.register(ListProducts)
class ListProductsAdmin(ImportExportModelAdmin):
    search_fields = ['title']
    list_display = ('pk', 'title', 'created_on')

@admin.register(Features)
class FeaturesAdmin(ImportExportModelAdmin):
    search_fields = ['title', 'icon']
    list_display = ('pk', 'title', 'icon','created_on')

@admin.register(ProductType)
class ProductTypeAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ('pk', 'name', 'created_on')

@admin.register(CartProduct)
class CartProductAdmin(ImportExportModelAdmin):
    search_fields = ['product']
    list_display = ('pk', 'product', 'order', 'quantity', 'created_on')

@admin.register(Shipping)
class ShippingAdmin(ImportExportModelAdmin):
    search_fields = ['city', 'price']
    list_display = ('pk', 'city', 'price', 'created_on')

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    search_fields = ['customer', 'city', 'state']
    list_display = ('pk', 'customer', 'state', 'city', 'phone_number',  'address', 'created_on')
    inlines = [CartProductInline]
