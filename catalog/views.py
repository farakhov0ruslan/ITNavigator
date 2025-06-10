from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from catalog.models import Tag, ITSolution, ITRequest
from django.contrib import messages
from django.views.decorators.http import require_POST
from catalog.forms import ITSolutionForm, ITRequestForm


@require_POST
def request_create(request):
    """
    Обработка POST из формы 'Создать запрос на IT-решение'.
    Доступно только авторизованным пользователям.
    """
    if not request.user.is_authenticated or request.user.profile_type != "initiator":
        print(request.user.profile_type, request.user.is_authenticated)
        messages.error(request, "Только авторизованные пользователи могут создавать запросы.")
        return redirect(reverse("catalog:requests"))

    form = ITRequestForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Ваш запрос отправлен на модерацию!")
    else:
        messages.error(request, "Ошибка при отправке запроса. Проверьте форму.")
        # Сохраняем ошибки, чтобы показать их в модалке
        request.session["request_form_errors"] = form.errors

    return redirect(reverse("catalog:requests"))


@require_POST
def solution_create(request):
    """
    Обработка POST из формы 'Предложить IT-решение'.
    Доступно только авторизованным компаниям.
    """
    # Проверка роли
    if not request.user.is_authenticated or request.user.profile_type != "company":
        messages.error(request, "Только компании могут предлагать решения.")
        return redirect(reverse("catalog:solutions"))

    form = ITSolutionForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, "Ваше решение отправлено на модерацию!")
    else:
        messages.error(request, "Ошибка при отправке решения. Проверьте форму.")
        # В идеале вы хотите сохранить ошибки в сессии или вернуть их AJAX'ом.
    return redirect(reverse("catalog:solutions"))


def solutions(request):
    """
    Представление для каталога с поддержкой:
    - только одобренных решений
    - поиска (case-insensitive)
    - фильтрации по бизнес-статусу (стартап/продукт)
    - фильтрации по тегам
    """

    solutions = ITSolution.objects.filter(
        moderation_status="approved"
    ).prefetch_related("tags")

    tags = Tag.objects.all()

    # Параметры из GET
    q = request.GET.get("q", "").strip()
    selected_status = request.GET.get("status", "all")
    selected_tags = request.GET.getlist("tags")

    # Поиск
    if q:
        solutions = solutions.filter(
            Q(title__icontains=q) |
            Q(short_description__icontains=q)
        )

    # Фильтр по бизнес-статусу
    if selected_status in ["startup", "product"]:
        solutions = solutions.filter(status=selected_status)

    # Фильтр по тегам
    if selected_tags:
        solutions = solutions.filter(
            tags__slug__in=selected_tags
        ).distinct()

    form_errors = request.session.pop("solution_form_errors", None)
    if form_errors:
        solution_form = ITSolutionForm()
        solution_form._errors = form_errors
    else:
        solution_form = ITSolutionForm()

    context = {
        "page_content": {
            "solutions": solutions,
            "tags": tags,
            "selected_tags": selected_tags,
            "selected_status": selected_status,
            "search_query": q,
        },
        "solution_form": solution_form,
    }
    return render(request, "catalog_solutions.html", context)


def requests(request):
    """
    Публичный список одобренных запросов на IT-решения с поиском.
    """
    # Берём только запросы, которые прошли модерацию
    qs = ITRequest.objects.filter(moderation_status="approved").prefetch_related("tags")


    # Параметры поиска
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(short_description__icontains=q) |
            Q(company_name__icontains=q) |
            Q(contact_name__icontains=q)
        ).distinct()

        # Подготовка формы и ошибок
    form_errors = request.session.pop("request_form_errors", None)
    if form_errors:
        request_form = ITRequestForm()
        request_form._errors = form_errors
    else:
        request_form = ITRequestForm()

    context = {
        "requests": qs,
        "search_query": q,
        "request_form": request_form,  # <-- передаём форму в шаблон
    }
    return render(request, "catalog_requests.html", context)
