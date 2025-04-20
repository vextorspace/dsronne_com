from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get('password1')
        pwd2 = cleaned_data.get('password2')
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        # Use email as username
        user = User.objects.create_user(username=email, email=email, password=password)
        return user