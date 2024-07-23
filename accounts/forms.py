from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'phone_numbers', 'address', 'profile_picture']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        print(f"Cleaning email: {email}") 
        if email and '@' not in email:
            raise forms.ValidationError('Please enter a valid email address with an @ symbol.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    def clean_phone_numbers(self):
        phone_numbers = self.cleaned_data.get('phone_numbers', '')
        
        # Split phone numbers by comma
        phone_numbers_list = [num.strip() for num in phone_numbers.split(',')]
        
        # Validate each phone number
        for number in phone_numbers_list:
            if not (number.isdigit() and len(number) == 10):
                raise forms.ValidationError(f"Phone number '{number}' should be exactly 10 digits long and contain only numbers.")
        
        return ', '.join(phone_numbers_list)  # Optionally join back into a single string

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='username')
    password = forms.CharField(widget=forms.PasswordInput, label='password')


