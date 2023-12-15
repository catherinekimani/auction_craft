from django import forms
class BidForm(forms.Form):
    amount = forms.FloatField(label='Bid Amount')