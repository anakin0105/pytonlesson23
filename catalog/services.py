# catalog/services.py
from django.core.cache import cache
from catalog.models import Product, Category


def get_products_by_category(category_id: int, timeout: int = 300):
    """
    Сервисная функция для получения списка продуктов в категории.
    Использует низкоуровневое кеширование Redis.
    Ключ: category_{id}
    TTL: 5 минут (300 секунд)
    """
    cache_key = f"category_{category_id}"

    # Пытаемся достать из кеша
    products = cache.get(cache_key)

    if products is None:  # Cache miss
        products = list(
            Product.objects.filter(
                category_id=category_id,
                is_published=True
            )
            .select_related('category')
            .order_by('-created_at')
        )

        # Сохраняем в Redis
        cache.set(cache_key, products, timeout=timeout)

    return products