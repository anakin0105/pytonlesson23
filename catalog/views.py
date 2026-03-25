from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        # Здесь можно отправить email или сохранить в БД позже
        messages.success(request, f'Спасибо, {name}! Сообщение отправлено.')
        return redirect('catalog:contacts') # или 'home'
    return render(request, 'contacts.html')