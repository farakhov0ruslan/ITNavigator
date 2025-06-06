from django.shortcuts import render
from catalog.models import Tag, ITSolution

def catalog_view(request):
    """
    Демонстрационное представление.
    Вместо «заглушек» solutions / tags подключите реальные модели.
    """
    # qs = ITSolution.objects.all().prefetch_related("tags")
    # q = request.GET.get("q")
    # if q:
    #     qs = qs.filter(title__icontains=q)  # или по любым другим полям
    #
    # selected_tags = request.GET.getlist("tags")
    # if selected_tags:
    #     qs = qs.filter(tags__slug__in=selected_tags).distinct()
    #
    # status = request.GET.get("statusOptions")
    # if status and status != "all":
    #     qs = qs.filter(status=status)
    #
    # solutions = qs

    solutions = ITSolution.objects.all()
    tags = Tag.objects.all()

    # ─── Контекст, который передаём в шаблон ───────────────────────────────────
    content = {
        "solutions": solutions,
        "tags": tags,
    }
    return render(request, "catalog.html", {"page_content": content})
