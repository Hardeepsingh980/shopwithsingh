from django.contrib import admin
from .models import Category, Color, Product, Sizes, Review, Order

admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(Sizes)
admin.site.register(Review)
admin.site.register(Order)

# Register your models here.
