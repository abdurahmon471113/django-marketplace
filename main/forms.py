from django import forms
from django.core.exceptions import ValidationError

from .models import Advertisement


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = [
            "category",
            "subcategory",
            "title",
            "price",
            "description",
            "contact_person",
            "phone",
            "email",
            "images",
        ]

        labels = {
            "category": "Категория",
            "subcategory": "Подкатегория",
            "title": "Укажите название",
            "price": "Цена",
            "description": "Описание",
            "contact_person": "Контактное лицо",
            "email": "Email-адрес",
            "phone": "Номер телефона",
            "images": "Фото",
        }

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "widget-base-dimension widget_category form-select rounded-1 border-0"
                }
            ),
            "subcategory": forms.Select(
                attrs={
                    "class": "widget-base-dimension widget_category form-select rounded-1 border-0"
                }
            ),
            "title": forms.TextInput(
                attrs={"class": "widget_title form-control rounded-1 border-dark"}
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "widget-base-dimension widget_price form-control rounded-1 border-0"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "widget_description form-control rounded-1 border-dark",
                    "rows": 4,
                }
            ),
            "contact_person": forms.TextInput(
                attrs={
                    "class": "widget-base-dimension form-control rounded-1 border-dark",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "widget-base-dimension form-control rounded-1 border-dark",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "widget-base-dimension form-control rounded-1 border-dark",
                }
            ),
            "images": forms.ClearableFileInput(
                attrs={"class": "widget_image form-control rounded-0 border-1"}
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields["email"].initial = user.email
            self.fields["email"].disabled = True

        self.fields["title"].validators.append(self.validate_title)
        self.fields["description"].validators.append(self.validate_description)
        self.fields["price"].validators.append(self.validate_price)

    def validate_title(self, value):
        if len(value) < 12:
            raise ValidationError("Название должно содержать минимум 12 символов.")

    def validate_description(self, value):
        if len(value) < 40:
            raise ValidationError("Описание должно содержать минимум 40 символов.")

    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Цена должна быть больше 0.")

    def save(self, commit=True):
        ad = super().save(commit=False)
        ad.email = self.cleaned_data["email"]

        if commit:
            ad.save()

        return ad
