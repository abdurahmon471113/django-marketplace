from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("my_ads_list/", views.my_ads_list_view, name="my_ads"),
    path("change_ad/<int:pk>/", views.change_ad_view, name="change_ad"),
    path("create_ad/", views.create_ad_view, name="create_ad"),
]
