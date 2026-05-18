from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.conf import settings

class BlogPost(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок"
    )
    content = models.TextField(
        verbose_name="Содержимое"
    )
    preview = models.ImageField(
        upload_to='blog/previews/',
        blank=True,
        null=True,
        verbose_name="Превью"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Показать в блоге"
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров"
    )
    likes = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество лайков"
    )
    dislikes = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество дизлайков"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        null=True,
        blank=True,
        related_name="blog_posts"
    )

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ['-created_at']
        permissions = [
            ("can_publish_post", "Может публиковать статьи"),
            ("can_unpublish_post", "Может снимать статьи с публикации"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})