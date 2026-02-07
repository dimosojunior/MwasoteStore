from django.db.models.query import QuerySet
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.db.models import Q
import datetime
from django.utils import timezone
from django.views.generic.base import TemplateView
#from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
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
from django.db.models import Sum, Max, Min, Avg

def options(request):
    
    return render(request,'Account/options.html')

def maduka_yote(request):
    maduka = MadukaYote.objects.all()
    contexts = {
        "maduka":maduka,
    }

    
    return render(request,'Account/maduka_yote.html', contexts)


# Create your views here.
def user_login(request):
    context={}
    if request.POST:
        form=UserLoginForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user = authenticate(request, email=email,password=password)

            if user is not None:
                login(request,user)
                return redirect('options')
            messages.success(request, "password or email is incorrect")
        else:
            context['login_form']=form
            
    else:
        #messages.success(request, "password or username is incorrect")
        form=UserLoginForm(request.POST)
        context['login_form']=form    
        
    return render(request,'Account/user_login.html', context)


def user_logout(request):
    logout(request)
    return redirect('user_login')
    return render(request,'Account/logout.html')



def registration(request):
    context = {}

    if request.method == "POST":
        form = MyUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # BOOLEAN FIELDS
            user.is_staff = form.cleaned_data.get("is_staff")
            user.is_superuser = form.cleaned_data.get("is_superuser")

            user.save()

            # SEND EMAIL
            subject = "Welcome to Mwasote Pembejeo Za Kilimo"
            message = f"""
                Hello {user.username},

                Your account has been successfully created.

                Shop: {user.ShopName}
                Email: {user.email}

                Regards,
                Mwasote Pembejeo Team
            """
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=True
            )

            # AUTO LOGIN
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)

            return redirect("users_list")

        else:
            context["registration_form"] = form

    else:
        context["registration_form"] = MyUserForm()

    return render(request, "Account/registration.html", context)




def users_list(request):
    users = MyUser.objects.all()
    return render(request, "Account/users_list.html", {"users": users})
