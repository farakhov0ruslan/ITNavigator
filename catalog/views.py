from django.shortcuts import render
from django.db.models import Q
from catalog.models import Tag, ITSolution, ITRequest

def solutions(request):
    """
    Представление для каталога с поддержкой:
    - только одобренных решений
    - поиска (case-insensitive)
    - фильтрации по бизнес-статусу (стартап/продукт)
    - фильтрации по тегам
    """
    # 1) Берём только одобренные
    solutions = ITSolution.objects.filter(
        moderation_status="approved"
    ).prefetch_related("tags")

    tags = Tag.objects.all()

    # 2) Параметры из GET
    q               = request.GET.get("q", "").strip()
    selected_status = request.GET.get("status", "all")
    selected_tags   = request.GET.getlist("tags")

    # 3) Поиск
    if q:
        solutions = solutions.filter(
            Q(title__icontains=q) |
            Q(short_description__icontains=q)
        )

    # 4) Фильтр по бизнес-статусу
    if selected_status in ["startup", "product"]:
        solutions = solutions.filter(status=selected_status)

    # 5) Фильтр по тегам
    if selected_tags:
        solutions = solutions.filter(
            tags__slug__in=selected_tags
        ).distinct()

    page_content = {
        "solutions":       solutions,
        "tags":            tags,
        "selected_tags":   selected_tags,
        "selected_status": selected_status,
        "search_query":    q,
    }
    return render(request, "catalog_solutions.html", {"page_content": page_content})


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

    context = {
        "requests":     qs,
        "search_query": q,
    }
    return render(request, "catalog_requests.html", context)