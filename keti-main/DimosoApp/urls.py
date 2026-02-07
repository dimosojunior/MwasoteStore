
from django.urls import path
from . import views

urlpatterns = [
    
    
    path('dashboard/', views.dashboard, name="dashboard"),
    path('about-system/', views.about_system, name='about_system'),
    path('stock/', views.stock, name="stock"),
    path('add_items/', views.add_items.as_view(), name="add_items"),
    path('update_items/<str:pk>/', views.update_items.as_view(), name="update_items"),
    path('delete_items/<int:id>/', views.delete_items, name="delete_items"),
    path('stock_detailpage/<int:id>/', views.stock_detailpage, name="stock_detailpage"),
    path('issue_items/<int:id>/', views.issue_items, name="issue_items"),
    path('receive_items/<int:id>/', views.receive_items, name="receive_items"),
    path('reorder_level/<int:id>/', views.reorder_level, name="reorder_level"),
    path('ending_products/', views.ending_products, name="ending_products"),

    path('received_items_history/', views.received_items_history, name="received_items_history"),
    path('receive_amount/<int:id>/', views.receive_amount, name="receive_amount"),
    path('issued_amount/<int:id>/', views.issued_amount, name="issued_amount"),

    path('issued_items_history/', views.issued_items_history, name="issued_items_history"),
    path('point_of_sales/', views.point_of_sales, name="point_of_sales"),

    path('manunuzi_maduka/', views.manunuzi_maduka, name="manunuzi_maduka"),
    path('manunuzi/<str:shop_name>/', views.manunuzi_ya_duka, name='manunuzi_ya_duka'),

    path('mauzo_maduka/', views.mauzo_maduka, name="mauzo_maduka"),
    path('mauzo/<str:shop_name>/', views.mauzo_ya_duka, name='mauzo_ya_duka'),

    path('reports/', views.reports_dashboard, name='reports'),
    path('pos/', views.pos_view, name='pos'),
    path('reports_maduka/', views.reports_maduka, name="reports_maduka"),



    

    path(
        'manunuzi/<str:shop_name>/export-excel/',
        views.export_manunuzi_excel,
        name='export_manunuzi_excel'
    ),

    

    path(
        'mauzo/<str:shop_name>/export-excel/',
        views.export_mauzo_excel,
        name='export_mauzo_excel'
    ),

    # ===============================
    # CHARTS
    # ===============================
    path(
        'mauzo/<str:shop_name>/charts/',
        views.mauzo_charts,
        name='mauzo_charts'
    ),

    # ===============================
    # PROFIT
    # ===============================
    path(
        'profit/<str:shop_name>/',
        views.profit_ya_duka,
        name='profit_ya_duka'
    ),

    # ===============================
    # POS RECEIPT
    # ===============================
    path(
        'receipt/<int:sale_id>/',
        views.pos_receipt,
        name='pos_receipt'
    ),


    path('product-history/', views.product_history, name='product_history'),
    






    path('issued_items_history_1/', views.issued_items_history_1, name="issued_items_history_1"),
    path('issued_items_history_2/', views.issued_items_history_2, name="issued_items_history_2"),
    path('issued_items_history_3/', views.issued_items_history_3, name="issued_items_history_3"),
    path('issued_items_history_4/', views.issued_items_history_4, name="issued_items_history_4"),
    path('issued_items_history_5/', views.issued_items_history_5, name="issued_items_history_5"),
    path('issued_items_history_6/', views.issued_items_history_6, name="issued_items_history_6"),
    path('issued_items_history_7/', views.issued_items_history_7, name="issued_items_history_7"),
    path('issued_items_history_8/', views.issued_items_history_8, name="issued_items_history_8"),
    path('issued_items_history_9/', views.issued_items_history_9, name="issued_items_history_9"),
    path('issued_items_history_10/', views.issued_items_history_10, name="issued_items_history_10"),
    path('issued_items_history_11/', views.issued_items_history_11, name="issued_items_history_11"),
    path('issued_items_history_12/', views.issued_items_history_12, name="issued_items_history_12"),
    path('issued_items_history_today/', views.issued_items_history_today, name="issued_items_history_today"),



    path('received_items_history_1/', views.received_items_history_1, name="received_items_history_1"),
    path('received_items_history_2/', views.received_items_history_2, name="received_items_history_2"),
    path('received_items_history_3/', views.received_items_history_3, name="received_items_history_3"),
    path('received_items_history_4/', views.received_items_history_4, name="received_items_history_4"),
    path('received_items_history_5/', views.received_items_history_5, name="received_items_history_5"),
    path('received_items_history_6/', views.received_items_history_6, name="received_items_history_6"),
    path('received_items_history_7/', views.received_items_history_7, name="received_items_history_7"),
    path('received_items_history_8/', views.received_items_history_8, name="received_items_history_8"),
    path('received_items_history_9/', views.received_items_history_9, name="received_items_history_9"),
    path('received_items_history_10/', views.received_items_history_10, name="received_items_history_10"),
    path('received_items_history_11/', views.received_items_history_11, name="received_items_history_11"),
    path('received_items_history_12/', views.received_items_history_12, name="received_items_history_12"),
    path('received_items_history_today/', views.received_items_history_today, name="received_items_history_today"),





    path('point_of_sales_1/', views.point_of_sales_1, name="point_of_sales_1"),
    path('point_of_sales_2/', views.point_of_sales_2, name="point_of_sales_2"),
    path('point_of_sales_3/', views.point_of_sales_3, name="point_of_sales_3"),
    path('point_of_sales_4/', views.point_of_sales_4, name="point_of_sales_4"),
    path('point_of_sales_5/', views.point_of_sales_5, name="point_of_sales_5"),
    path('point_of_sales_6/', views.point_of_sales_6, name="point_of_sales_6"),
    path('point_of_sales_7/', views.point_of_sales_7, name="point_of_sales_7"),
    path('point_of_sales_8/', views.point_of_sales_8, name="point_of_sales_8"),
    path('point_of_sales_9/', views.point_of_sales_9, name="point_of_sales_9"),
    path('point_of_sales_10/', views.point_of_sales_10, name="point_of_sales_10"),
    path('point_of_sales_11/', views.point_of_sales_11, name="point_of_sales_11"),
    path('point_of_sales_12/', views.point_of_sales_12, name="point_of_sales_12"),
    path('point_of_sales_today/', views.point_of_sales_today, name="point_of_sales_today"),




]