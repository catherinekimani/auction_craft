from django.db import models
from django.contrib.auth.models import User

# image
from cloudinary.models import CloudinaryField

from django.core.exceptions import ObjectDoesNotExist

# time imports
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now


# Customer model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    added_items = models.ManyToManyField('AuctionItem', related_name='sellers', blank=True)

    def __str__(self):
        return str(self.user)

# AuctionItem model
class AuctionItem(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = CloudinaryField('image')

    @property
    def bid_end_time(self):
        try:
            latest_bid = self.bid_set.latest('timestamp')
            return latest_bid.timestamp + timedelta(days=1)
        except ObjectDoesNotExist:
            return timezone.now() + timedelta(days=1)

# AuctionItemFeature model
class AuctionItemFeature(models.Model):
    product = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    feature = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.product) + " Feature: " + self.feature

# AuctionItemReview model
class AuctionItemReview(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    product = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.customer) +  " Review: " + self.content

# purchase model
class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(default=now)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.purchaseitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.purchaseitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

# purchase item model
class PurchaseItem(models.Model):
    product = models.ForeignKey(AuctionItem, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.order)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

# order update model
class OrderUpdate(models.Model):
    order_id = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    desc = models.CharField(max_length=500)
    date = models.DateField(default=now)

    def __str__(self):
        return str(self.order_id)

# purchase details model
class PurchaseDetail(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    total_amount = models.CharField(max_length=10, blank=True,null=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    payment = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return self.address
# user contact info
class UserContact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

# bid model
class Bid(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.customer} bid {self.amount} on {self.item}"