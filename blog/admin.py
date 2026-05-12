from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'views', 'likes', 'dislikes', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('views', 'likes', 'dislikes', 'created_at')

    # Меняем текст кнопок действий под новое название
    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, "Статьи теперь показываются в блоге!")

    make_published.short_description = "Показать в блоге выбранные статьи"

    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, "Статьи скрыты из блога!")

    make_unpublished.short_description = "Скрыть из блога выбранные статьи"