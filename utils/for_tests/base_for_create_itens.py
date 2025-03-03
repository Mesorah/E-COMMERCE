from home.models import (  # noqa E501
    CartItem,
    Category,
    CustomerQuestion,
    Ordered,
    Products,
)


def create_product(
        user,
        name='Test Product',
        price=150,
        description='Test',
        stock=1,
        is_published=True
        ):
    product = Products.objects.create(
            name=name,
            price=price,
            description=description,
            stock=stock,
            is_published=is_published,
            user=user,
        )

    return product


def create_cart(user):
    cart = Cart.objects.create(user=user)

    return cart


def create_cart_item(cart, product, quantity=1):
    cart_item = CartItem.objects.create(
        cart=cart,
        product=product,
        quantity=quantity
    )

    return cart_item


def create_ordered(
        first_name='Test First',
        last_name='Test Last',
        street_name='Test Street',
        house_number='911',
        ):

    ordered = Ordered.objects.create(
        first_name=first_name,
        last_name=last_name,
        street_name=street_name,
        house_number=house_number,
    )

    return ordered


def create_question(user, question='Question message test'):
    question = CustomerQuestion.objects.create(
        user=user,
        question=question,
    )

    return question


def create_category(name):
    category = Category.objects.create(
        name=name
    )

    return category
