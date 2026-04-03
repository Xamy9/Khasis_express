from django import forms
from .models import ServiceRequest
from .models import BusinessImage        
from .models import ContactMessage




class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = [
            "pickup_location",
            "destination",
            "sender_phone_number",
            "receiver_name",
            "receiver_phone_number",
            "package_description",
            "weight"
        ]

        widgets = {
            "pickup_location": forms.TextInput(attrs={"class": "form-control"}),
            "destination": forms.TextInput(attrs={"class": "form-control"}),
            "sender_phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "receiver_name": forms.TextInput(attrs={"class": "form-control"}),
            "receiver_phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "package_description": forms.TextInput(attrs={"class": "form-control"}),
            "weight": forms.NumberInput(attrs={"class": "form-control"}),
        }
        
        
class BusinessImageForm(forms.ModelForm):
    class Meta:
        model = BusinessImage
        fields = ['title', 'image', 'description']        
        
        


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }