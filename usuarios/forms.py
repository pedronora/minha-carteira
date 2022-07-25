from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, label='Primeiro Nome',
                                 max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro Nome'}))
    last_name = forms.CharField(required=True, label='Último Nome',
                                max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Último Nome'}))

    class Meta:
        model = User
        fields = (
            'username', 'first_name',
            'last_name', 'email',
            'password1', 'password2'
        )

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Usuário'
        }
        self.fields['password1'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Senha'
        }
        self.fields['password2'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Confirmação de senha'
        }
