from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Customer, Analyst,User, Profile

class CustomerSignUpForm(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    DOB = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = forms.ChoiceField(choices=gender_choices, required=True)
    city_code = forms.CharField(required=True)
  
    class Meta(UserCreationForm.Meta):
        model = User
 
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user, name=self.cleaned_data.get('name'), email=self.cleaned_data.get('email'), DOB=self.cleaned_data.get('DOB'), gender=self.cleaned_data.get('gender'), city_code=self.cleaned_data.get('city_code'))
        customer.save()
        return customer



class AnalystSignUpForm(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    DOB = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = forms.ChoiceField(choices=gender_choices, required=True)
    city_code = forms.CharField(required=True)
  
    class Meta(UserCreationForm.Meta):
        model = User
 
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_analyst = True
        user.save()
        analyst = Analyst.objects.create(user=user, name=self.cleaned_data.get('name'), email=self.cleaned_data.get('email'), DOB=self.cleaned_data.get('DOB'), gender=self.cleaned_data.get('gender'), city_code=self.cleaned_data.get('city_code'))
        analyst.save()
        return analyst

class CustomerUpdateForm(forms.ModelForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    DOB = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = forms.ChoiceField(choices=gender_choices, required=True)
    city_code = forms.CharField(required=True)
  
    class Meta:
        model = Customer
        fields = ['name', 'DOB', 'gender', 'city_code']
 
    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.name = self.cleaned_data['name']
        customer.DOB = self.cleaned_data['DOB']
        customer.gender = self.cleaned_data['gender']
        customer.city_code = self.cleaned_data['city_code']
        if commit:
            customer.save()
        return customer

class AnalystUpdateForm(forms.ModelForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    DOB = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    gender = forms.ChoiceField(choices=gender_choices, required=True)
    city_code = forms.CharField(required=True)
  
    class Meta:
        model = Analyst
        fields = ['name', 'DOB', 'gender', 'city_code']
 
    def save(self, commit=True):
        analyst = super().save(commit=False)
        analyst.name = self.cleaned_data['name']
        analyst.DOB = self.cleaned_data['DOB']
        analyst.gender = self.cleaned_data['gender']
        analyst.city_code = self.cleaned_data['city_code']
        if commit:
            analyst.save()
        return analyst


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']