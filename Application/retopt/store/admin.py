from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(ProductCategory)
# admin.site.register(ProductSubCategory)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAdress)
# admin.site.register(Transaction)
