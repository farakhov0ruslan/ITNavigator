from django.contrib.auth import logout
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse


def index(request):
    return render(request, 'main.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            print(form.data)
            user = form.save()  # Сохраняем пользователя
            print(user)
            login(request, user)  # Логиним пользователя
            # Возвращаем успешный ответ с редиректом на главную страницу
            return JsonResponse({'success': True, 'redirect_url': '/'})  # Перенаправляем на главную страницу
        else:

            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list  # Собираем ошибки для каждого поля
            print(errors)
            return JsonResponse({'success': False, 'errors': errors})  # Отправляем ошибки на фронт
    else:
        form = UserRegistrationForm()

    return render(request, 'main.html', {'form': form})

def custom_logout(request):
    # Сохраняем в локальную переменную всё, что не должны терять при flush()
    routes_left = request.session.get('routes_left', 1)
    route_json = request.session.get('route')
    days_count = request.session.get('days_count', None)
    # Можно сохранить и другие ключи, если нужно:
    # some_other = request.session.get('some_other', default)

    # Разлогиниваем — по умолчанию это делает session.flush()
    logout(request)

    # Т.к. сессия уже новая, но cookie та же, сразу восстанавливаем счётчик
    request.session['routes_left'] = routes_left
    # И любые другие необходимые данные:
    if route_json is not None:
        request.session['route'] = route_json
    if days_count is not None:
        request.session['days_count'] = days_count
    # request.session['some_other'] = some_other

    return redirect('main:index')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')  # Получаем email
        password = request.POST.get('password')  # Получаем пароль

        # Аутентификация по email, а не username
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)  # Логиним пользователя
            return JsonResponse({"success": True, "redirect_url": '/'})  # Возвращаем JSON для успешного входа
        else:
            # Если аутентификация не прошла
            return JsonResponse({"success": False, "errors": {"password": "Неверные данные для входа."}})

    return render(request, 'main.html')