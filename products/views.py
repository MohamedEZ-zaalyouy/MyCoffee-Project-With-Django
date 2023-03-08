from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


def products(request):
    products = Product.objects.all()
    context = {
        'products':products,
    }
    return render(request, 'products/products.html',context)



def product(request,pro_id):
    # product = Product.objects.get(id = pro_id)
    product = get_object_or_404(Product, pk=pro_id)
    context = {
        'product':product,
    }
    return render(request, 'products/product.html',context)



def search(request):
    return render(request, 'products/search.html')


def searchProduct(request):
    products = Product.objects.all()
    cs = None
    if 'cs' in request.GET:
        cs = request.GET['cs']
        if not cs:
            cs ='off'

    if 'SearchName' in request.GET:
        SearchName= request.GET['SearchName']
        if SearchName:
            if cs =='on':
                products = products.filter(name__contains = SearchName)
            else:
                products = products.filter(name__icontains = SearchName)

    if 'SearchDesc' in request.GET:
        SearchDesc= request.GET['SearchDesc']
        if SearchDesc:
            if cs == 'on':
                products = products.filter(description__contains = SearchDesc)
            else:
                products = products.filter(description__icontains = SearchDesc)
    
    if 'SearchPriceMin' in request.GET and 'SearchPriceMax' in request.GET:
        SearchPriceMin= request.GET['SearchPriceMin']
        SearchPriceMax= request.GET['SearchPriceMax']
        if SearchPriceMin and SearchPriceMax:
            if SearchPriceMin.isdigit() and SearchPriceMax.isdigit():
                products = products.filter(price__gte= SearchPriceMin, price__lte= SearchPriceMax)
            
    
    
    # cs= request.GET['cs']

    context = {
        'products':products,
    }
    return render(request, 'products/searchProduct.html',context)