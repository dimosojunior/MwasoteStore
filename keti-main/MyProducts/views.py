from django.shortcuts import render
from django.db.models.query import QuerySet
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView, View

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.db.models import Q
import datetime
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter
#from reportlab.lib.pagesizes import landscape
#from reportlab.platypus import Image
import os
from django.conf import settings
from django.http import HttpResponse
#from django.template.loader import get_template
#from xhtml2pdf import pisa
#from django.contrib.staticfiles import finders
import calendar
from calendar import HTMLCalendar
from DimosoApp.models import *
from DimosoApp.forms import *
#from hitcount.views import HitCountDetailView
from django.core.mail import send_mail
from django.conf import settings
import csv
import stripe
import datetime
from django.utils import timezone
import json
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.contrib.auth.models import User

stripe.api_key = ""


# Create your views here.
def base(request):
    order = Order.objects.get(user=request.user, ordered=False)
    x=datetime.datetime.today()
    current_date = x.strftime('%d-%m-%Y %H:%M')
    context={
        "current_date":current_date,
        "order":order
    }
    return render(request, "MyProducts/base.html",context)
def payment_error_message(request):
	return render(request, "MyProducts/payment_error_message.html")


def home(request,category_id=None):
    x=datetime.datetime.today()
    current_date = x.strftime('%d-%m-%Y %H:%M')
    trans = _('hello')
    trans = translate(language='sw')
    #form = StockCreateForm(request.POST or None)


    category = None




    categories = Category.objects.all()
    item = Stock.objects.all().order_by('-id')

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(item,12)
    page = request.GET.get('page')
    try:
        item=paginator.page(page)
    except PageNotAnInteger:
        item=paginator.page(1)
    except EmptyPage:
        item=paginator.page(paginator.num_pages)
    
    form = StockSearchForm(request.POST or None)




    #MWISHO HAP

    if category_id:
        #add hii kwa ajili ya pagination ukiselect category
        item = Stock.objects.all()

        category = get_object_or_404(Category,id=category_id)
        item= item.filter(category=category)



    #To SET  PAGINATION IN STOCK LIST PAGE
        paginator = Paginator(item,8)
        page = request.GET.get('page')
        try:
            item=paginator.page(page)
        except PageNotAnInteger:
            item=paginator.page(1)
        except EmptyPage:
            item=paginator.page(paginator.num_pages)
        #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

    #kwa ajili kusearch product

    
	


    context = {
        "current_date":current_date,
        "trans":trans,
        "categories":categories, 
        "category":category,
        "item":item,
        "page":page
    }

    return render(request, 'MyProducts/home.html', context)


def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext('hello')
    finally:
        activate(cur_language)
    return text


def search_product(request):
    
    query=None
    results=[]
    x=datetime.datetime.today()
    current_date = x.strftime('%d-%m-%Y %H:%M')
    if request.method == "GET":
        query=request.GET.get("search")
        results=Stock.objects.filter(Q(item_name__icontains=query))
    context={
        "current_date":current_date,
        "query":query,
        "results":results
    }
    return render(request, 'MyProducts/search_product.html',context)

def search_autoco_product(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(item_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    product = Stock.objects.filter(search)
    mylist= []
    mylist += [x.item_name for x in product]
    return JsonResponse(mylist, safe=False) 

def product_details(request, id):
    x=datetime.datetime.today()
    current_date = x.strftime('%d-%m-%Y %H:%M')
    
    category = Category.objects.all()

    item = Stock.objects.get(id=id)

    

	




    context = {
		"current_date":current_date, 
		"category":category,
		"item":item,
	}

    return render(request, 'MyProducts/product_details.html', context)


def add_to_cart(request, id):
	item = get_object_or_404(Stock, id=id)
	if item.quantity == 0:
		messages.info(request, f"There is no any {item.item_name} product(s) in a stock for now")
		return redirect('product_details', id=id)
	else:
	    
	    order_item, created = OrderItem.objects.get_or_create(
	        item=item,
	        user=request.user,
	        ordered=False,
	    )
	    order_qs = Order.objects.filter(user=request.user, ordered=False)
	    if order_qs.exists():
	        order = order_qs[0]
	        if order.items.filter(item_id=item.id).exists():
	            order_item.quantity += 1
	            order_item.save()
	            messages.success(request, f"{item}'s quantity was updated")
	            return redirect('order_summary')
	        else:
	            order.items.add(order_item)
	            order.save()
	            messages.success(request, f"{item} was added to your Order")
	            return redirect('order_summary')

	    else:
	        ordered_date = timezone.now()
	        order = Order.objects.create(
	            user=request.user, ordered=False, ordered_date=ordered_date)
	        order.items.add(order_item)
	        order.save()
	        messages.success(request, f"{item} was added to your Order")
	        return redirect('order_summary')


def remove_from_cart(request, id):

    item = get_object_or_404(Stock, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_id=item.id).exists():
            order.items.remove(order_item)
            order.save()
            messages.success(request, f"{item.item_name} was removed from your Order")
                
            return redirect('order_summary')
        else:
            messages.info(request, f"{item.item_name} was not in your Order")
            return redirect('order_summary')
    else:
        messages.info(request, "You don't have an active order!")
        return redirect('order_summary')



def remove_single_from_cart(request, id):
    item = get_object_or_404(Stock, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id).exists():
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order.save()
            messages.success(request, f"{item.item_name}'s quantity was updated")
            return redirect('order_summary')
        else:
            messages.info(request, f"{item.item_name} was not in your Order")
            return redirect('order_summary')
    else:
        messages.info(request, "You don't have an active Order!")
        return redirect('order_summary')

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order':order
        }
        return render(self.request, 'MyProducts/order_summary.html',context)








class CheckoutView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        # address = Address.objects.get(user=self.request.user, default=True)
        coupon_form = CouponForm()
        form = AddressForm()
        context = {
            'form': form,
            'order': order,
            'coupon_form': coupon_form,
            "DISPLAY_COUPON_FORM": True
            # 'address': address
        }
        return render(self.request, 'MyProducts/checkout.html', context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = AddressForm(self.request.POST or None)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            save_info = form.cleaned_data.get('save_info')
            use_default = form.cleaned_data.get('use_default')
            payment_option = form.cleaned_data.get('payment_option')

            address = Address(
                user=self.request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                zip=zip,
            )
            address.save()
            if save_info:
                address.default = True
                address.save()

            order.address = address
            order.save()

            if use_default:
                address = Address.objects.get(
                    user=self.request.user, default=True)
                order.address = address
                order.save()

            if payment_option == "S":
                return redirect('payment', payment_option="stripe")

            if payment_option == "P":
                return redirect('payment', payment_option="paypal")
            messages.info(self.request, "Invalid payment option")
            return redirect('checkout')
        else:
            print('form invalid')
            return redirect('checkout')


def payment_complete(request):
    x=datetime.datetime.today()
    current_date = x.strftime('%d-%m-%Y %H:%M')
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, ordered=False, id=body['orderID'])
    payment = Payment(
        user=request.user,
        stripe_charge_id=body['payID'],
        amount=order.get_total()
    )
    payment.save()

    # assign the payment to order
    order.payment = payment
    order.ordered = True
    order.save()
    messages.success(request, "Payment was successful")
    return redirect('home')


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)

        context = {
            'order': order,
            "DISPLAY_COUPON_FORM": False

        }
        return render(self.request, 'MyProducts/payment.html', context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        try:
            customer = stripe.Customer.create(
                email=self.request.user.email,
                description=self.request.user.username,
                source=self.request.POST['stripeToken']
            )
            amount = order.get_total()
            charge = stripe.Charge.create(
                amount=amount * 100,
                currency="usd",
                customer=customer,
                description="Test payment for buteks online",
            )
            payment = Payment(
                user=self.request.user,
                stripe_charge_id=charge['id'],
                amount=amount
            )
            payment.save()

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Payment was successful")
            return redirect('payment_error_message')
        except stripe.error.CardError as e:
            messages.info(self.request, f"{e.error.message}")
            return redirect('payment_error_message')
        except stripe.error.InvalidRequestError as e:
            messages.success(self.request, "Invalid request")
            return redirect('payment_error_message')
        except stripe.error.AuthenticationError as e:
            messages.success(self.request, "Authentication error")
            return redirect('payment_error_message')
        except stripe.error.APIConnectionError as e:
            messages.success(self.request, "Check your connection")
            return redirect('payment_error_message')
        except stripe.error.StripeError as e:
            messages.success(
                self.request, "There was an error please try again")
            return redirect('payment_error_message')
        except Exception as e:
            messages.success(
                self.request, "A serious error occured we were notified")
            return redirect('payment_error_message')


class CouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = Coupon.objects.get(code=code)
                order.save()
                messages.success(self.request, "Successfully added coupon !")
                return redirect('checkout')
            except ObjectDoesNotExist:
                messages.success(self.request, "You don't have an active order")
                return redirect('home')
        messages.success(self.request, "Enter a valid coupon code")
        return redirect('checkout')


def contact_me(request):
    
    form = ContactMeForm()
    order = Order.objects.get(user=request.user, ordered=False)
    if request.method == "POST":
        form = ContactMeForm(request.POST or None)
        if form.is_valid:
            form.save()
            '''
            email = request.POST.get('email')
            message = request.POST.get('message')
            phone = request.POST.get('phone')
            place = request.POST.get('place')
            send_mail(phone,message,settings.EMAIL_HOST_USER,[email],  fail_silently=True)
            messages.success(request,"Email sent Successfully to juniordimoso@gmail.com")
            return redirect('home')
            '''
            to = request.POST['email']
            username = request.POST['username']
            phone = request.POST['phone']
            place = request.POST['place']
            message = request.POST['message']
           # send_date = request.POST['send_date']
            #to_dimoso_email = request.POST['to_dimoso_email']
            to_dimoso_email = "juniordimoso8@gmail.com"
            
                        
            html_content = render_to_string(
                "MyProducts/email_template.html",
                {
                'title':'Student Report System ', 
                'username':username,
                'phone':phone,
                'place':place,
                "message":message,
                "to":to
               # "send_date":send_date
                
                
                
                })
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
            "testing",
            #content
            text_content,
            #from email
            settings.EMAIL_HOST_USER,
            #to
            [to_dimoso_email]


            )
            email.attach_alternative(html_content,"text/html")
            email.send(fail_silently=True)


            #HIZI NI KWA AJILI KUTUMA EMAIL ENDAPO MTU AKIJISAJILI
            username = request.POST['username']
            #last_name = request.POST['last_name']
            email = request.POST['email']
            subject = "Welcome to KING STORE ONLINE SYSTEM"
            message = f"Ahsante  {username} kwa kuweka oda ya bidhaa kutoka kwetu, wasiliana nasi kupitia Email: {to_dimoso_email} au Kwa namba ya simu 0628431507"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            #ZINAISHIA HAPA ZA KUTUMA EMAIL
            messages.success(request, f"Email sent Successfully to {to_dimoso_email}")
            return redirect('home')
        

    context = {
            'form': form,
            'order': order,
            
        }
    return render(request, "MyProducts/contact_me.html",context)

def contact_me_if_not_registered(request):
    
    form = ContactMeForm()
    #order = Order.objects.get(user=request.user, ordered=False)
    if request.method == "POST":
        form = ContactMeForm(request.POST or None)
        if form.is_valid:
            form.save()
            '''
            email = request.POST.get('email')
            message = request.POST.get('message')
            phone = request.POST.get('phone')
            place = request.POST.get('place')
            send_mail(phone,message,settings.EMAIL_HOST_USER,[email],  fail_silently=True)
            messages.success(request,"Email sent Successfully to juniordimoso@gmail.com")
            return redirect('home')
            '''
            to = request.POST['email']
            username = request.POST['username']
            phone = request.POST['phone']
            place = request.POST['place']
            message = request.POST['message']
           # send_date = request.POST['send_date']
            #to_dimoso_email = request.POST['to_dimoso_email']
            to_dimoso_email = "juniordimoso8@gmail.com"
            
                        
            html_content = render_to_string(
                "MyProducts/email_template.html",
                {
                'title':'Student Report System ', 
                'username':username,
                'phone':phone,
                'place':place,
                "message":message,
                "to":to
               # "send_date":send_date
                
                
                
                })
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
            "testing",
            #content
            text_content,
            #from email
            settings.EMAIL_HOST_USER,
            #to
            [to_dimoso_email]


            )
            email.attach_alternative(html_content,"text/html")
            email.send(fail_silently=True)


            #HIZI NI KWA AJILI KUTUMA EMAIL ENDAPO MTU AKIJISAJILI
            username = request.POST['username']
            #last_name = request.POST['last_name']
            email = request.POST['email']
            subject = "Welcome to KING STORE ONLINE SYSTEM"
            message = f"Ahsante  {username} kwa kuweka oda ya bidhaa kutoka kwetu, wasiliana nasi kupitia Email: {to_dimoso_email} au Kwa namba ya simu 0628431507"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            #ZINAISHIA HAPA ZA KUTUMA EMAIL
            messages.success(request, f"Email sent Successfully to {to_dimoso_email}")
            return redirect('home')
        

    context = {
            'form': form,
            #'order': order,
            
        }
    return render(request, "MyProducts/contact_me_if_not_registered.html",context)

def extra_email_template(request):
    order = Order.objects.get(user=request.user, ordered=False)
    context = {
            'form': form,
            'order': order,
            
        }
    return render(request, "MyProducts/extra_email_template.html",context)