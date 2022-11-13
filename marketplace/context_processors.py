from .models import Cart,Tax

from menu.models import FoodItem



def get_cart_counter(request):
  cart_count=0
  if request.user.is_authenticated:
    try:
      cart_items = Cart.objects.filter(user=request.user)
      if cart_items:
        for cart_item in cart_items:
          cart_count += cart_item.quantity
      else:
        cart_count = 0
    except:
      cart_count=0
  context = {
      'cart_count': cart_count
  }
  return context


def get_cart_amounts(request):
  subtotal =0
  tax=0
  grant_total =0
  d='sscsscdcsdjkasbiyLIN?mC/NLKCNsdLcn'
  
  if request.user.is_authenticated:
    cart_items =Cart.objects.filter(user=request.user)
    for item in cart_items:
      fooditem =FoodItem.objects.get(pk=item.fooditem.id)
      subtotal +=(fooditem.price * item.quantity)
    
    get_tax = Tax.objects.filter(is_active=True)
    
    tax_dict={}
    for i in get_tax:
      tax_type = i.tax_type
      tax_percentage =i.tax_percentage
      tax_amount =round((tax_percentage * subtotal)/100 ,2)
      tax_dict.update({tax_type:{str(tax_percentage):tax_amount}})

    tax =sum(x for key in tax_dict.values() for x in key.values())
    grant_total =subtotal + tax
  
  context ={
    'subtotal':subtotal,
    'tax':tax,
    'grand_total':grant_total,
    'tax_dict':tax_dict
  }
  return context