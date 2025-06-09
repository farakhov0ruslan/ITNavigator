# main/models.py
from django.db import models
from django.utils import timezone
from catalog.models import Tag

class ITRequest(models.Model):
    short_description = models.TextField(
        verbose_name="Краткое описание"
    )
    category = models.ForeignKey(
        Tag,
        on_delete=models.PROTECT,
        verbose_name="Категория"
    )
    company = models.CharField(
        max_length=255,
        verbose_name="Компания / ИП"
    )
    inn = models.CharField(
        max_length=20,
        verbose_name="ИНН"
    )
    agreement = models.BooleanField(
        verbose_name="Согласие на обработку данных"
    )
    fio = models.CharField(
        max_length=200,
        verbose_name="ФИО"
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон"
    )
    email = models.EmailField(
        verbose_name="E-mail"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата подачи"
    )

    class Meta:
        verbose_name = "Запрос на ИТ-решение"
        verbose_name_plural = "Запросы на ИТ-решения"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.short_description[:50]}… ({self.created_at:%d.%m.%Y})"
