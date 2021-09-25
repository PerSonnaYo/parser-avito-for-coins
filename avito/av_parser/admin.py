from django.contrib import admin
from .forms import ProductForm
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'url')
    list_filter = ('price', )
    form = ProductForm
# Register your models here.
