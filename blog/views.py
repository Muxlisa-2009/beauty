from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

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


