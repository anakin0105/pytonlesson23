from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse


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
    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})