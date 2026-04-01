from symtable import Class

from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название товара",
        help_text="Введите название товара",
    )
    description = models.TextField(
        verbose_name="Описание товара",
        help_text="Введите описание товара",
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to="catalog/photos/",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото товара",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Выберите категорию товара",
        null=True,
        blank=True,
        related_name="products",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        default='+7 (000) 000-00-00'  # значение по умолчанию
    )
    message = models.TextField(verbose_name="Сообщение", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"{self.name} ({self.phone})"

    class Meta:
        verbose_name = "Контактное сообщение"
        verbose_name_plural = "Контактные сообщения"