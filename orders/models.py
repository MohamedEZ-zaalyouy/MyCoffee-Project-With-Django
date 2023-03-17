from django.db import models
from django.contrib.auth.models import User 
from products.models import Product
from datetime import datetime
from creditcards.models import CardExpiryField, CardNumberField, SecurityCodeField

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.ManyToManyField(Product, through='OrderDetail')

    order_date = models.DateTimeField(default=datetime.now)  
    is_finished = models.BooleanField(default=False)

    total = 0
    items_count = 0

    def __str__(self):
        return 'User: '+ self.user.username + ', Order id: '+ str(self.id)
    


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()


    def __str__(self):
        return 'User: '+ self.order.user.username + ', Product: '+ self.product.name + ', Order id: '+ str(self.order.id)
    
    class Meta:
        ordering = ['-id']

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_address = models.CharField(max_length=200)
    shipment_phone= models.CharField(max_length=50)
    card_number = CardNumberField()
    expire = CardNumberField()
    security_code = SecurityCodeField()