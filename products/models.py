from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save


class Category(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    featured = models.BooleanField(default=None)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# Create your models here.
# if want to add a new field after db has been created take care to add default value in the new field or null values are allowed.
# create product instance
class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(Category, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=99.00)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2,
                                     null=True, blank=True)

    slug = models.SlugField(unique=True)  # slug is going to make up our URL(for that instance) so it should be unique
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)  # created time will be stored
    update = models.DateTimeField(auto_now_add=False, auto_now=True)  # updates time will be stored
    active = models.BooleanField(default=True)  # want to show that product on our site
    update_defaults = models.BooleanField(default=False)

    # methods
    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'slug')  # show kar dega agar product slug kisi se match karega to

    def get_price(self):
        return self.price

    def get_absolute_url(self):
        # return "/products/%s/"%(self.slug)
        return reverse("single_products", args=[self.slug])  # or kwargs={"slug":self.slug} , number of argument 1


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.product.title


class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category='size')

    def colors(self):
        return super(VariationManager, self).filter(active=True).filter(category='color')


VAR_CATEGORIES = (
    ('size', 'size'),
    ('color', 'color'),
    ('package', 'package'),

)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
    title = models.CharField(max_length=120)
    image = models.ForeignKey(ProductImage, null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10000)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects = VariationManager()  # custom query set manager

    def __str__(self):
        return self.title


def product_defaults(sender, instance, created, *args, **kwargs):
    if instance.update_defaults:
        categories = instance.category.all()
        for cat in categories:
            if cat.id == 1:  # for t-shirts
                small_size = Variation.objects.get_or_create(product=instance,
                                                             category='size',
                                                             title='Small')
                medium_size = Variation.objects.get_or_create(product=instance,
                                                              category='size',
                                                              title='Medium')
                large_size = Variation.objects.get_or_create(product=instance,
                                                             category='size',
                                                             title='Large')
        instance.update_defaults = False
        instance.save()


# print args, kwargs

post_save.connect(product_defaults, sender=Product)
