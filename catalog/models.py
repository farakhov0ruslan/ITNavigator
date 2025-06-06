from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    """
    Модель для хранения тегов.
    Например: 'Экология', 'Образование', 'Туризм' и т.д.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название тега"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True,
        verbose_name="Slug тега (для URL и CSS-классов)"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Если slug не задан явно — генерируем из name
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class ITSolution(models.Model):
    """
    Основная модель для IT-решения (стартапа/продукта).
    """
    STATUS_CHOICES = [
        ("startup", "Стартап"),
        ("product", "Продукт"),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name="Название решения"
    )
    short_description = models.CharField(
        max_length=255,
        verbose_name="Краткое описание"
    )
    description = models.TextField(
        verbose_name="Полное описание"
    )
    organization = models.CharField(
        max_length=200,
        verbose_name="Организация"
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Телефон"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="E-mail"
    )
    site = models.URLField(
        blank=True,
        verbose_name="Сайт"
    )

    image = models.ImageField(
        upload_to="itsolutions/%Y/%m/%d/",
        blank=True,
        verbose_name="Изображение/логотип"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="product",
        verbose_name="Статус"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="solutions",
        verbose_name="Теги"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения"
    )

    class Meta:
        verbose_name = "IT-решение"
        verbose_name_plural = "IT-решения"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
