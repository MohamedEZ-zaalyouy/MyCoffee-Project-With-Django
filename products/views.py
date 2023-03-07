from django.shortcuts import render
from .models import Product

# Create your views here.


def products(request):
    products = Product.objects.all()
    context = {
        'products':products,
    }
    return render(request, 'products/products.html',context)



def product(request):
    return render(request, 'products/product.html')



def search(request):
    return render(request, 'products/search.html')