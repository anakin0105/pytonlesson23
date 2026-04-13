from django.views.generic import (
    ListView, DetailView, CreateView, TemplateView
)
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .models import Product, CompanyContacts, Contact
from .forms import ProductForm


# ==================== ПРОДУКТЫ ====================

class HomePageView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.order_by('-created_at')[:5]

        # === Дополнительное задание: вывод в консоль ===
        print("\n" + "=" * 75)
        print("ПОСЛЕДНИЕ 5 ДОБАВЛЕННЫХ ПРОДУКТОВ (из базы данных)")
        print("=" * 75)
        latest = context['latest_products']
        if latest.exists():
            for i, product in enumerate(latest, 1):
                print(f"{i:2d}. {product.name}")
                print(f"     Цена: {product.price} ₽")
                print(f"     Создан: {product.created_at.strftime('%d.%m.%Y')}")
                if product.category:
                    print(f"     Категория: {product.category.name}")
                if product.description:
                    print(f"     Описание: {product.description[:80]}...")
                print("-" * 70)
        else:
            print("⚠️  В базе данных пока нет продуктов.")
        print("=" * 75 + "\n")

        return context


class ProductsCatalogView(ListView):
    model = Product
    template_name = 'catalog/products_catalog.html'
    context_object_name = 'page_obj'   # важно для пагинации
    paginate_by = 6
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = context['page_obj']   # для совместимости с шаблоном
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:products_catalog')

    def form_valid(self, form):
        messages.success(self.request, '✅ Товар успешно добавлен в каталог!')
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