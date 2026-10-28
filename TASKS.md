# Beauty — bosh sahifaga mahsulotlarni bazadan chiqarish

Hozir `Product` modeli bor, admin orqali 10 ta mahsulot qo'shilgan, lekin bosh sahifada hali ham
shablondagi qo'lda yozilgan 8 ta kartochka chiqyapti. Endi ularni bazadan chiqaramiz.

Tartib bilan qil. Har bir qismdan keyin `python manage.py runserver` qilib tekshirib tur.

## Qilingan ishlar

- `blog/models.py` — `Product` ga `is_popular` maydoni qo'shildi.
- `blog/admin.py` — `is_popular` ro'yxatda chiqadi, filtrda bor, `list_editable` bilan galochka qo'yiladi.
- `config/urls.py` — `static(settings.MEDIA_URL, ...)` qo'shildi.

Quyida qolgan ishlar.

---

## 1-qism. Rasmlar (media)

**1. `MEDIA_URL` va `MEDIA_ROOT` yo'q**
`config/urls.py` da `settings.MEDIA_URL` ishlatilyapti, lekin `settings.py` da u yozilmagan.
Django o'zi `MEDIA_URL = '/'` qo'yadi, natijada saytdagi har qanday noto'g'ri manzil fayl sifatida qidiriladi.
Admin orqali yuklangan rasmlar esa loyiha ildizidagi `products/` papkaga tushib, git ga kirib ketgan.

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

Tekshir: brauzerda `http://127.0.0.1:8000/media/products/1.jpg` ochilib rasm chiqishi kerak.

---

## 2-qism. Migratsiya

**3. `is_popular` uchun migratsiya yo'q**
Modelga maydon qo'shilgan, lekin `makemigrations` qilinmagan. Bazada bu ustun yo'q,
admin da mahsulotlar ro'yxatini ochsang xato chiqadi.
```
python manage.py makemigrations
python manage.py migrate
```
`blog/migrations/` da `0003_product_is_popular.py` paydo bo'lishi kerak. Uni ham commit qil.

Keyin admin ga kirib, 4 ta mahsulotga "Mashhurmi?" galochkasini qo'y.
Bir nechtasiga `Chegirmadagi narxi` ham yoz.

---

## 3-qism. View

**4. `index` view shablonga hech narsa bermayapti**
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

**5. "Popular products" bloki qo'lda yozilgan**
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

**6. "Latest products" bloki ham qo'lda yozilgan**
`<section id="latest-products">` ichida ham xuddi shunday qil. Kod bir xil, faqat birinchi qatorda:
```django
  {% for p in latest_products %}
```

---

## Tekshirish

- Admin da mahsulotlar ro'yxati xatosiz ochiladi, "Mashhurmi?" galochkasi qo'yiladi.
- Bosh sahifada "Popular products" da galochka qo'yilgan 4 ta mahsulot chiqadi.
- "Latest products" da oxirgi qo'shilgan 4 ta mahsulot chiqadi.
- Rasmlar ochiladi, kategoriya nomi chiqadi, chegirmasi borlarda eski narx ustidan chizilgan.
- Admin da yangi mahsulot qo'shsang, u "Latest products" da birinchi bo'lib chiqadi.
- `git status` da `media/` papka ko'rinmaydi.

Hammasi ishlasa commit qilib push qil.
