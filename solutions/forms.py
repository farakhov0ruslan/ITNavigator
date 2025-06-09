from django import forms
from .models import ITRequest

class ITRequestForm(forms.ModelForm):
    class Meta:
        model = ITRequest
        fields = [
            "short_description",
            "category",
            "company", "inn",
            "agreement",
            "fio",
            "phone", "email"
        ]
        widgets = {
            "short_description": forms.Textarea(attrs={
                "class": "form-control bg-secondary text-white",
                "rows": 3,
                "placeholder": "Пожалуйста, дайте краткое описание решения"
            }),
            "category": forms.Select(attrs={
                "class": "form-select bg-secondary text-white"
            }),
            "company": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Укажите название компании или ИП"
            }),
            "inn": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Укажите ИНН"
            }),
            "agreement": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "fio": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Пожалуйста, укажите ФИО"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Пожалуйста, укажите контактный номер"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control bg-secondary text-white",
                "placeholder": "Пожалуйста, укажите адрес электронной почты"
            }),
        }
        labels = {
            "short_description": "Краткое описание",
            "category": "Категория",
            "company": "Компания / ИП",
            "inn": "ИНН",
            "agreement": "Согласие на обработку персональных данных",
            "fio": "ФИО",
            "phone": "Телефон",
            "email": "E-mail",
        }
