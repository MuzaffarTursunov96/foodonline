
from django.urls import path,re_path
from . import views 
from accounts.views import vendorDashboard
urlpatterns = [
  path('',vendorDashboard,name='vendor'),
   path('profile/',views.vprofile,name='vprofile')
]
