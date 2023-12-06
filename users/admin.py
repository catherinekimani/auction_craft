from django.contrib import admin
from .models import AuctionItem, ShoppingCartItem

# Register your models here.

admin.site.register(AuctionItem)
admin.site.register(ShoppingCartItem)