from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import Product, Contact, CompanyContacts
from .forms import ProductForm
from django.core.paginator import Paginator


def home(request):
    # Получаем САМЫЕ ПОСЛЕДНИЕ 5 продуктов (новые сверху)
    latest_products = Product.objects.order_by('-created_at')[:5]

    # === Вывод в консоль (как требует дополнительное задание) ===
    print("\n" + "=" * 75)
    print("ПОСЛЕДНИЕ 5 ДОБАВЛЕННЫХ ПРОДУКТОВ (из базы данных)")
    print("=" * 75)

    if latest_products.exists():
        for i, product in enumerate(latest_products, 1):
            print(f"{i:2d}. {product.name}")  # ← здесь name, а не title!
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

    # Получаем контактную информацию для блока на главной странице
    # Берём последнее отправленное сообщение или можно создать отдельную модель позже
    contact_info = Contact.objects.order_by('-created_at').first()

    context = {
        'latest_products': latest_products,
        'contact_info': contact_info,  # передаём для блока реквизитов
    }

    return render(request, 'catalog/home.html', context)


def contacts(request):
    company = CompanyContacts.objects.order_by('-created_at').first()

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if not name or not phone:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
            return render(request, 'contacts.html', {"company": company})

        Contact.objects.create(
            name=name,
            phone=phone,
            message=message
        )

        messages.success(request, 'Ваше сообщение успешно отправлено!')
        return redirect('catalog:contacts')

    return render(request, 'catalog/contacts.html', {"company": company})


def products_catalog(request):
    """Страница каталога со всеми товарами + пагинация"""
    all_products = Product.objects.all().order_by('-created_at')  # новые сверху

    # Пагинация: по 8 товаров на странице
    paginator = Paginator(all_products, 6)  # ← можно поменять на 6, 9, 12
    page_number = request.GET.get('page')  # получаем номер страницы из URL
    page_obj = paginator.get_page(page_number)  # безопасно получает текущую страницу

    context = {
        'page_obj': page_obj,  # передаём объект страницы
        'products': page_obj,  # для удобства в шаблоне
    }
    return render(request, 'catalog/products_catalog.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)   # безопасный запрос
    return render(request, 'catalog/product_detail.html', {'product': product})


def add_product(request):
    """Форма добавления нового товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # request.FILES ОБЯЗАТЕЛЬНО для фото!

        if form.is_valid():
            form.save()
            messages.success(request, '✅ Товар успешно добавлен в каталог!')
            return redirect('catalog:products_catalog')  # после добавления возвращаем в каталог
    else:
        form = ProductForm()

    return render(request, 'catalog/add_product.html', {'form': form})