# catalog/admin.py

from django.contrib import admin
from .models import Tag, ITSolution, ITRequest

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display        = ("name", "slug")
    search_fields       = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering            = ("name",)


@admin.register(ITSolution)
class ITSolutionAdmin(admin.ModelAdmin):
    list_display       = (
        "title",
        "organization",
        "status",               # стартап/продукт
        "moderation_status",    # в обработке/одобрено/отклонено
        "created_at",
    )
    list_filter        = (
        "status",
        "moderation_status",
        "tags",
        "created_at",
    )
    search_fields      = (
        "title",
        "organization",
        "short_description",
        "description",
    )
    autocomplete_fields = ("tags",)
    readonly_fields    = ("created_at", "updated_at")
    fieldsets = (
        (None, {
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
        }),
        ("Модерация", {
            "fields": ("moderation_status",),
        }),
        ("Служебная информация", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )
    actions = ("approve_solutions", "reject_solutions")

    @admin.action(description="Одобрить выбранные решения")
    def approve_solutions(self, request, queryset):
        updated = queryset.update(moderation_status="approved")
        self.message_user(request, f"{updated} решениe(й) отмечено(ы) как «Одобрено».")

    @admin.action(description="Отклонить выбранные решения")
    def reject_solutions(self, request, queryset):
        updated = queryset.update(moderation_status="rejected")
        self.message_user(request, f"{updated} решениe(й) отмечено(ы) как «Отклонено».")


@admin.register(ITRequest)
class ITRequestAdmin(admin.ModelAdmin):
    list_display       = (
        "title",
        "company_name",
        "contact_name",
        "moderation_status",
        "created_at",
    )
    list_filter        = (
        "moderation_status",
        "tags",
        "created_at",
    )
    search_fields      = (
        "title",
        "company_name",
        "contact_name",
        "email",
    )
    autocomplete_fields = ("tags",)
    readonly_fields    = ("created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": (
                "title",
                "short_description",
                "contact_name",
                "company_name",
                "inn",
                "phone",
                "email",
                "tags",
            )
        }),
        ("Модерация", {
            "fields": ("moderation_status",),
        }),
        ("Служебная информация", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )
    actions = ("approve_requests", "reject_requests")

    @admin.action(description="Одобрить выбранные запросы")
    def approve_requests(self, request, queryset):
        updated = queryset.update(moderation_status="approved")
        self.message_user(request, f"{updated} запрос(ов) отмечен(ы) как «Одобрено».")

    @admin.action(description="Отклонить выбранные запросы")
    def reject_requests(self, request, queryset):
        updated = queryset.update(moderation_status="rejected")
        self.message_user(request, f"{updated} запрос(ов) отмечен(ы) как «Отклонено».")
