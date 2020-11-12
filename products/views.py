from django.shortcuts import render, Http404

# Create your views here.

from .models import Product, ProductImage  # relative import from app (.models becoz in the same app)
from marketing.models import MarketingMessage, Slider


# (name.models if want to import from some other app)
# ---------------------------------------------------------------------------

def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        products = Product.objects.filter(title__icontains=q)
        context = {'query': q, 'products': products}
        template = 'products/results.html'
    else:
        context = {}
        template = 'products/home_new.html'
    return render(request, template, context)


def home(request):
    sliders = Slider.objects.all_featured()
    products = Product.objects.all()
    # marketing_message = MarketingMessage.objects.all()[0]
    template = 'products/home_new.html'
    # context = locals()
    context = {'products': products,
               'sliders' : sliders,
               # 'marketing_message': marketing_message,
               }
    return render(request, template, context)


def all(request):
    products = Product.objects.all()  # stored in a variable
    context = {'products': products}  # contain list of all instances of Product class madel in model.py
    template = 'products/all.html'
    return render(request, template, context)


def single(request, slug):
    # try:
    product = Product.objects.get(slug=slug)
    # images = product.productimage_set.all()
    images = ProductImage.objects.filter(product=product)
    print(product.title)
    context = {'product': product, 'images': images}  # contain list of all instances of Product class madel in model.py
    template = 'products/single.html'
    return render(request, template, context)
# except Product.DoesNotExist:
# except:
#     raise Http404
