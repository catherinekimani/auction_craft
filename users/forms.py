from django import forms
from .models import AuctionItem
# bid form
class BidForm(forms.Form):
    amount = forms.FloatField(label='Bid Amount')
# products form
class AuctionItemForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = ['name', 'price', 'image']