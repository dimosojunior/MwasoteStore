from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from datetime import datetime, date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django_countries.fields import CountryField
from django.forms import ModelForm, TextInput, Textarea
from django.http import request
from django.utils import timezone
from django.utils.safestring import mark_safe

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser
import random
from datetime import timedelta
from django.utils.timezone import now #, timedelta
# language


def generated_reg_no():
    last_reg_no = Stock.objects.all().order_by('id').last()
    if not last_reg_no:
        return '1'
    reg_no = last_reg_no.reg_no
    new_reg_no = int(reg_no) + 1
    return new_reg_no

class MadukaYote(models.Model):
    ShopName = models.CharField(verbose_name="Jina la Duka", max_length=200, blank=True, null=True)
    ShopLocation = models.CharField(verbose_name="Mahali Lilipo", max_length=200, blank=True, null=True)
    quantity = models.IntegerField(verbose_name="Kiasi Cha Bidhaa Zilizopo", default='0', blank=True, null=True)

    image = models.ImageField(blank=True, null=True, upload_to="media/")

    def __str__(self):
        return self.ShopName

# Create your models here.

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("Your user name is required")
        
        

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,

        )
        user.is_admin=True
        user.is_staff=True
        
        user.is_superuser=True
        user.save(using=self._db)
        return user

    

  #HII NI PATH KWA AJILI YA KUHIFADHI HIZO IMAGE      
def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"44.jpg"}'

#HII NI KWA AJILI YA KUPATA DEFAULT IMAGE KM MTU ASIPO INGIZA IMAGE ILI ISILETE ERRORS
def get_default_profile_image():
    return "media/44.jpg"

class MyUser(AbstractBaseUser):
    ShopName = models.ForeignKey(MadukaYote, verbose_name="Duka", on_delete=models.CASCADE, blank=True,null=True)
    email=models.EmailField(verbose_name="email", max_length=100, unique=True)
    first_name=models.CharField(verbose_name="first name", max_length=100, unique=False)
    username=models.CharField(verbose_name="user name", max_length=100, unique=True)
    middle_name=models.CharField(verbose_name="middle name", max_length=100, unique=False)
    last_name=models.CharField(verbose_name="last name", max_length=100, unique=False)
    company_name=models.CharField(verbose_name="company name", max_length=100, unique=False)
    phone=models.CharField(verbose_name="phone", max_length=15)
    profile_image = models.ImageField(upload_to='get_profile_image_filepath', blank=True, null=True)
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    


    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['username']
    
    objects=MyUserManager()

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True






        
class Post(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    
    title = RichTextUploadingField(blank=True, null=True)
    title_tag = models.CharField(max_length=200, blank=True, null=True)
    body = RichTextUploadingField(blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="media/")

# class Language(models.Model):
#     name= models.CharField(max_length=20)
#     code= models.CharField(max_length=5)
#     status=models.BooleanField()
#     create_at=models.DateTimeField(auto_now_add=True)
#     update_at=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# llist = Language.objects.filter(status=True)
# list1 = []
# for rs in llist:
#     list1.append((rs.code,rs.name))
# langlist = (list1)

class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product_by_category', args=[self.id])


category_choices = (
    ('Furniture', 'Furniture'),
    ('Electrical Equipments', 'Electrical Equipments'),
    ('Phone', 'Phone'),
)

class Stock(models.Model):
    reg_no= models.CharField(max_length=100000, default=generated_reg_no,  editable=False,blank=True,null=True)

    ShopName = models.ForeignKey(MadukaYote, verbose_name="Duka", on_delete=models.CASCADE, blank=True,null=True)
    #lang =  models.CharField(max_length=6, choices=langlist, blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True,null=True)
    item_name = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=200, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=200, blank=True, null=True)
    issue_to = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    reorder_level = models.IntegerField(default='10', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False,auto_now=True, blank=True, null=True )
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True,blank=True, null=True )
    price = models.FloatField(blank=True, null=True )
    discount_price = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='media/productImages', blank=True, null=True)
    available=models.BooleanField(default=True, blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True, blank=True, null=True)
        
    status = models.CharField(max_length=200, blank=True, null=True )
    amount = models.IntegerField(default='0', blank=True, null=True)
    receive_amount = models.IntegerField(default='0', blank=True, null=True)
    issued_amount = models.IntegerField(default='0', blank=True, null=True)
    purchasing_amount = models.IntegerField(default='0', blank=True, null=True)
    sales_amount = models.IntegerField(default='0', blank=True, null=True)
    is_issued = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)

    #def lifespan(self):
        #return '%s - present' % self.last_updated.strftime('%d/%m/%Y')

    #export_to_CSV = models.BooleanField(default=False)
    def __str__(self):
        return self.item_name
    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'id': self.id})
    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'id': self.id})
    def get_remove_single_from_cart_url(self):
        return reverse('remove_single_from_cart', kwargs={'id': self.id})
    








class ManunuziYote(models.Model):
    reg_no = models.CharField(verbose_name="Namba Ya Bidhaa", max_length=100000, blank=True, null=True)

    JinaLaBidhaa = models.CharField(verbose_name="Jina La Bidhaa Uliyonunua", max_length=500, blank=True, null=True)
    ShopName = models.CharField(verbose_name="Duka lililopokea Bidhaa", max_length=500, blank=True, null=True)
    Category = models.CharField(verbose_name="Category", max_length=500, blank=True, null=True)
    
    HelaUliyotoa = models.IntegerField(verbose_name="Hela Uliyotoa", blank=True, null=True, default=0)
    KiasiChaBidhaaUlichonunua = models.IntegerField(verbose_name="Kiasi Cha Bidhaa Ulichonunua", blank=True, null=True, default=0)

    
    

    ImenunuliwaNa = models.CharField(verbose_name="Imenunuliwa Na ?", max_length=500, blank=True, null=True)
    
    Created = models.DateTimeField(default=now, blank=True, null=True)
    Updated = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name_plural = "Manunuzi Yote"

    def __str__(self):
        return f"{self.JinaLaBidhaa}"




class MauzoYote(models.Model):
    reg_no = models.CharField(verbose_name="Namba Ya Bidhaa", max_length=100000, blank=True, null=True)

    JinaLaBidhaa = models.CharField(verbose_name="Jina La Bidhaa", max_length=500, blank=True, null=True)
    ShopName = models.CharField(verbose_name="Duka Lilipouzwa", max_length=500, blank=True, null=True)
    Category = models.CharField(verbose_name="Category", max_length=500, blank=True, null=True)
    
    HelaUliyopokea = models.IntegerField(verbose_name="Hela Uliyopokea", blank=True, null=True, default=0)
    KiasiChaBidhaaKilichotoka = models.IntegerField(verbose_name="Kiasi Cha Bidhaa Kilichotoka", blank=True, null=True, default=0)

    
    

    ImeuzwaNa = models.CharField(verbose_name="Imeuzwa Na ?", max_length=500, blank=True, null=True)
    
    Created = models.DateTimeField(default=now, blank=True, null=True)
    Updated = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name_plural = "Mauzo Yote"

    def __str__(self):
        return f"{self.JinaLaBidhaa}"










class OrderItem(models.Model):
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Stock, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_final_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()

   


class Order(models.Model):
   # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
   
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    address = models.ForeignKey(
        "Address", on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        "Payment", on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        "Coupon", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        
        
        return total










class StockHistory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True,null=True)
    item_name = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=200, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=200, blank=True, null=True)
    issue_to = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    date = models.DateTimeField(auto_now_add=False, auto_now=False,blank=True, null=True )

    #export_to_CSV = models.BooleanField(default=False)



class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    apartment_address = models.CharField(max_length=200)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=200)
    save_info = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    use_default = models.BooleanField(default=False)
    payment_option = models.CharField(choices=PAYMENT_CHOICES, max_length=2)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    charge_id = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    amount = models.IntegerField()

    def __str__(self):
        return self.code


class ContactMe(models.Model):
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(max_length=1000, blank=True, null=True)
    
    username = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(default='+255',max_length=13, blank=True, null=True)
    email = models.EmailField(default='@gmail.com', blank=True, null=True)
    place = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    send_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    to_dimoso_email = models.EmailField(default='juniordimoso8@gmail.com', blank=True, null=True)
    
