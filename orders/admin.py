from django.contrib import admin

# Register your models here.
from .models import Order,OrderedFood,Payment


class OrderFoodAdmin(admin.TabularInline):
  model= OrderedFood
  readonly_fields =['order','payment','user','fooditem','quantity','price','amount']
  extra=0

class OrderAdmin(admin.ModelAdmin):
  list_display=['order_number','name','phone','email','status','order_plased_to']
  inlines=[OrderFoodAdmin]

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedFood)
