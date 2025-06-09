from django.contrib import admin
from .models import ITRequest

@admin.register(ITRequest)
class ITRequestAdmin(admin.ModelAdmin):
    list_display = (
        'short_description_summary',
        'category',
        'company',
        'inn',
        'fio',
        'phone',
        'email',
        'created_at',
    )
    list_filter = ('category', 'agreement', 'created_at')
    search_fields = ('short_description', 'company', 'inn', 'fio', 'email')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

    def short_description_summary(self, obj):
        return obj.short_description if len(obj.short_description) < 75 else obj.short_description[:72] + '…'
    short_description_summary.short_description = 'Описание'

