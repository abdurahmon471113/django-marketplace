from django.contrib import admin

from .models import Advertisement, Category, SavedAd, SubCategory

admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(SavedAd)
admin.site.register(SubCategory)
