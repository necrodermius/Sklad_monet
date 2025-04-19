from decimal import Decimal

from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", max_length=30,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Last Name", max_length=30,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label="Phone Number", max_length=20,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Така адреса електронної пошти вже використовується.")
        return email

class BonusForm(forms.Form):
    order_amount = forms.DecimalField(
        label="Сума замовлення",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Введіть суму замовлення',
            'step': '0.01'
        })
    )

class UseBonusForm(forms.Form):
    bonus_amount = forms.DecimalField(
        label='Кількість бонусів для використання:',
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        help_text='Введіть, скільки бонусів гість хоче витратити (1 бонус = 1 гривня)'
    )