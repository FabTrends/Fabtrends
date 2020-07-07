from django import forms
from .models import Order,Refund,CheckZipcode

class OrderCreateForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['address_type','first_name', 'last_name', 'email','phone_number','house_number','town','city','district','state','country','postal_code','full_address']
        
class CheckZipcodeForm(forms.Form):
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Check zipcode for delivery',
        'aria-label': 'zipcode checker',
        'aria-describedby': 'basic-addon2'
    }))

class RequestRefundForm(forms.Form):
    order_id = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()