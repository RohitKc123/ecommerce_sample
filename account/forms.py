from django.forms import ModelForm
from django import forms
from .models import User
from django.contrib.auth.models import Group


class User_register(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'image', 'address', 'phone_number', 'password']
        widgets = {
            # telling Django your password field in the mode is a password input on the template
            'password': forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super(User_register, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")
        if password != confirm_password:
            raise forms.ValidationError(
                {
                    'password': "Password and confirm_password doesnt not match"
                }
            )
        phone_number = self.cleaned_data.get("phone_number")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if first_name.isnumeric() and last_name.isnumeric():
            raise forms.ValidationError({
                'first_name': "First name cannot be numeric",
                'last_name': "Last name cannot be numeric"
            })
        if len(str(phone_number)) != 10:
            raise forms.ValidationError({
                'phone_number': "Invalid phone number"
            })
        if not str(phone_number)[:2] in ['98', '97', '96']:
            raise forms.ValidationError({
                'phone_number': "Invalid phone number"
            })

        user = User.objects.filter(email__iexact=email)
        if user.exists():
            raise forms.ValidationError({
                'email': 'User with that email already exists'
            })

    # def clean_phone_number(self):

    def save(self, commit=True):
        instance = super(User_register, self).save(commit=False)
        if commit:
            instance.set_password(self.cleaned_data.get('password'))
            # instance.groups.add(Group.objects.get(name="Buyer"))
            instance.save()
        return instance


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    widgets = {
        # telling Django your password field in the mode is a password input on the template
        'password': forms.PasswordInput()
    }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError({
                "email": "Invalid Email"
            })

        user = User.objects.get(email__iexact=email)
        if not user.check_password(password):
            raise forms.ValidationError({
                "password": "Invalid password"
            })



class UpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'address', 'image', 'phone_number']

    def clean(self):
        cleaned_data = super(UpdateUser, self).clean()
        phone_number = self.cleaned_data.get("phone_number")
        if len(str(phone_number)) != 10:
            raise forms.ValidationError({
                'phone_number': "Invalid phone number"
            })
        if not str(phone_number)[:2] in ['98', '97', '96']:
            raise forms.ValidationError({
                'phone_number': "Invalid phone number"
            })
