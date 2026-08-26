from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("home/", views.home_view, name="home"),
    path("my-ads-list/", views.my_ads_list_view, name="my_ads"),
    path("ad-detail/<int:pk>/", views.ad_detail_view, name="ad_detail"),
    path("change-ad/<int:pk>/", views.change_ad_view, name="change_ad"),
    path("change-ad-ajax/<int:pk>/", views.change_ad_ajax_view, name="change_ad_ajax"),
    path("delete-ad/<int:pk>/", views.delete_ad_view, name="delete_ad"),
    path("delete-ad-ajax/<int:pk>/", views.delete_ad_ajax_view, name="delete_ad_ajax"),
    path("create-ad/", views.create_ad_view, name="create_ad"),
    path("save-favorite-ad/<int:pk>/", views.save_favorite_ad, name="save_favorite_ad"),
    path(
        "delete-favorite-ad/<int:pk>/",
        views.delete_favorite_ad,
        name="delete_favorite_ad",
    ),
    path("saved/", views.saved_ads_view, name="saved_ads"),
    path("archive-ad/<int:pk>/", views.archive_ad_view, name="archive_ad"),
    path("archive-ad-ajax/<int:pk>/", views.archive_ad_ajax_view, name="archive_ad_ajax"),
    path("from-archive-ajax/<int:pk>/", views.from_archive_ajax_view, name="from_archive_ajax"),

    path(
        "favorite/save-ajax/<int:pk>/",
        views.save_favorite_ad_ajax,
        name="save_favorite_ad_ajax",
    ),
    path(
        "favorite/delete-ajax/<int:pk>/",
        views.delete_favorite_ad_ajax,
        name="delete_favorite_ad_ajax",
    ),
    path("my-ads-list-ajax", views.my_ads_list_ajax_view, name="my_ads_list_ajax"),
]
