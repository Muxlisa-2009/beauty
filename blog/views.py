from django.shortcuts import render

from blog.models import Product


# Create your views here.
def index(request):
    products = Product.objects.filter(is_available=True).select_related('category')
    context = {
        'popular_products': products.filter(is_popular=True)[:4],
        'latest_products': products.order_by('-created_at')[:4],
    }
    return render(request, 'index.html', context)


def cart(request):
    return render(request,'cart.html')

def shop(request):
    return render(request,'shop.html')

def women(request):
    return render(request,'single-product-page.html')

def not_found(request):
    return render(request,'404.html')

def checkout(request):
    return render(request,'checkout.html')


