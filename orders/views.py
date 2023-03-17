from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from orders.models import Order, OrderDetail, Payment
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
# Start Payment  Views
##########################################
@login_required(login_url='signin')
def payment(request):
    context = None
    shipment_address = None
    shipment_phone= None
    card_number = None
    expire = None
    security_code = None
    is_added = None

    if request.method == 'POST' and 'btnpayment' in request.POST:
        if 'shipment_address' in request.POST: shipment_address = request.POST['shipment_address']
        if 'shipment_phone' in request.POST: shipment_phone = request.POST['shipment_phone']
        if 'card_number' in request.POST: card_number = request.POST['card_number']
        if 'expire' in request.POST: expire = request.POST['expire']
        if 'security_code' in request.POST: security_code = request.POST['security_code']
        
        if Order.objects.all().filter(user = request.user, is_finished=False):
            order = Order.objects.get(user = request.user, is_finished=False)
            payment = Payment(order = order, shipment_address = shipment_address, shipment_phone = shipment_phone,
                              card_number = card_number , expire = expire, security_code = security_code)
            payment.save()
            order.is_finished = True
            order.save()
            is_added = True
            messages.success(request, 'Your order is Finished')
            


        context = {
            'shipment_address' : shipment_address,
            'shipment_phone' : shipment_phone,
            'card_number' : card_number,
            'expire' : expire,
            'security_code' : security_code,
            'is_added' : is_added,
        }
    else:
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

    return render(request, 'orders/payment.html', context)

##########################################
# Start Sub QTY  Views
##########################################
@login_required(login_url='signin')
def show_orders(request):
    context = None
    all_orders = None
    all_orders = Order.objects.all().filter(user = request.user)
    if all_orders:
        for ord in all_orders:
            order = Order.objects.get(id = ord.id)
            orderdetail = OrderDetail.objects.all().filter(order = order)

            total = 0
            for sub in orderdetail:
                total += sub.price * sub.quantity
            
            ord.total = total
            ord.items_count = orderdetail.count

    context = {
            'all_orders' : all_orders,
        }
    return render(request, 'orders/orders.html', context)