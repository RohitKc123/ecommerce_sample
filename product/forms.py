from django import forms
from .models import Product, Order
from bootstrap_modal_forms.forms import BSModalModelForm

class product_form(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['user']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_by', 'shipping_address', 'mobile', 'email', 'payment_method']


    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        mobile = cleaned_data.get('mobile')
        if len(str(mobile)) != 10:
            raise forms.ValidationError({
                'mobile': "Invalid phone number"
            })
        if not str(mobile)[:2] in ['98', '97', '96']:
            raise forms.ValidationError({
                'mobile': "Invalid phone number"
            })
