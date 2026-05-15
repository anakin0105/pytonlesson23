from django.contrib.auth.models import AbstractUser,  BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        blank=True,
        default='',
        unique=False,
        verbose_name="Имя пользователя"
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("Пользователь с таким email уже существует."),
        }
    )

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефона")
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="Страна")
    token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Token")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # ← убрали username

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


from secrets import token_hex
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import UserRegisterForm
from .models import CustomUser


class UserCreateView(CreateView):
    """Регистрация пользователя с подтверждением email"""

    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Делаем неактивным до подтверждения
        user.token = token_hex(16)  # Генерируем токен
        user.save()

        # Формируем ссылку для подтверждения
        host = self.request.get_host()
        confirmation_url = f'http://{host}/users/email_confirm/{user.token}/'

        # Письмо с подтверждением email
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
            'Регистрация почти завершена! Проверьте вашу почту и подтвердите email.'
        )

        return super().form_valid(form)


def email_verification(request, token):
    """Подтверждение email и отправка приветственного письма"""
    user = get_object_or_404(CustomUser, token=token)

    if not user.is_active:
        user.is_active = True
        user.token = None  # Очищаем токен после использования
        user.save()

        # Отправляем приветственное письмо после подтверждения
        send_mail(
            subject='Добро пожаловать в Skystore!',
            message=f"""Здравствуйте, {user.get_full_name()}!

Спасибо, что подтвердили email и присоединились к Skystore!

Теперь вы можете:
• Добавлять и редактировать товары
• Писать статьи в блоге
• Управлять своим профилем

Приятного использования!

С уважением,
Команда Skystore""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(request, 'Email успешно подтверждён! Добро пожаловать в Skystore!')

    return redirect(reverse('users:login'))