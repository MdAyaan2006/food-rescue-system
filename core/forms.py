from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, FoodListing, ContactMessage

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'user_type', 'organization_name', 'phone_number')

# NEW: Form to allow users to update their details
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'organization_name')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class FoodListingForm(forms.ModelForm):
    class Meta:
        model = FoodListing
        fields = ('title', 'description', 'quantity_kg', 'expiry_time', 'location')
        widgets = {
            'expiry_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'subject', 'message')
        widgets = {'message': forms.Textarea(attrs={'rows': 5})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'