

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as MarketplaceViews

from .views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name='home'),
    path('accounts/',include('accounts.urls')),
    path('vendor/', include('vendor.urls')),
    path('customer/', include('customers.urls')),
    path('marketplace/',include('marketplace.urls')),

    path('cart/',MarketplaceViews.cart,name='cart'),
    #Search
    path('search/',MarketplaceViews.search,name='search'),

    path('checkout/',MarketplaceViews.checkout,name='checkout'),
    
    path('orders/',include('orders.urls')),


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
