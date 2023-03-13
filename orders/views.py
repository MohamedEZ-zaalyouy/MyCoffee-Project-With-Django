from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from orders.models import Order, OrderDetail
from django.utils import timezone


# Create your views here.
##########################################
# Start Add to cart  Views
##########################################

@login_required(login_url='signin')
def add_to_cart(request):
    if 'pro_id' in request.GET and 'quantity' in request.GET:
        pro_id =  request.GET['pro_id']
        quantity =  request.GET['quantity']

        if not Product.objects.all().filter(id=pro_id).exists():
            return redirect('products')
        
        product = Product.objects.get(id=pro_id)
        price = product.price
        order = Order.objects.all().filter(user=request.user, is_finished = False)
       

        if order:
            old_order = Order.objects.get(user=request.user, is_finished = False)
            orderdetail = OrderDetail.objects.create(product = product, order = old_order, price = price, quantity=quantity )
            orderdetail.save()

            messages.success(request, 'Was added to cart for old order')
        else:
            new_order = Order()
            new_order.user = request.user
            new_order.is_finished=False
            new_order.save()

            orderdetail = OrderDetail.objects.create(product = product, order = new_order, price = price, quantity=quantity )
            orderdetail.save()

            messages.success(request, 'Was added to cart for new order')

        return redirect('/product/'+ request.GET['pro_id'])
    else:
        return redirect('products')


##########################################
# Start cart  Views
##########################################

def cart(request):
    return render(request,'orders/cart.html')