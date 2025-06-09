from django.shortcuts import render, redirect
from django.http import JsonResponse
from catalog.models import Tag
from .models import ITOffer
from .forms import ITRequestForm

def offers_view(request):
    tags = Tag.objects.all()
    form = ITRequestForm()

    # вынесем GET-параметр q
    q = request.GET.get('q', '').strip()

    # базовый QuerySet — все запросы, отсортированные по дате (последние первыми)
    qs = ITOffer.objects.order_by('-created_at')

    if q:
        # фильтруем по полю short_description (icontains — без учёта регистра)
        qs = qs.filter(short_description__icontains=q)

    total_count = ITOffer.objects.count()          # общее кол-во
    shown_count = qs.count()                         # сколько отобрано после фильтра

    # обрежем до трёх последних
    latest_requests = qs[:3]

    # обработка AJAX/POST как было у вас...
    if request.method == "POST":
        form = ITRequestForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": True})
            return redirect("offers:")  # поправьте namespace/name, если нужно
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            errors = {k: v.get_json_data() for k, v in form.errors.items()}
            return JsonResponse({"success": False, "errors": errors}, status=400)

    return render(request, "offers.html", {
        "tags":     tags,
        "form":     form,
        "requests": latest_requests,
        "count":    total_count,
        "shown":    shown_count,
        "q":        q,
    })
