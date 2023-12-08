from django.contrib import admin
from . models import *

admin.site.register(Customer) #customer model
admin.site.register(AuctionItem) #product model
admin.site.register(AuctionItemFeature) #feature model
admin.site.register(AuctionItemReview) #review model
admin.site.register(Purchase) #order model
admin.site.register(PurchaseItem) #order item model
admin.site.register(PurchaseDetail) #checkout model
admin.site.register(OrderUpdate) #update order model
admin.site.register(UserContact) #contact model