from django import forms
from .models import users_collection


USER_TYPE={
        ('admin', 'admin'),
        ('customer', 'customer'),
        ('owner', 'owner')
    }


class RegisterForm(forms.Form): 
    username = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})) 
    email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})) 
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})) 
    usertype = forms.ChoiceField(choices=USER_TYPE, widget=forms.Select(attrs={'class': 'form-control'}))

class LoginForm(forms.Form): 
    email = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})) 
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})) 
    
    #  <option value="Un Furnished">Un Furnished</option>
    # <option value="Semi Furnished">Semi Furnished</option>
    # <option value="Fully Furnished">Fully Furnished</option>

Furnished={
        ('Un Furnished', 'Un Furnished'),
        ('Semi Furnished', 'Semi Furnished'),
        ('Fully Furnished', 'Fully Furnished')
    }

AvailableFor={
        ('All', 'All'),
        ('Family', 'Family'),
        ('Bachelors', 'Bachelors'),
        ('Commercial', 'Commercial'),
           
    }
    
class NewProperty(forms.Form):
    ownerId = forms.CharField(max_length = 200, widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'formInputOwnerId', 'placeholder': 'Owner Id'}))
    ownerName = forms.CharField(max_length = 200, widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'formInputOwnerName','placeholder': 'Owner Name'}))
    description = forms.CharField(max_length = 500, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    carouselImage1 = forms.CharField(max_length = 1000, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Carousel Image 1'}))
    carouselImage2 = forms.CharField(max_length = 1000, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Carousel Image 2'}))
    carouselImage3 = forms.CharField(max_length = 1000, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Carousel Image 3'}))
    rent = forms.IntegerField( widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rent'}))
    area = forms.IntegerField( widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Area'}))
    deposit = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Deposit'}))
    agreementDuration = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Agreement Duration'}))
    availableFor = forms.ChoiceField(choices=AvailableFor, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Available For'}))
    furnished = forms.ChoiceField(choices=Furnished, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Furnished'}))
    address = forms.CharField(max_length = 500, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    
    
class UpdateProperty(forms.Form):
    ownerId = forms.CharField(max_length = 200, widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'formInputOwnerId', 'placeholder': 'Owner Id'}))
    ownerName = forms.CharField(max_length = 200, widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'formInputOwnerName','placeholder': 'Owner Name'}))
    description = forms.CharField(max_length = 500, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    carouselImage1 = forms.CharField(max_length = 1000, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Carousel Image 1'}))
    carouselImage2 = forms.CharField(max_length = 1000, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Carousel Image 2'}))
    carouselImage3 = forms.CharField(max_length = 1000, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Carousel Image 3'}))
    rent = forms.IntegerField( widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rent'}))
    area = forms.IntegerField( widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Area'}))
    deposit = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Deposit'}))
    agreementDuration = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Agreement Duration'}))
    availableFor = forms.ChoiceField(choices=AvailableFor, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Available For'}))
    furnished = forms.ChoiceField(choices=Furnished, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Furnished'}))
    address = forms.CharField(max_length = 500, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    
    