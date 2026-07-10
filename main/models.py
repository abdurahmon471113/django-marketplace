from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from main.choices import StatusChoices


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Advertisement(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(
        max_length=250, choices=StatusChoices.choices, default=StatusChoices.ACTIVE
    )
    images = models.ImageField(upload_to="images/", blank=True, null=True)

    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.title


class SavedAd(BaseModel):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.id}) {self.user.email} user saved ad {self.advertisement.id}"
