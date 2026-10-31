from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404

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
    # Barcha mahsulotlarni olish
    products_list = Product.objects.all().order_by('-id')

    # Har bir sahifada 6 tadan mahsulot ko'rsatish
    paginator = Paginator(products_list, 6)
    page_number = request.GET.get('page')

    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # Agar sahifa raqami berilmagan bo'lsa, 1-sahifani ko'rsatadi
        products = paginator.page(1)
    except EmptyPage:
        # Agar sahifa raqami juda katta bo'lsa, oxirgi sahifani ko'rsatadi
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
    }
    return render(request, 'shop.html', context)

def women(request):
    return render(request,'single-product-page.html')

def not_found(request):
    return render(request,'404.html')

def checkout(request):
    return render(request,'checkout.html')


def product_detail(request, slug):
    # Slug orqali mahsulotni topamiz, agar topilmasa 404 xatoligini chiqaradi
    product = get_object_or_404(Product, slug=slug)

    # Shu kategoriyadagi boshqa o'xshash mahsulotlardan 4 tasini tavsiya sifatida olish (ixtiyoriy)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)


def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Mehmonlar uchun session ishlatamiz
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart


# Mahsulotni savatga qo'shish
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request)

    # Savatda bu mahsulot allaqachon bormi tekshiramiz
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')


# Savat sahifasini ko'rsatish
def cart_detail(request):
    cart = _get_or_create_cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context)




def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart