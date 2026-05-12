from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Удаляет все существующие данные и загружает тестовые продукты из catalog.json'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Начинаем загрузку тестовых данных...'))

        # 1. Удаляем все существующие категории и продукты
        deleted_products = Product.objects.all().delete()
        deleted_categories = Category.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'Удалено продуктов: {deleted_products[0]}, категорий: {deleted_categories[0]}'
            )
        )

        # 2. Загружаем фикстуру
        self.stdout.write('Загружаем фикстуру catalog.json ...')

        try:
            call_command('loaddata', 'catalog.json', verbosity=2)
            self.stdout.write(self.style.SUCCESS('Фикстура успешно загружена!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке фикстуры: {e}'))
            return

        # 3. Показываем результат
        total_categories = Category.objects.count()
        total_products = Product.objects.count()

        self.stdout.write(self.style.SUCCESS(
            f'Готово! В базе теперь {total_categories} категорий и {total_products} продуктов.'
        ))

        # Дополнительно выводим список загруженных товаров
        self.stdout.write('\nЗагруженные продукты:')
        for product in Product.objects.select_related('category').all():
            self.stdout.write(
                self.style.SUCCESS(f'  • {product.name} — {product.price} ₽ ({product.category.name})')
            )