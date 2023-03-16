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
       

        if order: # Il y a  Old order
            old_order = Order.objects.get(user=request.user, is_finished = False)
            if OrderDetail.objects.all().filter(order= old_order, product = product):
                orderdetail = OrderDetail.objects.get(order= old_order, product = product)
                orderdetail.quantity += int(quantity)
                orderdetail.save()
            else:
                orderdetail = OrderDetail.objects.create(product = product, order = old_order, price = price, quantity=quantity )
                orderdetail.save()

            messages.success(request, 'Was added to cart for old order')
        else: # add new order
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
@login_required(login_url='signin')
def cart(request):
    context = None

    if Order.objects.all().filter(user = request.user, is_finished=False):
        order = Order.objects.get(user = request.user, is_finished=False)
        orderdetail = OrderDetail.objects.all().filter(order = order)

        total = 0
        for sub in orderdetail:
            total += sub.price * sub.quantity

        context = {
            'order' : order,
            'orderdetail' : orderdetail,
            'total' : total,
        }

    return render(request,'orders/cart.html',context)


##########################################
# Start remove_from_cart  Views
##########################################
@login_required(login_url='signin')
def remove_from_cart(request, orderdetails_id):
    if orderdetails_id:
        orderdetails = OrderDetail.objects.get(id = orderdetails_id)
        if orderdetails:
            if orderdetails.order.user.id == request.user.id:
                orderdetails.delete()            
    return redirect('cart')

##########################################
# Start add_QTY  Views
##########################################
@login_required(login_url='signin')
def add_QTY(request, orderdetails_id):
    if orderdetails_id:
        orderdetails = OrderDetail.objects.get(id = orderdetails_id)
        if orderdetails:
            if orderdetails.order.user.id == request.user.id:
                orderdetails.quantity +=1
                orderdetails.save()            
    return redirect('cart')


##########################################
# Start Sub QTY  Views
##########################################
@login_required(login_url='signin')
def sub_QTY(request, orderdetails_id):
    if orderdetails_id:
        orderdetails = OrderDetail.objects.get(id = orderdetails_id)
        if orderdetails:
            if orderdetails.order.user.id == request.user.id:
                if orderdetails.quantity > 1:
                    orderdetails.quantity -=1
                    orderdetails.save()            
    return redirect('cart')

##########################################
# Start Sub QTY  Views
##########################################
@login_required(login_url='signin')
def payment(request):
    return render(request, 'orders/payment.html')