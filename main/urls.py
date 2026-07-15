from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("home/", views.home_view, name="home"),
    path("my-ads-list/", views.my_ads_list_view, name="my_ads"),
    path("ad-detail/<int:pk>/", views.ad_detail_view, name="ad_detail"),
    path("change-ad/<int:pk>/", views.change_ad_view, name="change_ad"),
    path("delete-ad/<int:pk>/", views.delete_ad_view, name="delete_ad"),
    path("create-ad/", views.create_ad_view, name="create_ad"),
    path("save-favorite-ad/<int:pk>/", views.save_favorite_ad, name="save_favorite_ad"),
    path(
        "delete-favorite-ad/<int:pk>/",
        views.delete_favorite_ad,
        name="delete_favorite_ad",
    ),
    path("saved/", views.saved_ads_view, name="saved_ads"),
    path("archive-ad/<int:pk>/", views.archive_ad_view, name="archive_ad"),
]
