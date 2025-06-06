from django.contrib import admin
from .models import Tag, ITSolution


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(ITSolution)
class ITSolutionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organization",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "tags",
        "created_at",
    )
    search_fields = (
        "title",
        "organization",
        "short_description",
        "description",
    )
    autocomplete_fields = ("tags",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "short_description",
                    "description",
                    "organization",
                    "phone",
                    "email",
                    "site",
                    "image",
                    "status",
                    "tags",
                )
            },
        ),
        (
            "Служебная информация",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
