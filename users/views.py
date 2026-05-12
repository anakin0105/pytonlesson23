# users/views.py
from secrets import token_hex
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import UserRegisterForm
from .models import CustomUser
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from .models import CustomUser


class UserCreateView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Делаем неактивным
        user.token = token_hex(32)  # Генерируем токен
        user.save()

        # Формируем ссылку подтверждения
        host = self.request.get_host()
        confirmation_url = f'http://{host}/users/email_confirm/{user.token}/'

        # Отправляем письмо с подтверждением
        send_mail(
            subject='Подтверждение регистрации в Skystore',
            message=f"""Здравствуйте!

Для завершения регистрации перейдите по ссылке:
{confirmation_url}

Если вы не регистрировались — просто проигнорируйте это письмо.

С уважением,
Команда Skystore""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(
            self.request,
            '✅ Регистрация почти завершена! Проверьте вашу почту и подтвердите email.'
        )

        return super().form_valid(form)


def email_verification(request, token):
    """Подтверждение email"""
    user = get_object_or_404(CustomUser, token=token)

    if not user.is_active:
        user.is_active = True
        user.token = None  # Очищаем токен
        user.save()

        messages.success(request, '✅ Email успешно подтверждён! Теперь вы можете войти в аккаунт.')

    return redirect(reverse('users:login'))