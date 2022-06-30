from django.forms import ModelForm, fields
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields='__all__'


class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude = ['user']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class UpdateUserForm(forms.ModelForm):

    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

                
class ProfileUpdateForm(forms.ModelForm):
            class Meta:
                model = Profile
                fields = ['image']
            
class ProfileUpdateForm(forms.ModelForm):
            class Meta:
                model = Profile
                fields = ['image']