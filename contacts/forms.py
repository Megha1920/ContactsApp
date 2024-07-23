from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    phone_numbers = forms.CharField(
        widget=forms.Textarea,
        help_text="Enter phone numbers separated by commas. Each phone number must be exactly 10 digits long."
    )

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'address', 'company', 'phone_numbers']