from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AdvertisementForm
from .models import Advertisement, SavedAd


@login_required
def my_ads_list_view(request):
    my_ads = Advertisement.objects.filter(author=request.user).order_by("-created_at")
    ads_count = my_ads.count()
    return render(
        request, "main/my-ads-list.html", {"my_ads": my_ads, "ads_count": ads_count}
    )


@login_required
def ad_detail_view(request, pk):
    ad = Advertisement.objects.get(pk=pk)
    is_already_in_saved = SavedAd.objects.filter(user=request.user, advertisement=ad)
    return render(
        request,
        "main/ad_detail.html",
        {"ad": ad, "is_already_in_saved": is_already_in_saved},
    )


@login_required
def create_ad_view(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.email = request.user.email
            ad.save()

            return redirect("main:my_ads")

    else:
        form = AdvertisementForm(user=request.user)

    return render(request, "main/create_ad.html", {"form": form})


@login_required
def change_ad_view(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk, author=request.user)
    if request.method == "POST":
        form = AdvertisementForm(
            request.POST, request.FILES, instance=ad, user=request.user
        )
        print(request.FILES)

        if form.is_valid():
            form.save()
            return redirect("main:my_ads")

    else:
        form = AdvertisementForm(instance=ad, user=request.user)

    return render(request, "main/change_ad.html", {"form": form})


@login_required
def delete_ad_view(request, pk):
    my_ads = Advertisement.objects.filter(author=request.user, pk=pk)
    my_ads.delete()
    return redirect("main:my_ads")


def home_view(request):
    others = Advertisement.objects.all()
    query = request.GET.get("q")
    if request.user.is_authenticated:
        others = others.exclude(author=request.user)

    if query:
        others = others.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    return render(request, "main/home.html", {"others": others})


@login_required
def saved_ads_view(request):
    ad_ids = SavedAd.objects.filter(user=request.user).values_list("advertisement__id")
    print("ad_ids", ad_ids)
    ads = Advertisement.objects.filter(id__in=ad_ids)
    return render(request, "main/favorites.html", {"ads": ads})


@login_required
def save_favorite_ad(request, pk):
    if request.method == "POST":
        user = request.user
        ad = get_object_or_404(Advertisement, pk=pk)
        SavedAd.objects.create(user=user, advertisement=ad)
        return redirect("main:ad_detail", pk=pk)


@login_required
def delete_favorite_ad(request, pk):
    if request.method == "POST":
        user = request.user
        ad = get_object_or_404(Advertisement, pk=pk)
        delete_ad = SavedAd.objects.filter(user=user, advertisement=ad)
        delete_ad.delete()
        return redirect("main:ad_detail", pk=pk)
