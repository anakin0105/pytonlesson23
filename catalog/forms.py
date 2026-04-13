from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'photo']

        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

        labels = {
            'name': 'Название товара',
            'category': 'Категория',
            'description': 'Описание товара',
            'price': 'Цена (₽)',
            'photo': 'Фотография товара',
        }