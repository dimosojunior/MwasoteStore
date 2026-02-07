from django.db.models.query import QuerySet
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView

from django.contrib.auth import login, authenticate
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

import openpyxl
from django.http import HttpResponse
# add_items

# Create your views here.

def dashboard(request):
	return render(request, "DashBoard/index.html")


def about_system(request):
    return render(request, 'DimosoApp/about_system.html')


def stock(request):
    form = StockSearchForm(request.POST or None)
    x = datetime.now()
    current_date = x.strftime('%d-%m-%Y %H:%M')

    # ====== CHUKUA DUKA LILILOCHAGULIWA ======
    shop_id = request.GET.get('shop')
    shop = MadukaYote.objects.get(id=shop_id)


    # ====== BASE QUERYSET (LAZIMA LIWE LA DUKA TU) ======
    if shop_id:
        queryset = Stock.objects.filter(ShopName_id=shop_id).order_by('-id')
    else:
        queryset = Stock.objects.all().order_by('-id')

    # ====== PAGINATION ======
    paginator = Paginator(queryset, 5)
    page = request.GET.get('page')

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    # ====== SEARCH & FILTER ======
    if request.method == 'POST':
        item_name = form['item_name'].value()
        category = form['category'].value()

        queryset = Stock.objects.all()

        # filter kwa duka kwanza
        if shop_id:
            queryset = queryset.filter(ShopName_id=shop_id)

        if item_name:
            queryset = queryset.filter(item_name__icontains=item_name)

        if category:
            queryset = queryset.filter(category_id=category)

        # ====== CSV EXPORT ======
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List_of_Items.csv"'
            writer = csv.writer(response)
            writer.writerow(['DUKA', 'CATEGORY', 'ITEM NAME', 'QUANTITY'])

            for stock in queryset:
                writer.writerow([
                    stock.ShopName,
                    stock.category,
                    stock.item_name,
                    stock.quantity
                ])
            return response

        # ====== PAGINATION BAADA YA FILTER ======
        paginator = Paginator(queryset, 5)
        page = request.GET.get('page')

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page": page,
        "current_date": current_date,
        "shop_id": shop_id,
        "shop": shop,

    }

    return render(request, 'DimosoApp/stock.html', context)


class add_items(SuccessMessageMixin, CreateView):
	model = Stock
	template_name = 'DimosoApp/add_items.html'
	form_class = StockCreateForm
	success_url = reverse_lazy('add_items')
	success_message = "Item added successfully in your stock"
class update_items(SuccessMessageMixin, UpdateView):
	model = Stock
	template_name = 'DimosoApp/update_stock.html'
	form_class = StockUpdateForm
	success_url = reverse_lazy('update_stock')
	success_message = "Item updated successfully in your stock"

def delete_items(request, id):
    queryset = get_object_or_404(Stock, id=id)

    # chukua shop_id kabla ya kufuta
    shop_id = queryset.ShopName.id if queryset.ShopName else None

    if request.method == 'POST':
        queryset.delete()
        messages.success(request, "Item deleted successfully from your stock")

        # rudisha user kwenye stock page ya duka husika
        if shop_id:
            return redirect(f'/stock/?shop={shop_id}')
        else:
            return redirect('stock')

    context = {
        "queryset": queryset
    }

    return render(request, 'DimosoApp/delete_items.html', context)

# def delete_items(request, id):
# 	queryset = Stock.objects.get(id=id)
# 	x= datetime.now()
# 	current_date = x.strftime('%d-%m-%Y %H:%M')
	
# 	if request.method == 'POST':
# 		queryset.delete()
# 		messages.success(request,"Item deleted successfully from your stock")
# 		return redirect('stock',id=id)
		

	# return render(request, 'DimosoApp/delete_items.html', {"current_date":current_date})

def stock_detailpage(request, id):
	queryset = Stock.objects.get(id=id)
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')
	context ={
		"current_date":current_date,
		"queryset":queryset
	}
	
	
		

	return render(request, 'DimosoApp/stock_detailpage.html',context)

# def issue_items(request, id):
# 	queryset = Stock.objects.get(id=id)
# 	x= datetime.now()
# 	current_date = x.strftime('%d-%m-%Y %H:%M')
# 	form= IssueForm(request.POST or None, instance=queryset)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.quantity -= instance.issue_quantity
# 		instance.sales_amount += instance.receive_amount
# 		#instance.issue_by = str(request.user)
# 		messages.success(request,"Items Issued successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in store")
# 		instance.save()
# 		#return redirect('stock_detailpage/'+str(instance.id))
# 		return redirect('stock_detailpage',id=id)
# 		#return HttpResponseRedirect(instance.get_absolute_url())
# 	context ={
# 		"instance":queryset,
# 		"current_date":current_date,
# 		"form":form,
# 		#"username": 'Issued By: ' + str(request.user),
# 		"title": 'Issue ' + str(queryset.item_name),
# 	}
	
	
		

# 	return render(request, 'DimosoApp/issue_items.html',context)








from django.db.models import Sum
from django.shortcuts import render
from .models import MadukaYote, ManunuziYote, MauzoYote, Stock

def reports_dashboard(request):
    shop_id = request.GET.get('shop')

    shops = MadukaYote.objects.all()

    manunuzi = ManunuziYote.objects.all()
    mauzo = MauzoYote.objects.all()
    stock = Stock.objects.all()

    if shop_id:
        manunuzi = manunuzi.filter(ShopName=MadukaYote.objects.get(id=shop_id).ShopName)
        mauzo = mauzo.filter(ShopName=MadukaYote.objects.get(id=shop_id).ShopName)
        stock = stock.filter(ShopName_id=shop_id)

    total_manunuzi = manunuzi.aggregate(total=Sum('HelaUliyotoa'))['total'] or 0
    total_mauzo = mauzo.aggregate(total=Sum('HelaUliyopokea'))['total'] or 0
    total_stock_qty = stock.aggregate(total=Sum('quantity'))['total'] or 0

    faida = total_mauzo - total_manunuzi

    context = {
        'shops': shops,
        'manunuzi': manunuzi,
        'mauzo': mauzo,
        'total_manunuzi': total_manunuzi,
        'total_mauzo': total_mauzo,
        'faida': faida,
        'total_stock_qty': total_stock_qty,
        'shop_id': shop_id
    }
    return render(request, 'DimosoApp/reports.html', context)



from django.shortcuts import render, redirect
from django.contrib import messages

def pos_view(request):
    shops = MadukaYote.objects.all()
    products = Stock.objects.filter(available=True)

    if request.method == 'POST':
        product_id = request.POST['product']
        quantity = int(request.POST['quantity'])
        shop_id = request.POST['shop']

        product = Stock.objects.get(id=product_id)

        if product.quantity < quantity:
            messages.error(request, "Stock haitoshi")
            return redirect('pos')

        total_price = quantity * product.price

        MauzoYote.objects.create(
            reg_no=product.reg_no,
            JinaLaBidhaa=product.item_name,
            ShopName=product.ShopName.ShopName,
            Category=product.category.name,
            KiasiChaBidhaaKilichotoka=quantity,
            HelaUliyopokea=total_price,
            ImeuzwaNa=request.user.username
        )

        product.quantity -= quantity
        product.save()

        messages.success(request, "Mauzo yamefanikiwa")
        return redirect('pos')

    return render(request, 'DimosoApp/pos.html', {
        'shops': shops,
        'products': products
    })




def reports_maduka(request):
	maduka = MadukaYote.objects.all()
	return render(request, 'DimosoApp/reports_maduka.html', {"maduka": maduka})














from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import Stock, ManunuziYote
from .forms import IssueForm


def issue_items(request, id):
    queryset = Stock.objects.get(id=id)
    x = datetime.now()
    current_date = x.strftime('%d-%m-%Y %H:%M')

    form = IssueForm(request.POST or None, instance=queryset)

    if form.is_valid():
        instance = form.save(commit=False)

        # ===== UPDATE STOCK =====
        instance.quantity -= instance.issue_quantity
        instance.sales_amount += instance.receive_amount
        instance.is_issued = True
        instance.save()

        # ===== SAVE TO Mazuo YOTE =====
        MauzoYote.objects.create(
            reg_no=instance.reg_no,
            JinaLaBidhaa=instance.item_name,
            ShopName=str(instance.ShopName),
            Category=str(instance.category),
            HelaUliyopokea=instance.receive_amount,
            KiasiChaBidhaaKilichotoka=instance.issue_quantity,
            ImeuzwaNa=str(request.user),
        )

        messages.success(
            request,
            f"Items Issued Successfully. {instance.quantity} {instance.item_name} left in stock"
        )

        return redirect('stock_detailpage', id=id)

    context = {
        "instance": queryset,
        "current_date": current_date,
        "form": form,
        "title": 'Issue ' + str(queryset.item_name),
    }

    return render(request, 'DimosoApp/issue_items.html', context)






def manunuzi_maduka(request):
	maduka = MadukaYote.objects.all()
	return render(request, 'DimosoApp/manunuzi_maduka.html', {"maduka": maduka})

def mauzo_maduka(request):
	maduka = MadukaYote.objects.all()
	return render(request, 'DimosoApp/mauzo_maduka.html', {"maduka": maduka})

from django.utils.timezone import now
from django.db.models import Sum
from .models import ManunuziYote


def manunuzi_ya_duka(request, shop_name):
    today = now().date()

    # ===== DEFAULT: MAUZO YA LEO =====
    manunuzi = ManunuziYote.objects.filter(
        ShopName=shop_name,
        Created__date=today
    ).order_by('-Created')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # ===== FILTER BY DATE =====
    if start_date and end_date:
        manunuzi = ManunuziYote.objects.filter(
            ShopName=shop_name,
            Created__date__range=[start_date, end_date]
        ).order_by('-Created')

    elif start_date:
        manunuzi = ManunuziYote.objects.filter(
            ShopName=shop_name,
            Created__date=start_date
        ).order_by('-Created')

    # ===== CALCULATE TOTALS (IMPORTANT PART) =====
    total_amount = manunuzi.aggregate(
        total=Sum('HelaUliyotoa')
    )['total'] or 0

    total_items = manunuzi.aggregate(
        total=Sum('KiasiChaBidhaaUlichonunua')
    )['total'] or 0

    context = {
        "manunuzi": manunuzi,
        "shop_name": shop_name,
        "today": today,
        "total_amount": total_amount,
        "total_items": total_items,
    }

    return render(request, 'DimosoApp/manunuzi_ya_duka.html', context)





def mauzo_ya_duka(request, shop_name):
    today = now().date()

    # ===== DEFAULT: MAUZO YA LEO =====
    manunuzi = MauzoYote.objects.filter(
        ShopName=shop_name,
        Created__date=today
    ).order_by('-Created')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # ===== FILTER BY DATE =====
    if start_date and end_date:
        manunuzi = MauzoYote.objects.filter(
            ShopName=shop_name,
            Created__date__range=[start_date, end_date]
        ).order_by('-Created')

    elif start_date:
        manunuzi = MauzoYote.objects.filter(
            ShopName=shop_name,
            Created__date=start_date
        ).order_by('-Created')

    # ===== CALCULATE TOTALS (IMPORTANT PART) =====
    total_amount = manunuzi.aggregate(
        total=Sum('HelaUliyopokea')
    )['total'] or 0

    total_items = manunuzi.aggregate(
        total=Sum('KiasiChaBidhaaKilichotoka')
    )['total'] or 0

    context = {
        "manunuzi": manunuzi,
        "shop_name": shop_name,
        "today": today,
        "total_amount": total_amount,
        "total_items": total_items,
    }

    return render(request, 'DimosoApp/mauzo_ya_duka.html', context)



def receive_items(request, id):
	queryset = Stock.objects.get(id=id)
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	form= ReceiveForm(request.POST or None, instance=queryset)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity += instance.receive_quantity
		instance.purchasing_amount += instance.issued_amount
		#instance.issue_by = str(request.user)
		#messages.success(request,"Items Issued successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in store")
		instance.save()

		# ===== SAVE TO Mazuo YOTE =====
		ManunuziYote.objects.create(
			reg_no=instance.reg_no,
			JinaLaBidhaa=instance.item_name,
			ShopName=str(instance.ShopName),
			Category=str(instance.category),
			HelaUliyotoa=instance.issued_amount,
			KiasiChaBidhaaUlichonunua=instance.receive_quantity,
			ImenunuliwaNa=str(request.user),
		)





		messages.success(request, "Received successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s in Your Store")
		#return redirect('stock_detailpage/'+str(instance.id))
		return redirect('stock_detailpage',id=id)
		#return HttpResponseRedirect(instance.get_absolute_url())
	context ={
		"instance":queryset,
		"form":form,
		"current_date":current_date,
		#"username": 'Issued By: ' + str(request.user),
		"title": 'Receive ' + str(queryset.item_name),
	}
	
	
		

	return render(request, 'DimosoApp/receive_items.html',context)









#############################################################################################


def export_mauzo_excel(request, shop_name):
    mauzo = MauzoYote.objects.filter(ShopName=shop_name)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Mauzo"

    ws.append([
        "Bidhaa", "Category", "Kiasi", "Hela", "Imeuzwa Na", "Tarehe"
    ])

    for m in mauzo:
        ws.append([
            m.JinaLaBidhaa,
            m.Category,
            m.KiasiChaBidhaaKilichotoka,
            m.HelaUliyopokea,
            m.ImeuzwaNa,
            m.Created.strftime("%d-%m-%Y %H:%M")
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=Mauzo_{shop_name}.xlsx'
    wb.save(response)
    return response



def export_manunuzi_excel(request, shop_name):
    manunuzi = ManunuziYote.objects.filter(ShopName=shop_name)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Manunuzi"

    ws.append([
        "Bidhaa", "Category", "Kiasi", "Hela", "Imenunuliwa Na", "Tarehe"
    ])

    for m in manunuzi:
        ws.append([
            m.JinaLaBidhaa,
            m.Category,
            m.KiasiChaBidhaaUlichonunua,
            m.HelaUliyotoa,
            m.ImenunuliwaNa,
            m.Created.strftime("%d-%m-%Y %H:%M")
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=Manunuzi_{shop_name}.xlsx'
    wb.save(response)
    return response







from django.db.models.functions import TruncDay, TruncMonth

def mauzo_charts(request, shop_name):
    daily = (
        MauzoYote.objects
        .filter(ShopName=shop_name)
        .annotate(day=TruncDay('Created'))
        .values('day')
        .annotate(total=Sum('HelaUliyopokea'))
        .order_by('day')
    )

    monthly = (
        MauzoYote.objects
        .filter(ShopName=shop_name)
        .annotate(month=TruncMonth('Created'))
        .values('month')
        .annotate(total=Sum('HelaUliyopokea'))
        .order_by('month')
    )

    return render(request, 'DimosoApp/mauzo_charts.html', {
        "daily": daily,
        "monthly": monthly,
        "shop_name": shop_name
    })







from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import now
from .models import MauzoYote, ManunuziYote


def profit_ya_duka(request, shop_name):
    today = now()
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    # ===== DEFAULT: CURRENT MONTH =====
    month = int(selected_month) if selected_month else today.month
    year = int(selected_year) if selected_year else today.year

    sales = MauzoYote.objects.filter(
        ShopName=shop_name,
        Created__year=year,
        Created__month=month
    ).aggregate(total=Sum('HelaUliyopokea'))['total'] or 0

    purchases = ManunuziYote.objects.filter(
        ShopName=shop_name,
        Created__year=year,
        Created__month=month
    ).aggregate(total=Sum('HelaUliyotoa'))['total'] or 0

    profit = sales - purchases

    context = {
        "shop_name": shop_name,
        "sales": sales,
        "purchases": purchases,
        "profit": profit,
        "month": month,
        "year": year,
    }

    return render(request, 'DimosoApp/profit.html', context)



def pos_receipt(request, sale_id):
    sale = MauzoYote.objects.get(id=sale_id)
    return render(request, 'DimosoApp/pos_receipt.html', {"sale": sale})








from django.db.models import Q
from .models import MauzoYote, ManunuziYote, Stock


def product_history(request):
    reg_no = request.GET.get('reg_no', None)  # filter by reg_no if provided
    products = Stock.objects.all()

    selected_product = None
    mauzo = []
    manunuzi = []

    if reg_no:
        try:
            selected_product = Stock.objects.get(reg_no=reg_no)
        except Stock.DoesNotExist:
            selected_product = None

        if selected_product:
            mauzo = MauzoYote.objects.filter(reg_no=reg_no).order_by('-Created')
            manunuzi = ManunuziYote.objects.filter(reg_no=reg_no).order_by('-Created')

    return render(request, 'DimosoApp/product_history.html', {
        "products": products,
        "selected_product": selected_product,
        "mauzo": mauzo,
        "manunuzi": manunuzi,
        "reg_no": reg_no,
    })










def reorder_level(request, id):
	queryset = Stock.objects.get(id=id)
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')
	form= ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level of " + str(instance.item_name) + "is updated to " + str(instance.reorder_level))
		#return redirect('stock_detailpage/'+str(instance.id))
		return redirect('stock')
		#return HttpResponseRedirect(instance.get_absolute_url())
	context ={
		"instance":queryset,
		"form":form,
		"current_date":current_date
		
	}
	
	
		

	return render(request, 'DimosoApp/reorder_level.html',context)

def ending_products(request):
	form = StockSearchForm(request.POST or None)
	formu = ReorderLevelForm(request.POST or None)
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')
	

	queryset = Stock.objects.filter(quantity__lt = formu['reorder_level'].value()).order_by('-id')
	context ={
		"queryset":queryset,
		"form":form,
		"formu":formu,
		"current_date":current_date
	}

		

	return render(request, 'DimosoApp/ending_products.html',context)


def received_items_history(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)

	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')
	

	queryset = Stock.objects.filter(
		
		Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
		is_received=True
		).order_by('-id')

	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)

	get_sum = Stock.objects.filter(is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "DimosoApp/received_items_history.html",context)



def received_items_history_1(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =1) | Q(last_updated__month =1),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_received=True 
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1),is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_1.html",context)

def received_items_history_2(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =2) | Q(last_updated__month =2),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_received=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2),is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_2.html",context)


def received_items_history_3(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =3) | Q(last_updated__month =3),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_received=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3),is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_3.html",context)

def received_items_history_4(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =4) | Q(last_updated__month =4),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_received=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4),is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_4.html",context)

def received_items_history_5(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =5) | Q(last_updated__month =5),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_received=True 
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5),is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_5.html",context)


def received_items_history_6(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')
	

	queryset = Stock.objects.filter(
			Q(last_updated__month =6) | Q(timestamp__month =6),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_received=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6),is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_6.html",context)

def received_items_history_7(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =7) | Q(last_updated__month =7),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_received=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7),is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_7.html",context)


def received_items_history_8(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =8) | Q(last_updated__month =8),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_received=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8),is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_8.html",context)


def received_items_history_9(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =9) | Q(last_updated__month =9),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_received=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9),is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_9.html",context)




def received_items_history_10(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =10) | Q(last_updated__month =10),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_received=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10),is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_10.html",context)

def received_items_history_11(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =11) | Q(last_updated__month =11),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_received=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11),is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_11.html",context)


def received_items_history_12(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =12) | Q(last_updated__month =12),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_received=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12),is_received=True).aggregate(avg=Avg('purchasing_amount'))
	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,
		"current_month":current_month,
		"current_year":current_year,
	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_12.html",context)




def received_items_history_today(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	x= timezone.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%Y-%m-%d')

	queryset = Stock.objects.filter(
			#Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			#last_updated__month =5,

			last_updated__date = current_date,
			 is_received=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(last_updated__date = current_date, is_received=True).aggregate(sum=Sum('issued_amount'))
	get_max = Stock.objects.filter(last_updated__date = current_date, is_received=True).aggregate(max=Max('issued_amount'))
	get_min = Stock.objects.filter(last_updated__date = current_date, is_received=True).aggregate(min=Min('issued_amount'))
	get_avg = Stock.objects.filter(last_updated__date = current_date, is_received=True).aggregate(avg=Avg('issued_amount'))


	context ={
		"x":x,
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,
		

	}
	return render(request, "RECEIVED_ITEMS_MONTHS/received_items_history_today.html",context)




























def issued_items_history(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')
	


	

	queryset = Stock.objects.filter(
		Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
		is_issued=True

		).order_by('-id')

	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)

	get_sum = Stock.objects.filter(is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		

	}
	return render(request, "DimosoApp/issued_items_history.html",context)












def issued_items_history_1(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =1) | Q(last_updated__month =1),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_issued=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	 

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1), is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1), is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1), is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1), is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_1.html",context)

def issued_items_history_2(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =2) | Q(last_updated__month =2),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_issued=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2), is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2), is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2), is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2), is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_2.html",context)

def issued_items_history_3(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =3) | Q(last_updated__month =3),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_issued=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3), is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3), is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3), is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3), is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_3.html",context)

def issued_items_history_4(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =4) | Q(last_updated__month =4),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_issued=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4), is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4), is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4), is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4), is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_4.html",context)

def issued_items_history_5(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =5) | Q(last_updated__month =5),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_issued=True
			
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5), is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5), is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5), is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5), is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_5.html",context)


def issued_items_history_6(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =6) | Q(last_updated__month =6),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_issued=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6), is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6), is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6), is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6), is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_6.html",context)

def issued_items_history_7(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =7) | Q(last_updated__month =7),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_issued=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7), is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7), is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7), is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7), is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_7.html",context)

def issued_items_history_8(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =8) | Q(last_updated__month =8),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_issued=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8), is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8), is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8), is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8), is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_8.html",context)

def issued_items_history_9(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =9) | Q(last_updated__month =9),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_issued=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9), is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9), is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9), is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9), is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_9.html",context)


def issued_items_history_10(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =10) | Q(last_updated__month =10),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_issued=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10), is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10), is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10), is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10), is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_10.html",context)

def issued_items_history_11(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =11) | Q(last_updated__month =11),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_issued=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11), is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11), is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11), is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11), is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_11.html",context)


def issued_items_history_12(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =12) | Q(last_updated__month =12),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			is_issued=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12), is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12), is_issued=True).aggregate(max=Max('sales_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12), is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12), is_issued=True).aggregate(avg=Avg('sales_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"current_date":current_date,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_12.html",context)



def issued_items_history_today(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	

	x= datetime.now()
	current_date = x.strftime('%Y-%m-%d')

	queryset = Stock.objects.filter(
			#last_updated__year=current_year,
			#last_updated__month =5,
			last_updated__date = current_date,
			 is_issued=True
		)
	#To SET  PAGINATION IN STOCK LIST PAGE
	paginator = Paginator(queryset,5)
	page = request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)


	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(last_updated__date = current_date, is_issued=True).aggregate(sum=Sum('receive_amount'))
	get_max = Stock.objects.filter(last_updated__date = current_date, is_issued=True).aggregate(max=Max('receive_amount'))
	get_min = Stock.objects.filter(last_updated__date = current_date, is_issued=True).aggregate(min=Min('receive_amount'))
	get_avg = Stock.objects.filter(last_updated__date = current_date, is_issued=True).aggregate(avg=Avg('receive_amount'))


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,
		

	}
	return render(request, "ISSUED_ITEMS_MONTHS/issued_items_history_today.html",context)









def point_of_sales(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month

	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')
	

	queryset = Stock.objects.filter(
		Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
		is_issued=True,
		is_received=True

		).order_by('-id')

	get_sum = Stock.objects.filter(is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(is_issued=True).aggregate(avg=Avg('sales_amount'))

	profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		"profit":profit
	}
	return render(request, "DimosoApp/point_of_sales.html",context)









def point_of_sales_1(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =1) | Q(last_updated__month =1),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			
			
			is_received=True,
			is_issued=True
			#Q(timestamp__month = 1) and Q(is_received=True), is_issued=True
			#timestamp__date = current_date,
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1),is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1),is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1),is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1),is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(Q(timestamp__month =1) | Q(last_updated__month =1),is_issued=True).aggregate(avg=Avg('sales_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,
		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_1.html",context)


def point_of_sales_2(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =2) | Q(last_updated__month =2),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			is_received=True,
			is_issued=True
			#timestamp__date = current_date,
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2),is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2),is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2),is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2),is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(Q(timestamp__month =2) | Q(last_updated__month =2),is_issued=True).aggregate(avg=Avg('sales_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_2.html",context)

def point_of_sales_3(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =3) | Q(last_updated__month =3),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			is_received=True,
			is_issued=True
			#timestamp__date = current_date,
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3),is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3),is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3),is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3),is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(Q(timestamp__month =3) | Q(last_updated__month =3),is_issued=True).aggregate(avg=Avg('sales_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_3.html",context)

def point_of_sales_4(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =4) | Q(last_updated__month =4),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			is_received=True,
			is_issued=True
			#timestamp__date = current_date,
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4),is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4),is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4),is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4),is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(Q(timestamp__month =4) | Q(last_updated__month =4),is_issued=True).aggregate(avg=Avg('sales_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_4.html",context)

def point_of_sales_5(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =5) | Q(last_updated__month =5),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			is_received=True,
			is_issued=True
			#timestamp__date = current_date,
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5),is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5),is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5),is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5),is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(Q(timestamp__month =5) | Q(last_updated__month =5),is_issued=True).aggregate(avg=Avg('sales_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_5.html",context)




def point_of_sales_6(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =6) | Q(last_updated__month =6),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			is_received=True,
			is_issued=True
			#timestamp__date = current_date,
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6),is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6),is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6),is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6),is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(Q(timestamp__month =6) | Q(last_updated__month =6),is_issued=True).aggregate(avg=Avg('sales_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_6.html",context)


def point_of_sales_7(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =7) | Q(last_updated__month =7),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			is_received=True,
			is_issued=True
			#timestamp__date = current_date,
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7),is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7),is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7),is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7),is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(Q(timestamp__month =7) | Q(last_updated__month =7),is_issued=True).aggregate(avg=Avg('sales_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_7.html",context)


def point_of_sales_8(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =8) | Q(last_updated__month =8),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			is_received=True,
			is_issued=True
			#timestamp__date = current_date,
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8),is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8),is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8),is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8),is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(Q(timestamp__month =8) | Q(last_updated__month =8),is_issued=True).aggregate(avg=Avg('sales_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_8.html",context)

def point_of_sales_9(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =9) | Q(last_updated__month =9),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			is_received=True,
			is_issued=True
			#timestamp__date = current_date,
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9),is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9),is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9),is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9),is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(Q(timestamp__month =9) | Q(last_updated__month =9),is_issued=True).aggregate(avg=Avg('sales_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_9.html",context)

def point_of_sales_10(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =10) | Q(last_updated__month =10),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			is_received=True,
			is_issued=True
			#timestamp__date = current_date,
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10),is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10),is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10),is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10),is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(Q(timestamp__month =10) | Q(last_updated__month =10),is_issued=True).aggregate(avg=Avg('sales_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_10.html",context)

def point_of_sales_11(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =11) | Q(last_updated__month =11),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			is_received=True,
			is_issued=True
			#timestamp__date = current_date,
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11),is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11),is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11),is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11),is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(Q(timestamp__month =11) | Q(last_updated__month =11),is_issued=True).aggregate(avg=Avg('sales_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_11.html",context)



def point_of_sales_12(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	
	x= datetime.now()
	current_date = x.strftime('%d-%m-%Y %H:%M')

	queryset = Stock.objects.filter(
			Q(timestamp__month =12) | Q(last_updated__month =12),
			Q(timestamp__year =current_year) | Q(last_updated__year =current_year),
			is_received=True,
			is_issued=True
			#timestamp__date = current_date,
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12),is_received=True).aggregate(sum=Sum('purchasing_amount'))
	get_max = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12),is_received=True).aggregate(max=Max('purchasing_amount'))
	get_min = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12),is_received=True).aggregate(min=Min('purchasing_amount'))
	get_avg = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12),is_received=True).aggregate(avg=Avg('purchasing_amount'))


	get_sum2 = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12),is_issued=True).aggregate(sum=Sum('sales_amount'))
	get_max2 = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12),is_issued=True).aggregate(max=Max('sales_amount'))
	get_min2 = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12),is_issued=True).aggregate(min=Min('sales_amount'))
	get_avg2 = Stock.objects.filter(Q(timestamp__month =12) | Q(last_updated__month =12),is_issued=True).aggregate(avg=Avg('sales_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_12.html",context)


def point_of_sales_today(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	form = StockSearchForm(request.POST or None)
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	now = datetime.now()
	current_year = now.year
	current_month = now.month
	x= datetime.now()
	current_date = x.strftime('%Y-%m-%d')
	
	time = now.strftime('%I:%M %p')

	queryset = Stock.objects.filter(
			#last_updated__year=year,
			#timestamp__month =12,
			last_updated__date = current_date,
			 is_issued=True,
			  is_received=True
		)
	

	#queryset = Stock.objects.all().order_by('-id')

	get_sum = Stock.objects.filter(last_updated__date = current_date, is_received=True).aggregate(sum=Sum('issued_amount'))
	get_max = Stock.objects.filter(last_updated__date = current_date, is_received=True).aggregate(max=Max('issued_amount'))
	get_min = Stock.objects.filter(last_updated__date = current_date, is_received=True).aggregate(min=Min('issued_amount'))
	get_avg = Stock.objects.filter(last_updated__date = current_date, is_received=True).aggregate(avg=Avg('issued_amount'))


	get_sum2 = Stock.objects.filter(last_updated__date = current_date,is_issued=True).aggregate(sum=Sum('receive_amount'))
	get_max2 = Stock.objects.filter(last_updated__date = current_date,is_issued=True).aggregate(max=Max('receive_amount'))
	get_min2 = Stock.objects.filter(last_updated__date = current_date,is_issued=True).aggregate(min=Min('receive_amount'))
	get_avg2 = Stock.objects.filter(last_updated__date = current_date,is_issued=True).aggregate(avg=Avg('receive_amount'))

	#profit = 4-2


	context ={
		"queryset":queryset,
		"form":form,
		"get_sum":get_sum,
		"get_max":get_max,
		"get_min":get_min,
		"get_avg":get_avg,

		"get_sum2":get_sum2,
		"get_max2":get_max2,
		"get_min2":get_min2,
		"get_avg2":get_avg2,

		"current_month":current_month,
		"current_year":current_year,
		"current_date":current_date,

		#"profit":profit
	}
	return render(request, "POINT_OF_SALES_ALL_MONTHS/point_of_sales_today.html",context)

















def receive_amount(request, id):
	queryset = Stock.objects.get(id=id)

	form= ReceiveAmountForm(request.POST or None, instance=queryset)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.sales_amount += instance.receive_amount
		
		#instance.issue_by = str(request.user)
		#messages.success(request,"Items Issued successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in store")
		instance.save()
		messages.success(request, "Received successfully. " + str(instance.receive_amount) + "Tshs.")
		#return redirect('stock_detailpage/'+str(instance.id))
		return redirect('stock_detailpage',id=id)
		#return HttpResponseRedirect(instance.get_absolute_url())
	context ={
		"instance":queryset,
		"form":form,
		#"username": 'Issued By: ' + str(request.user),
		"title": 'Receive ' + str(queryset.item_name),
	}
	return render(request, 'DimosoApp/receive_amount.html',context)

def issued_amount(request, id):
	queryset = Stock.objects.get(id=id)

	form= IssuedAmountForm(request.POST or None, instance=queryset)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.purchasing_amount += instance.issued_amount
		
		#instance.issue_by = str(request.user)
		#messages.success(request,"Items Issued successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in store")
		instance.save()
		messages.success(request, "Issued successfully. " + str(instance.issued_amount) + "Tshs")
		#return redirect('stock_detailpage/'+str(instance.id))
		return redirect('stock_detailpage',id=id)
		#return HttpResponseRedirect(instance.get_absolute_url())
	context ={
		"instance":queryset,
		"form":form,
		#"username": 'Issued By: ' + str(request.user),
		"title": 'Receive ' + str(queryset.item_name),
	}
	return render(request, 'DimosoApp/issued_amount.html',context)