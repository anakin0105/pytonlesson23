from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Создаёт группу "Контент-менеджер" с необходимыми правами'

    def handle(self, *args, **options):
        # Получаем ContentType модели BlogPost
        post_ct = ContentType.objects.get_for_model(BlogPost)

        # Создаём или получаем группу
        group, created = Group.objects.get_or_create(name='Контент-менеджер')

        if created:
            self.stdout.write(self.style.SUCCESS('✅ Группа "Контент-менеджер" создана'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Группа "Контент-менеджер" уже существует'))

        # Права для контент-менеджера
        permissions = [
            Permission.objects.get(codename='can_publish_post', content_type=post_ct),
            Permission.objects.get(codename='can_unpublish_post', content_type=post_ct),
            Permission.objects.get(codename='change_blogpost', content_type=post_ct),
            Permission.objects.get(codename='delete_blogpost', content_type=post_ct),
            Permission.objects.get(codename='add_blogpost', content_type=post_ct),
        ]

        group.permissions.add(*permissions)

        self.stdout.write(self.style.SUCCESS('✅ Права успешно назначены группе "Контент-менеджер"'))
        self.stdout.write('   • can_publish_post')
        self.stdout.write('   • can_unpublish_post')
        self.stdout.write('   • change_blogpost, delete_blogpost, add_blogpost')