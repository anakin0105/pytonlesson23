from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает ей необходимые права'

    def handle(self, *args, **options):
        # Получаем ContentType модели Product
        product_ct = ContentType.objects.get_for_model(Product)

        # Создаём или получаем группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('✅ Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Группа "Модератор продуктов" уже существует'))

        # Права
        permissions = [
            Permission.objects.get(codename='can_unpublish_product', content_type=product_ct),
            Permission.objects.get(codename='delete_product', content_type=product_ct),
            # Дополнительно даём право на изменение (на всякий случай)
            Permission.objects.get(codename='change_product', content_type=product_ct),
        ]

        group.permissions.add(*permissions)

        self.stdout.write(self.style.SUCCESS('✅ Права успешно назначены группе "Модератор продуктов"'))
        self.stdout.write('   • can_unpublish_product')
        self.stdout.write('   • delete_product')
        self.stdout.write('   • change_product')