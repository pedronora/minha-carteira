from django import forms
from .models import FII, FIIByUser, Operacao


class UpSertFiiForm(forms.ModelForm):
    class Meta:
        model = FII
        fields = '__all__'
        labels = {'codigo': 'Código', 'image_url': 'Imagem Url'}
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código'
            }),
            'image_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Imagem Url'
            }),
        }


class AddFIIForm(forms.ModelForm):
    class Meta:
        model = FIIByUser
        fields = ['fii']
        labels = {'fii': 'FIIs'}
        widgets = {
            'fii': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class UpSertOperacaoForm(forms.ModelForm):

    class Meta:
        model = Operacao
        fields = ['data', 'nr_nota', 'tipo', 'preco', 'quantidade', 'custos']
        labels = {'nr_nota': 'Nr. da Nota', 'tipo': 'Tipo de Operação', 'preco': 'Preço'}
        widgets = {
            'data': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Data da Operação',
                'onfocus': 'this.type="date"'
            }),
            'nr_nota': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nr. da Nota'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Tipo da Operação',
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Preço'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantidade'
            }),
            'custos': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Custos'
            }),
        }
