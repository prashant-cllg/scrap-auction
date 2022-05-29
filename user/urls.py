from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import  static
from django.conf import settings
urlpatterns = [
    path('',views.userhome),
    path('funds/',views.funds),
    path('cancel/', views.cancel),
    path('payment/', views.payment),
    path('success/', views.success),
    path('cpuser/', views.cpuser),
    path('epuser/', views.epuser),
    path('viewbidproduct/', views.viewbidproduct),
    path('bid/', views.bid),
    path('transactions/', views.transactions),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
