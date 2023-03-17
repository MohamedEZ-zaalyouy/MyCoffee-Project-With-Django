from django.contrib import admin
from .models import Order, OrderDetail, Payment
# Register your models here.


admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Payment)