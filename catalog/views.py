from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Contact, CompanyContacts


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

    return render(request, 'home.html', context)


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

    return render(request, 'contacts.html', {"company": company})