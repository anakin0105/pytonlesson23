from django.views.generic import (
    ListView, DetailView, CreateView, TemplateView, DeleteView, UpdateView
)
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from io import BytesIO
from PIL import Image
from .models import Product, CompanyContacts, Contact, Category
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# ==================== ПРОДУКТЫ ====================

class HomePageView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Показываем только опубликованные товары
        context['latest_products'] = Product.objects.filter(
            is_published=True
        ).order_by('-created_at')[:5]
        context['categories'] = Category.objects.all().order_by('name')

        # === Дополнительное задание: вывод в консоль ===
        print("\n" + "=" * 75)
        print("ПОСЛЕДНИЕ 5 ОПУБЛИКОВАННЫХ ПРОДУКТОВ")
        print("=" * 75)
        latest = context['latest_products']
        if latest.exists():
            for i, product in enumerate(latest, 1):
                print(f"{i:2d}. {product.name} (by {product.owner.email if product.owner else '—'})")
                print(f"     Цена: {product.price} ₽")
                print(f"     Создан: {product.created_at.strftime('%d.%m.%Y')}")
                print("-" * 70)
        else:
            print("Пока нет опубликованных продуктов.")
        print("=" * 75 + "\n")

        return context


class ProductsCatalogView(ListView):
    model = Product
    template_name = 'catalog/products_catalog.html'
    context_object_name = 'products'
    paginate_by = 6
    ordering = ['-created_at']

    def get_queryset(self):
        return Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')

        # Добавляем все категории
        context['categories'] = Category.objects.all().order_by('name')

        return context

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = 'users:login'
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'      # ← изменили
    success_url = reverse_lazy('catalog:my_products')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # автоматически присваиваем владельца
        messages.success(self.request, '✅ Товар успешно добавлен!')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = 'users:login'
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:my_products')

    def test_func(self):
        """Только владелец или модератор может редактировать товар"""
        product = self.get_object()
        return (
                self.request.user == product.owner or
                self.request.user.has_perm('catalog.can_unpublish_product') or
                self.request.user.is_staff
        )

    def form_valid(self, form):
        if self.request.user.has_perm('catalog.can_unpublish_product'):
            messages.success(self.request, '✅ Изменения сохранены (модератор)')
        else:
            messages.success(self.request, '✅ Товар успешно обновлён!')
        return super().form_valid(form)


class MyProductsView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    model = Product
    template_name = 'catalog/my_products.html'
    context_object_name = 'products'
    ordering = ['-created_at']

    def get_queryset(self):
        # Пока показываем все товары (как в MyPostsView)
        # Потом можно будет фильтровать по пользователю, если добавим авторизацию
        return Product.objects.filter(owner=self.request.user)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = 'users:login'
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:my_products')

    def test_func(self):
        """Только владелец или модератор может удалять товар"""
        product = self.get_object()
        return (
                self.request.user == product.owner or
                self.request.user.has_perm('catalog.can_unpublish_product') or
                self.request.user.is_staff
        )

    def form_valid(self, form):
        messages.success(self.request, '✅ Товар успешно удалён!')
        return super().form_valid(form)




# ==================== КОНТАКТЫ ====================

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = CompanyContacts.objects.order_by('-created_at').first()
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if not name or not phone:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
            return self.render_to_response(self.get_context_data())

        Contact.objects.create(name=name, phone=phone, message=message)
        messages.success(request, 'Ваше сообщение успешно отправлено!')
        return HttpResponseRedirect(self.request.path)

from django.views.generic import ListView
from .services import get_products_by_category

class CategoryProductsView(ListView):
    """Список всех продуктов в указанной категории"""
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)  # сервис с кешем

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')
        category_id = self.kwargs.get('category_id')
        # Можно добавить название категории
        try:
            context['category'] = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            context['category'] = None
        return context