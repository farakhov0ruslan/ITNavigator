# catalog/forms.py
from django import forms
from catalog.models import ITSolution, ITRequest, Tag


class ITSolutionForm(forms.ModelForm):
    # Используем отдельное поле для выбора одной категории (тега),
    # так как в модели ITSolution tags — ManyToManyField.
    category = forms.ModelChoiceField(
        queryset=Tag.objects.all(), required=True, label="Категория",
        widget=forms.Select(attrs={"class": "form-select bg-secondary text-white"})
    )

    class Meta:
        model = ITSolution
        # Не включаем поля status и moderation_status (используются значения по умолчанию),
        # а также description (заполним автоматически из короткого описания).
        fields = [
            "title", "short_description",
            "organization", "phone", "email", "site",
            "image",  # изображение/логотип
            # tags не включаем напрямую
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Название решения"
            }),
            "short_description": forms.Textarea(attrs={
                "class": "form-control bg-secondary text-white", "rows": 3,
                "placeholder": "Пожалуйста, дайте краткое описание решения"
            }),
            "organization": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Укажите название компании или ИП"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Пожалуйста, укажите контактный номер"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Пожалуйста, укажите адрес электронной почты"
            }),
            "site": forms.URLInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Сайт (не обязательно)",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control bg-secondary text-white"
            }),
        }
        labels = {
            "title": "Название решения",
            "short_description": "Краткое описание",
            "organization": "Компания / ИП",
            "phone": "Телефон",
            "email": "E-mail",
            "site": "Сайт",
            "image": "Изображение/логотип",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Поле title не было в исходном дизайне формы, делаем его необязательным:
        self.fields["title"].required = False
        # Поле site не обязательное
        self.fields["site"].required = False

    def save(self, commit=True):
        """Переопределяем save, чтобы заполнить описание и tags."""
        instance = super().save(commit=False)
        # Если у решения нет заголовка, используем короткое описание (обрезанное до 200 символов)
        if not instance.title:
            instance.title = instance.short_description[:200]
        # Заполняем обязательное поле description контентом короткого описания (или пустой строкой, если требуется)
        instance.description = instance.short_description
        if commit:
            instance.save()
            # Сохраняем выбранную категорию как тег
            category_tag = self.cleaned_data.get("category")
            if category_tag:
                instance.tags.set([category_tag])
            else:
                instance.tags.clear()
        return instance


class ITRequestForm(forms.ModelForm):
    # Аналогично, используем отдельное поле для категории (тега)
    category = forms.ModelChoiceField(
        queryset=Tag.objects.all(), required=True, label="Категория",
        widget=forms.Select(attrs={"class": "form-select bg-secondary text-white"})
    )

    class Meta:
        model = ITRequest
        # Поле moderation_status не включаем (используется значение по умолчанию).
        fields = [
            "title", "short_description",
            "company_name", "inn", "contact_name",
            "phone", "email",
            # tags не включаем напрямую
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Заголовок запроса"
            }),
            "short_description": forms.Textarea(attrs={
                "class": "form-control bg-secondary text-white", "rows": 3,
                "placeholder": "Опишите, какое решение вы ищете (кратко)"
            }),
            "company_name": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Укажите название компании или ИП"
            }),
            "inn": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Укажите ИНН"
            }),
            "contact_name": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "ФИО контактного лица"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Контактный телефон"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Адрес электронной почты"
            }),
        }
        labels = {
            "title": "Заголовок запроса",
            "short_description": "Краткое описание",
            "company_name": "Компания / ИП",
            "inn": "ИНН",
            "contact_name": "Контактное лицо (ФИО)",
            "phone": "Телефон",
            "email": "E-mail",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если заголовок не хотят заполнять вручную, можно сделать его не обязательным:
        self.fields["title"].required = False

    def save(self, commit=True):
        """Сохраняем запрос, устанавливая заголовок и тег."""
        instance = super().save(commit=False)
        # Если заголовок не указан, берем первые 200 символов короткого описания
        if not instance.title:
            instance.title = instance.short_description[:200]
        if commit:
            instance.save()
            # Сохраняем выбранную категорию как тег запроса
            category_tag = self.cleaned_data.get("category")
            if category_tag:
                instance.tags.set([category_tag])
            else:
                instance.tags.clear()
        return instance
