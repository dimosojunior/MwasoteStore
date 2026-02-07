"""DimosoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _


urlpatterns = [

    path(_('admin/'), admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    
    
]
admin.site.site_header= "KING STORE SYSTEM"
admin.site.site_title = "ADMIN AREA"
admin.site.index_title = "WELCOME TO ADMIN DASHBOARD"


urlpatterns += i18n_patterns (
    path('inventory/', include('MyProducts.urls')),
    path('stock/', include('DimosoApp.urls')),
    path('', include('Account.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    

)
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))


    ]

