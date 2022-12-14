from django.shortcuts import render,get_object_or_404,redirect

from vendor.models import Vendor,OpeningHour
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse,JsonResponse
from .models import Cart
from .context_processors import get_cart_counter,get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date,datetime
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from orders.forms import OrderForm
from accounts.models import UserProfile


# Create your views here.


def marketplace(request):
  vendors =Vendor.objects.filter(is_approved=True,user__is_active=True)
  vendor_count=vendors.count()
  
  context ={
    'vendors':vendors,
    'vendor_count':vendor_count
  }
  return render(request,'marketplace/listing.html',context)

def vendor_detail(request,vendor_slug):
  vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
  categories = Category.objects.filter(vendor=vendor).prefetch_related(
    Prefetch(
      'fooditems',
      queryset=FoodItem.objects.filter(is_available=True)
    )
  )
  opening_hours=OpeningHour.objects.filter(vendor=vendor).order_by('day','-from_hour')


  today_date =date.today()
  today =today_date.isoweekday()
  current_day = OpeningHour.objects.filter(vendor=vendor,day=today)
  
  if request.user.is_authenticated:
    cart_items = Cart.objects.filter(user = request.user)
  else:
    cart_items=None

  context ={
    'vendor':vendor,
    'categories':categories,
    'cart_items':cart_items,
    'opening_hours':opening_hours,
    'current_day':current_day
  }

  return render(request,'marketplace/vendor_detail.html',context)


def add_to_cart(request, food_id):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') =='XMLHttpRequest':
      try:
       
        fooditem =FoodItem.objects.get(id=food_id)
       
        try:
          chkCart =Cart.objects.get(user=request.user,fooditem=fooditem)
          
          chkCart.quantity +=1
          chkCart.save()
          return JsonResponse({'status':'Success','message':'Increased the cart quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
        except:
          
          chkCart = Cart.objects.create(user = request.user, fooditem=fooditem,quantity=1)
          return JsonResponse({'status':'Success','message':'Food item added to cart','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
      except:
        return JsonResponse({'status':'Failed','message':'Food item does not exist.'})
    else:
      return JsonResponse({'status':'Failed','message':'Invalid request.'})
  else:
    return JsonResponse({'status':'login_required','message':'Please login to continue.'})

def decrease_cart(request,food_id):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') =='XMLHttpRequest':
      try:
       
        fooditem =FoodItem.objects.get(id=food_id)
       
        try:
          chkCart =Cart.objects.get(user=request.user,fooditem=fooditem)
          if chkCart.quantity > 1:
            chkCart.quantity -= 1
            chkCart.save()
          elif chkCart.quantity == 1:
            chkCart.delete()
            chkCart.quantity =0
          else:
            chkCart.delete()
            chkCart.quantity =0
          return JsonResponse({'status':'Success','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
        except:
          return JsonResponse({'status':'Failed','message':"You don't have this item in your cart!"})
      except:
        return JsonResponse({'status':'Failed','message':'Food item does not exist.'})
    else:
      return JsonResponse({'status':'Failed','message':'Invalid request.'})
  else:
    return JsonResponse({'status':'login_required','message':'Please login to continue.'})


@login_required(login_url='login')
def cart(request):
  cart_items =Cart.objects.filter(user =request.user).order_by('-created_at')
  context ={
    'cart_items':cart_items
  }
  return render(request,'marketplace/cart.html',context)

def delete_cart(request, cart_id):
  if request.user.is_authenticated:
    if request.headers.get('x-requested-with') =='XMLHttpRequest':
      try:
        cart_item =Cart.objects.get(user =request.user, id=cart_id)
        if cart_item:
          cart_item.delete()
          return JsonResponse({'status':'Success','message':'Cart item deleted!','cart_counter':get_cart_counter(request),'cart_amount':get_cart_amounts(request)})
      except:
        return JsonResponse({'status':'Failed','message':'Cart item does not exist.'})
    else:
      return JsonResponse({'status':'Failed','message':'Invalid request.'})
  return render

def search(request):
  if not 'address' in request.GET:
    return redirect('marketplace')
  address =request.GET.get('address',None)
  latitude =request.GET.get('lat',None)
  longitude =request.GET.get('lng',None)
  radius =request.GET.get('radius',None)
  keyword =request.GET.get('keyword',None)

  fetch_vendors_by_fooditems=FoodItem.objects.filter(food_title__icontains=keyword,is_available=True).values_list('vendor',flat=True)
  vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword,is_approved=True,user__is_active=True))
  vendor_count =vendors.count()
  if latitude and longitude and radius:
    pnt = GEOSGeometry('POINT(%s %s)' %(longitude,latitude))
    vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword,is_approved=True,user__is_active=True),
    user_profile__location__distance_lte=(pnt, D(km=radius))).annotate(distance=Distance('user_profile__location',pnt)).order_by('distance')

    for v in vendors:
      v.kms =round(v.distance.km,1)
  context ={
    'vendors':vendors,
    'vendor_count':vendor_count,
    'source_location':address
  }

  return render(request,'marketplace/listing.html',context)


@login_required(login_url='login')
def checkout(request):
  cart_items = Cart.objects.filter(user= request.user).order_by('created_at')
  cart_count = cart_items.count()
  if cart_count <= 0:
    return redirect('marketplace')
     
  user_profile = UserProfile.objects.get(user = request.user)
  default_values = {
    'first_name':request.user.first_name,
    'last_name':request.user.last_name,
    'phone':request.user.phone_number,
    'email':request.user.email,
    'address':user_profile.address,
    'country':user_profile.country,
    'state':user_profile.state,
    'city':user_profile.city,
    'pin_code':user_profile.pin_code,
  }

  form = OrderForm(initial=default_values)

  context ={
    'form':form,
    'cart_items':cart_items
  }
  return render(request,'marketplace/checkout.html',context)