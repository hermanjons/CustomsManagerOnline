from django import forms
from .models import ClientProfile, CustomUser, ConsultantProfile
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Kullanıcı Adı", widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Kullanıcı adınız'
    }))
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Şifreniz'
    }))



class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(role='client')


class ConsultantProfileForm(forms.ModelForm):
    class Meta:
        model = ConsultantProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(role='consultant')
