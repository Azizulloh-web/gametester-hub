from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Список имен URL, которые доступны БЕЗ логина (логин и регистрация)
        exempt_urls = [reverse('login'), reverse('register')]

        # Если пользователь не вошел и пытается зайти на страницу, которой нет в списке исключений
        if not request.user.is_authenticated and request.path not in exempt_urls:
            return redirect('login')

        response = self.get_response(request)
        return response