from DimosoApp.models import *
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from django.conf import settings

# StockCreateForm
# language
# lang




class MyUserForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        help_text="Required. Add a valid email address."
    )

    ShopName = forms.ModelChoiceField(
        queryset=MadukaYote.objects.all(),
        empty_label="-- Chagua Duka --",
        required=True
    )

    is_staff = forms.BooleanField(
        required=False,
        label="Is Staff?"
    )

    is_superuser = forms.BooleanField(
        required=False,
        label="Is Superuser?"
    )

    class Meta:
        model = MyUser
        fields = (
            "email",
            "username",
            "ShopName",
            "is_staff",
            "is_superuser",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Email {email} already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError(f"Username {username} already exists.")
        return username



         



         
        
class UserLoginForm(forms.ModelForm):
    password=forms.CharField(
        
        widget = forms.PasswordInput(attrs={'placeholder':'password', 'class':'input'})

    ) 
    email=forms.CharField(
        
        widget = forms.EmailInput(attrs={'placeholder':'email', 'class':'input'})

    )  

    class Meta:
        model=MyUser
        fields=('email', 'password')

    def clean(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            password=self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError("username or password incorrect")

class StockCreateForm(forms.ModelForm):
	


	class Meta:
		model = Stock
		fields =[
			# 'lang',
			'ShopName',
			'category', 
			'item_name', 
			'quantity', 
			'price', 
			'discount_price',
			'description',
			'image',
			'available'
			#'time_stamp',
			#'last_updated'


			]

	def clean_category(self):
		category = self.cleaned_data.get('category')
		if not category:
			raise forms.ValidationError('Please enter category')
		#for instance in Stock.objects.all():
			#if instance.category == category:
				#raise forms.ValidationError(category + 'is already created')

		return category
	def clean_item_name(self):
		item_name = self.cleaned_data.get('item_name')
		if not item_name:
			raise forms.ValidationError('Please enter item name')
		#for instance in Stock.objects.all():
			#if instance.item_name == item_name:
				#raise forms.ValidationError(item_name + ' is already created')
		return item_name



class StockSearchForm(forms.ModelForm):
	
	item_name = forms.CharField(
		required=False,
	#label=False,
		widget=forms.TextInput(attrs={'id' :'item', 'placeholder' : 'Enter Item Name'})

	)
	export_to_CSV = forms.BooleanField(required=False)
	#start_date = forms.DateTimeField(required=False)
	#end_date = forms.DateTimeField(required=False)


	class Meta:
		model = Stock
		fields =['category', 'item_name']

class StockUpdateForm(forms.ModelForm):
	

	class Meta:
		model = Stock
		fields =[
			# 'lang',
			'category', 
			'item_name', 
			'quantity', 
			'price', 
			'discount_price',
			'description',
			'image',
			'available'


			]
		

class IssueForm(forms.ModelForm):
	is_issued = forms.BooleanField(
		required=True,
	)
	issue_quantity = forms.IntegerField(
		required=True,
	)
	receive_amount = forms.IntegerField(
		required=True,
	)
	

	class Meta:
		model = Stock
		fields =['issue_quantity', 'issue_to','issue_by','receive_amount','is_issued']
class ReceiveForm(forms.ModelForm):
	is_received = forms.BooleanField(
		required=True,
	#label=False,
		

	)
	receive_quantity = forms.IntegerField(
		required=True,
	)
	issued_amount = forms.IntegerField(
		required=True,
	)
	

	class Meta:
		model = Stock
		fields =['receive_quantity','receive_by','issued_amount','is_received']

class ReorderLevelForm(forms.ModelForm):
	

	class Meta:
		model = Stock
		fields =['reorder_level']

#form ya kurekodi kiasi ulichopata baada ya kuuza bidhaa
class ReceiveAmountForm(forms.ModelForm):
	

	class Meta:
		model = Stock
		fields =['receive_amount']
#form ya kurekodi kiasi ulichotoa baada ya kununua  bidhaa
class IssuedAmountForm(forms.ModelForm):
	

	class Meta:
		model = Stock
		fields =['issued_amount']



PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "Promo code",
        'aria-label ': "Recipient's username",
        'aria-describedby': "basic-addon2"
    }), max_length=50)

class AddressForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField()
    country = CountryField(blank_label="Select country").formfield(widget=CountrySelectWidget(attrs={
        "class": "custom-select d-block w-100"
    }))
    zip = forms.CharField(required=False)
    save_info = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)


class ContactMeForm(forms.ModelForm):
	

	class Meta:
		model = ContactMe
		fields =['email','username','phone','place','message']

