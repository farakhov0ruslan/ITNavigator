from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    profile_type = forms.ChoiceField(
        label="Тип профиля",
        choices=CustomUser.PROFILE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial='guest'
    )

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com',
        })
    )

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'username',
            'profile_type',
            'password1',
            'password2',
        ]

    def clean_username(self):
        # Просто возвращаем введённое значение без проверки уникальности
        return self.cleaned_data.get('username')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Сохраняем email как идентификатор
        if commit:
            user.save()
        return user
