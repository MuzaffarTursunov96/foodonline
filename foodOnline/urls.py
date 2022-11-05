

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
    path('marketplace/',include('marketplace.urls')),
    path('cart/',MarketplaceViews.cart,name='cart'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
