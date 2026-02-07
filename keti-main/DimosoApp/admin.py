from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from DimosoApp.models import *
from DimosoApp.forms import *

from import_export.admin import ImportExportModelAdmin
# language
# Register your models here.
class MyUserAdmin(BaseUserAdmin):
    list_display=('username', 'email', 'company_name', 'profile_image', 'date_joined', 'last_login', 'is_admin', 'is_active')
    search_fields=('email', 'first_name', 'last_name')
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email', 'username', 'first_name', 'middle_name', 'last_name', 'company_name', 'phone', 'profile_image', 'password1', 'password2'),
        }),
    )

    ordering=('email',)
class PostAdmin(admin.ModelAdmin):
	list_display = ["name", "post_date"]
	#prepopulated_fields={'slug':('name',)}

@admin.register(MadukaYote)
class MadukaYoteAdmin(ImportExportModelAdmin):
	list_display = ["ShopName", "ShopLocation", "quantity"]
	#prepopulated_fields={'slug':('name',)}

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
	list_display = ["name"]
	#prepopulated_fields={'slug':('name',)}

@admin.register(Stock)
class StockAdmin(ImportExportModelAdmin):
	list_display = ["id", "reg_no","item_name", "ShopName", "category", "quantity", "receive_quantity", "receive_by","issue_quantity","issue_by","issue_to","reorder_level","is_issued","is_received"]
	form = StockCreateForm
	#list_filter =['category']
	search_fields = ['category', 'item_name']
	# list_filter= ['lang']


@admin.register(MauzoYote)  
class MauzoYoteAdmin(ImportExportModelAdmin):
    list_display = ["id","JinaLaBidhaa","ShopName","Category","HelaUliyopokea", "KiasiChaBidhaaKilichotoka", "ImeuzwaNa", "Created", "Updated"]
    list_filter =["Created", "ShopName"]
    search_fields = ["JinaLaBidhaa"]


@admin.register(ManunuziYote)  
class ManunuziYoteAdmin(ImportExportModelAdmin):
    list_display = ["id","JinaLaBidhaa","ShopName","Category","HelaUliyotoa", "KiasiChaBidhaaUlichonunua", "ImenunuliwaNa", "Created", "Updated"]
    list_filter =["Created", "ShopName"]
    search_fields = ["JinaLaBidhaa"]


class StockHistoryAdmin(admin.ModelAdmin):
	list_display = ["category", "item_name", "quantity", "receive_by","issue_by","issue_to","reorder_level"]
	#form = StockCreateForm
	#list_filter =['category']
	search_fields = ['category', 'item_name']

class OrderItemAdmin(admin.ModelAdmin):
	list_display = ["user", "item", "quantity", "ordered"]
	#form = StockCreateForm
	#list_filter =['category']
	search_fields = ['user', 'item']

class OrderAdmin(admin.ModelAdmin):
	list_display = ["user", "start_date", "ordered_date","ordered"]
	#form = StockCreateForm
	#list_filter =['category']
	search_fields = ['user', 'item']


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'default'
    ]
# class LanguageAdmin(admin.ModelAdmin):
# 	list_display = ["name", "code", "status"]
# 	#form = StockCreateForm
# 	#list_filter =['category']
# 	list_filter = ['status']
class ContactMeAdmin(admin.ModelAdmin):
	list_display = ["username", "email", "place","phone","send_date","to_dimoso_email"]
	#form = StockCreateForm
	#list_filter =['category']
	search_fields = ['username', 'email']

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Post, PostAdmin)
# admin.site.register(MadukaYote, MadukaYoteAdmin)
# admin.site.register(Stock, StockCreateAdmin)
# admin.site.register(Category)
admin.site.register(StockHistory, StockHistoryAdmin)

admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)

admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Address, AddressAdmin)
# admin.site.register(Language, LanguageAdmin)
admin.site.register(ContactMe, ContactMeAdmin)
