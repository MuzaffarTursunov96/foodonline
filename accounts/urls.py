
from django.urls import path,re_path
from . import views 

urlpatterns = [
    path('registerUser',views.registerUser,name='registerUser'),
    path('registerVendor',views.registerVendor,name='registerVendor'),
]
