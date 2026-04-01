from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Contact


def home(request):
    # Лучшая практика: явно указываем сортировку и фильтр
    latest_products = Product.objects.order_by('-created_at')[:5]

    # Вывод в консоль (как требует задание)
    print("\n" + "=" * 60)
    print("ПОСЛЕДНИЕ 5 ДОБАВЛЕННЫХ ПРОДУКТОВ")
    print("=" * 60)

    if latest_products.exists():
        for i, product in enumerate(latest_products, 1):
            print(f"{i:2d}. {product.name}")
            print(f"     Цена: ${product.price}")
            print(f"     Создан: {product.created_at.strftime('%d.%m.%Y')}")
            if product.category:
                print(f"     Категория: {product.category.name}")
            print("-" * 50)
    else:
        print("⚠️  В базе данных пока нет продуктов.")

    print("=" * 60 + "\n")

    context = {
        'latest_products': latest_products,
    }
    return render(request, 'home.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if not name or not phone:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
            return render(request, 'contacts.html')

        Contact.objects.create(
            name=name,
            phone=phone,
            message=message
        )

        messages.success(request, 'Ваше сообщение успешно отправлено!')
        return redirect('catalog:contacts')  # используем пространство имён

    return render(request, 'contacts.html')