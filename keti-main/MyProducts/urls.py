
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name="home"),
    path('<int:category_id>/', views.home, name="product_by_category"),
    path('base/', views.base, name="base"),
    path('search_product/', views.search_product, name="search_product"),
    path('search_autoco_product', views.search_autoco_product, name="search_autoco_product"),

    path('product_details/<int:id>/', views.product_details, name="product_details"),
    path('add_to_cart/<int:id>/', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name="remove_from_cart"),
    path('order_summary', views.OrderSummaryView.as_view(), name="order_summary"),
    path('remove_single_from_cart/<int:id>/', views.remove_single_from_cart, name="remove_single_from_cart"),

    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', views.PaymentView.as_view(), name='payment'),
    path('add-coupon', views.CouponView.as_view(), name="add_coupon"),
    path('payment-complete', views.payment_complete, name="payment_complete"),
    path('payment_error_message', views.payment_error_message, name="payment_error_message"),

    path('contact_me/', views.contact_me, name="contact_me"),
    path('contact_me_if_not_registered/', views.contact_me_if_not_registered, name="contact_me_if_not_registered"),
    path('extra_email_template/', views.extra_email_template, name="extra_email_template"),

    
]