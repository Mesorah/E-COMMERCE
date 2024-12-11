from django.conf import settings
from django.db import models


class Products(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    cover = models.ImageField(
        upload_to='products/%Y/%m/%d/',
        blank=True, null=True,
        default='default/image_default.png'
    )
    name = models.CharField(max_length=55)
    price = models.IntegerField()
    description = models.TextField(null=True)
    stock = models.IntegerField(null=True)  # colocar positiveinteger
    is_published = models.BooleanField(null=True, default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}'


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cart'  # user.cart  Retorna o carrinho
                             # associado ao usuário
    )

    def __str__(self):
        return f'Carrinho do {self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,
                             related_name='items',
                             on_delete=models.CASCADE
                             )
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_ordered = models.BooleanField(default=False)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['cart', 'product'],
    #                                 name='unique_cart_product'
    #                                 )
    #     ]

    # Não faz sentido ser unique por causa do is_ordered

    def __str__(self):
        return f'{self.quantity} x {self.product.name} no carrinho'


class Ordered(models.Model):
    number_ordered = models.PositiveIntegerField(default=1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=100, default='')
    street_name = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    products = models.ManyToManyField(CartItem, related_name='ordered')

    def __str__(self):
        return f'{self.number_ordered}: {self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        last_order = Ordered.objects.order_by('-number_ordered').first()

        if last_order:
            self.number_ordered = last_order.number_ordered + 1
        else:
            self.number_ordered = 1

        return super().save(*args, **kwargs)
