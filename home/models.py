from django.db import models
from django.conf import settings


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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'],
                                    name='unique_cart_product'
                                    )
        ]

    def __str__(self):
        return f'{self.quantity} x {self.product.name} no carrinho'
