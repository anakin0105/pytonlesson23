from django import forms
from django.core.exceptions import ValidationError
from PIL import Image
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Форма создания/редактирования товара с полной стилизацией и валидацией.
    """

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'photo', 'is_published']

        labels = {
            'name': 'Название товара',
            'category': 'Категория',
            'description': 'Описание товара',
            'price': 'Цена (₽)',
            'photo': 'Фотография товара (JPEG или PNG, макс. 5 МБ)',
            'is_published': 'Опубликовать товар',
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 7}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }

    # ====================== СТИЛИЗАЦИЯ ЧЕРЕЗ __init__ (Задание 3) ======================
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            # Placeholder'ы
            if field_name != 'category':
                field.widget.attrs['placeholder'] = f'Введите {field.label.lower()}'

        # Дополнительная настройка полей
        self.fields['photo'].widget.attrs['accept'] = 'image/jpeg, image/png'

    # ====================== ВАЛИДАЦИЯ ЗАПРЕЩЁННЫХ СЛОВ ======================
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name_lower = name.lower()
            forbidden = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                         'бесплатно', 'обман', 'полиция', 'радар']
            for word in forbidden:
                if word in name_lower:
                    raise ValidationError(f'В названии обнаружено запрещённое слово: «{word}».')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            desc_lower = description.lower()
            forbidden = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                         'бесплатно', 'обман', 'полиция', 'радар']
            for word in forbidden:
                if word in desc_lower:
                    raise ValidationError(f'В описании обнаружено запрещённое слово: «{word}».')
        return description

    # ====================== ВАЛИДАЦИЯ ЦЕНЫ ======================
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена товара не может быть отрицательной!')
        return price

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if not photo:
            return photo

        if hasattr(photo, 'content_type') and hasattr(photo, 'size'):
            # Проверка размера
            if photo.size > 5 * 1024 * 1024:
                raise ValidationError('Размер изображения не должен превышать 5 МБ.')

            # Проверка MIME-типа
            if photo.content_type not in ['image/jpeg', 'image/png']:
                raise ValidationError('Разрешены только изображения в формате JPEG или PNG.')

            # Проверка через Pillow
            try:
                photo.seek(0)  # сбрасываем указатель перед чтением
                img = Image.open(photo)
                img.verify()
                if img.format not in ['JPEG', 'PNG']:
                    raise ValidationError('Файл должен быть в формате JPEG или PNG.')
            except ValidationError:
                raise
            except Exception:
                raise ValidationError('Файл повреждён или не является корректным изображением.')
            finally:
                photo.seek(0)  # сбрасываем после verify(), НО НЕ ЗАКРЫВАЕМ!

        else:
            if hasattr(photo, 'name'):
                filename = photo.name.lower()
                if not filename.endswith(('.jpg', '.jpeg', '.png')):
                    raise ValidationError('Разрешены только изображения в формате JPEG или PNG.')

            try:
                img = Image.open(photo.path)
                img.verify()
                if img.format not in ['JPEG', 'PNG']:
                    raise ValidationError('Файл должен быть в формате JPEG или PNG.')
            except ValidationError:
                raise
            except Exception:
                raise ValidationError('Существующее изображение повреждено.')

        return photo