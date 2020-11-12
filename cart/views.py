from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse

# Create your views here.
from django.views.decorators.http import require_POST

from products.models import Product, Variation
from .models import Cart, CartItem


def view(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None

    if the_id:
        x = 0.00
        for item in cart.cartitem_set.all():
            line_total = float(item.product.price) * item.quantity
            x = x + line_total

        request.session['items_total'] = cart.cartitem_set.count()  # number of items in cart # items_total is the key
        cart.total = x
        cart.save()
        context = {'cart': cart}
    else:
        empty_msg = "Your Cart Is Empty, Please Keep Shopping."
        context = {"empty": True, "empty_msg": empty_msg}

    template = "cart/view.html"
    return render(request, template, context, )


# -----------------------------------------------------------------------------------

def remove_from_cart(request, id, slug):
    print(id)
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        return HttpResponseRedirect(reverse("cart"))

    cartitem = CartItem.objects.get(id=id)
    cartitem.cart = None
    cartitem.save()
    # send sucess msg
    return HttpResponseRedirect(reverse("cart"))


# -----------------------------------------------------------------------------------
def add_to_cart(request, id):
    request.session.set_expiry(1200000)  # logout

    try:
        the_id = request.session['cart_id']
    except:
        # create cart id
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id
    cart = Cart.objects.get(id=the_id)

    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        pass
    except:
        pass

    # list of objects
    product_var = []  # product variation
    if request.method == "POST":
        qty = request.POST['qty']
        # if int(qty) <= 0:
        for item in request.POST:
            key = item
            val = request.POST[key]
            try:
                v = Variation.objects.get(product=product, category__iexact=key, title__iexact=val)
                product_var.append(v)
            except:
                pass
        cart_item = CartItem.objects.create(cart=cart,
                                            product=product)  # not unique we will make it unique by adding session
        # ("cart item object", "true/false")              #create cart item with that specific product

        # adding the variation in the cart
        if len(product_var) > 0:
            cart_item.variations.add(*product_var)
        cart_item.quantity = qty
        cart_item.save()

        # if not cart_item in cart.items.all():
        #     cart.items.add(cart_item)
        # else:
        #     cart.items.remove(cart_item)
        #sucess msg
        return HttpResponseRedirect(reverse("cart"))
    #error msgs
    return HttpResponseRedirect(reverse("cart"))

## we will use session to store the id for whatever session u r in
## when u login u enter into a session when u log out u delete that session
## creating cart instance for each session


# -----------------------------------------------------------------------------------------
