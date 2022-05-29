from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import  static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('contact/',views.contact),
    path('register/',views.register),
    path('checkEmail/', views.checkEmail),
    path('verify/',views.verify),
    path('login/',views.login),
    path('about/',views.about),
    path('responseurl/',views.responseurl),
    path('auction_process/',views.auction_process),
    path('myadmin/', include('myadmin.urls')),
    path('user/', include('user.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
