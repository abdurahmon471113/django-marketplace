from django.contrib import admin

from .models import Advertisement, Category, SavedAd

admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(SavedAd)
