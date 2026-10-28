# Beauty — bosh sahifaga mahsulotlarni bazadan chiqarish

Hozir `Product` modeli bor, admin orqali 10 ta mahsulot qo'shilgan, lekin bosh sahifada hali ham
shablondagi qo'lda yozilgan 8 ta kartochka chiqyapti. Endi ularni bazadan chiqaramiz.

Tartib bilan qil. Har bir qismdan keyin `python manage.py runserver` qilib tekshirib tur.

---

## 1-qism. Rasmlar (media)

**1. `MEDIA_URL` va `MEDIA_ROOT` yo'q**
Admin orqali yuklangan rasmlar loyiha ildizidagi `products/` papkaga tushib qolgan va git ga ham kirib ketgan.
Yuklangan fayllar `media/` papkada turishi kerak.

`config/settings.py` da `STATICFILES_DIRS` dan keyin qo'sh:
```python
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**2. `products/` papkani `media/` ichiga ko'chir**
Terminalda (loyiha papkasida):
```
git rm -r --cached products
mkdir media
mv products media/
```
Bazadagi yo'llar (`products/1.jpg`) o'zgarmaydi, chunki ular `MEDIA_ROOT` ga nisbatan yoziladi.
`.gitignore` da `/media/` bor, shuning uchun endi rasmlar git ga tushmaydi.

**3. Rasmlar brauzerda ochilmaydi**
Django `runserver` da media fayllarni o'zi bermaydi, buni `urls.py` da yoqish kerak.

`config/urls.py` ni shunday qil:
```python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Tekshir: brauzerda `http://127.0.0.1:8000/media/products/1.jpg` ochilib rasm chiqishi kerak.

---

## 2-qism. "Popular" belgisi

**4. Qaysi mahsulot mashhur ekanini bilib bo'lmaydi**
Bosh sahifada ikkita blok bor: "Popular products" va "Latest products".
"Latest" — oxirgi qo'shilganlar (`created_at` bo'yicha). "Popular" uchun esa modelda maydon yo'q.

`blog/models.py` da `Product` ichiga, `is_available` dan keyin qo'sh:
```python
    is_popular = models.BooleanField(default=False, verbose_name="Mashhurmi?")
```
Keyin:
```
python manage.py makemigrations
python manage.py migrate
```

**5. Admin da belgilashni qulay qil**
`blog/admin.py` da `ProductAdmin` ni shunday qil:
```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'is_popular', 'created_at')
    list_filter = ('category', 'is_available', 'is_popular')
    list_editable = ('is_popular',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
```
`list_editable` — ro'yxatning o'zida galochka qo'yish mumkin bo'ladi.
Admin ga kirib, 4 ta mahsulotga "Mashhurmi?" galochkasini qo'y. Bir nechtasiga `Chegirmadagi narxi` ham yoz.

---

## 3-qism. View

**6. `index` view shablonga hech narsa bermayapti**
`blog/views.py` ning tepasiga import qo'sh:
```python
from .models import Product
```
`index` funksiyasini shunday qil:
```python
def index(request):
    products = Product.objects.filter(is_available=True).select_related('category')
    context = {
        'popular_products': products.filter(is_popular=True)[:4],
        'latest_products': products.order_by('-created_at')[:4],
    }
    return render(request, 'index.html', context)
```
- `filter(is_available=True)` — sotuvda yo'q mahsulotlar chiqmaydi.
- `select_related('category')` — shablonda `p.category.name` yozganda har bir mahsulot uchun
  alohida so'rov ketmasligi uchun.
- `[:4]` — faqat 4 tasi olinadi.

---

## 4-qism. Shablon

**7. "Popular products" bloki qo'lda yozilgan**
`templates/index.html` da `<section id="popular-products">` ichida 4 ta bir xil kartochka bor
(`<!-- Product 1 -->` ... `<!-- Product 4 -->`). Hammasini o'chir, o'rniga bitta kartochkani `for` ichida yoz.

`<div class="flex flex-wrap -mx-4">` ichi shunday bo'lsin:
```django
<div class="flex flex-wrap -mx-4">
  {% for p in popular_products %}
    <div class="w-full sm:w-1/2 lg:w-1/4 px-4 mb-8">
      <div class="bg-white p-3 rounded-lg shadow-lg">
        <img src="{{ p.image.url }}" alt="{{ p.name }}" class="w-full object-cover mb-4 rounded-lg">
        <a href="#" class="text-lg font-semibold mb-2">{{ p.name }}</a>
        <p class="my-2">{{ p.category.name }}</p>
        <div class="flex items-center mb-4">
          {% if p.discount_price %}
            <span class="text-lg font-bold text-primary">{{ p.discount_price|floatformat:0 }} so'm</span>
            <span class="text-sm line-through ml-2">{{ p.price|floatformat:0 }} so'm</span>
          {% else %}
            <span class="text-lg font-bold text-gray-900">{{ p.price|floatformat:0 }} so'm</span>
          {% endif %}
        </div>
        <button class="bg-primary border border-transparent hover:bg-transparent hover:border-primary text-white hover:text-primary font-semibold py-2 px-4 rounded-full w-full">Add to Cart</button>
      </div>
    </div>
  {% empty %}
    <p class="px-4">Mahsulotlar yo'q</p>
  {% endfor %}
</div>
```
- `{{ p.image.url }}` — rasm `media/` dan keladi, `{% static %}` bu yerda ishlatilmaydi.
- `{% if p.discount_price %}` — chegirma bo'lsa ikkala narx chiqadi, eskisi ustidan chizilgan.
- `floatformat:0` — narx `10000.00` emas, `10000` bo'lib chiqadi.
- `{% empty %}` — ro'yxat bo'sh bo'lsa shu matn chiqadi.

**8. "Latest products" bloki ham qo'lda yozilgan**
`<section id="latest-products">` ichida ham xuddi shunday qil. Kod bir xil, faqat birinchi qatorda:
```django
  {% for p in latest_products %}
```

---

## Tekshirish

- Bosh sahifada "Popular products" da galochka qo'yilgan 4 ta mahsulot chiqadi.
- "Latest products" da oxirgi qo'shilgan 4 ta mahsulot chiqadi.
- Rasmlar ochiladi, kategoriya nomi chiqadi, chegirmasi borlarda eski narx ustidan chizilgan.
- Admin da yangi mahsulot qo'shsang, u "Latest products" da birinchi bo'lib chiqadi.
- `git status` da `media/` papka ko'rinmaydi.

Hammasi ishlasa commit qilib push qil.
