from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, Variation, Category


# changes in admin dashboard
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'  # updated
    search_fields = ['title', 'description']  # search
    list_display = ['title', 'price', 'slug', 'active', 'update']  # various columns
    list_editable = ['price', 'active']  # editable in dashboard too
    list_filter = ['price', 'active']  # filter
    readonly_fields = ['update', 'timestamp']
    prepopulated_fields = {"slug": ("title",)}  # autofill based on what we are typing

    class Meta:  # ask?
        model = Product


admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)
admin.site.register(Variation)
admin.site.register(Category)
