from django.shortcuts import render
from django.db.models import Q
from catalog.models import Tag, ITSolution

def catalog_view(request):
    """
    Представление для каталога с поддержкой:
    - поиска (case-insensitive)
    - фильтрации по тегам
    - фильтрации по статусу
    """
    # Базовый queryset всех решений, сразу предзагружаем теги, чтобы не было N+1
    solutions = ITSolution.objects.all().prefetch_related("tags")
    tags = Tag.objects.all()

    # Параметры из GET
    q = request.GET.get("q", "").strip()
    selected_status = request.GET.get("status", "all")
    selected_tags = request.GET.getlist("tags")

    # 1. Поиск (case-insensitive: __icontains)
    if q:
        print(q)
        solutions = solutions.filter(
            Q(title__icontains=q) |
            Q(short_description__icontains=q)
        )

    # 2. Фильтр по статусу
    if selected_status in ["startup", "product"]:
        solutions = solutions.filter(status=selected_status)

    # 3. Фильтр по тегам
    if selected_tags:
        solutions = solutions.filter(tags__slug__in=selected_tags).distinct()

    # Контекст для шаблона
    page_content = {
        "solutions": solutions,
        "tags": tags,
        "selected_tags": selected_tags,
        "selected_status": selected_status,
        "search_query": q,
    }
    return render(request, "catalog.html", {"page_content": page_content})
