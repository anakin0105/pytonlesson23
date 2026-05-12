from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import BlogPostForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import BlogPost


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)



class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save(update_fields=['views'])

        if self.object.views == 5:
            print(f"🎉 Поздравляем! Статья '{self.object.title}' достигла 100 просмотров! На почту направлено сообщение")
            send_mail(
                subject=f'🎉 Статья достигла 100 просмотров!',
                message=f'Поздравляем! Статья "{self.object.title}" набрала 100 просмотров.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.NOTIFICATION_EMAIL],
            )

        return self.object

class BlogCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm  # вместо fields = [...]
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        form.instance.is_published = False
        response = super().form_valid(form)
        messages.success(
            self.request,
            '✅ Статья успешно отправлена на модерацию! '
            'После проверки она появится в блоге.'
        )
        return response


class BlogUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm  # вместо fields = [...]
    template_name = 'blog/blog_form.html'

    def get_success_url(self):
        messages.success(self.request, '✅ Статья успешно обновлена!')
        return reverse('blog:blog_detail', args=[self.object.pk])


class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')

def like_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.likes += 1
    post.save(update_fields=['likes'])
    messages.success(request, 'Спасибо за лайк! 👍')
    return redirect('blog:blog_detail', pk=pk)


def dislike_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.dislikes += 1
    post.save(update_fields=['dislikes'])
    messages.success(request, 'Спасибо за отзыв! 👎')
    return redirect('blog:blog_detail', pk=pk)

class MyPostsView(ListView):
    model = BlogPost
    template_name = 'blog/my_posts.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        # Пока показываем все статьи. Позже можно будет фильтровать по пользователю
        return BlogPost.objects.all()