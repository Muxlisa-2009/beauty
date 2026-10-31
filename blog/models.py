from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True, help_text="URL uchun unikal nom (masalan: t-shirts)")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Kategoriya rasmi")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Kategoriyasi"
    )
    name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name="Tavsifi")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Chegirmadagi narxi"
    )
    image = models.ImageField(upload_to='products/', verbose_name="Asosiy rasmi")
    is_available = models.BooleanField(default=True, verbose_name="Mavjudmi?")
    is_popular = models.BooleanField(default=False, verbose_name="Mashhurmi?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    # Agar foydalanuvchi ro'yxatdan o'tgan bo'lsa
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Ro'yxatdan o'tmagan mehmonlar uchun session ID
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Savat: {self.user.username}"
        return f"Mehmon savati: {self.session_id}"

    @property
    def total_price(self):
        # Savatdagi barcha mahsulotlarning umumiy narxi
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product',
                                on_delete=models.CASCADE)  # Product modelingiz shu faylda yoki import qilingan bo'lishi kerak
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        # Bitta mahsulot turi uchun umumiy narx (miqdor * narx)
        price = self.product.discount_price if self.product.discount_price else self.product.price
        return price * self.quantity