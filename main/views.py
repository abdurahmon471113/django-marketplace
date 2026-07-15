from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Q, Subquery
from django.shortcuts import get_object_or_404, redirect, render

from .choices import StatusChoices
from .forms import AdvertisementForm
from .models import Advertisement, SavedAd, SubCategory


@login_required
def my_ads_list_view(request):
    status = request.GET.get("status", StatusChoices.ACTIVE)
    print("Текущий статус----", request.GET)
    my_ads = Advertisement.objects.filter(author=request.user, status=status).order_by(
        "-created_at"
    )
    ads_count = my_ads.count()
    print("Кол-во объявлений---", ads_count)
    return render(
        request,
        "main/my-ads-list.html",
        {"my_ads": my_ads, "ads_count": ads_count, "current_status": status},
    )


@login_required
def archive_ad_view(request, pk):
    ad = get_object_or_404(Advertisement, author=request.user, pk=pk)
    if ad.status == StatusChoices.ACTIVE:
        ad.status = StatusChoices.ARCHIVED
        ad.save()
        print("После клика изм с ACTIVE на ARCHIVED---", ad)
    else:
        ad.status = StatusChoices.ACTIVE
        ad.save()
    return redirect("main:my_ads")


@login_required
def ad_detail_view(request, pk):
    ad = Advertisement.objects.get(pk=pk)
    is_already_in_saved = SavedAd.objects.filter(user=request.user, advertisement=ad)
    return render(
        request,
        "main/ad-detail.html",
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

    return render(request, "main/create-ad.html", {"form": form})


@login_required
def change_ad_view(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk, author=request.user)
    if request.method == "POST":
        form = AdvertisementForm(
            request.POST, request.FILES, instance=ad, user=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("main:my_ads")

    else:
        form = AdvertisementForm(instance=ad, user=request.user)

    return render(request, "main/change-ad.html", {"form": form})


@login_required
def delete_ad_view(request, pk):
    my_ads = Advertisement.objects.filter(author=request.user, pk=pk)
    my_ads.delete()
    return redirect("main:my_ads")


def home_view(request):
    ads = Advertisement.objects.filter(status=StatusChoices.ACTIVE)
    query = request.GET.get("q")
    if request.user.is_authenticated:
        ads = ads.exclude(author=request.user)

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if not request.user.is_authenticated:
        return render(request, "main/home.html", {"ads": ads})

    is_already_in_saved = SavedAd.objects.filter(
        user=request.user, advertisement=OuterRef("pk")
    ).values("id")[:1]

    ads = ads.annotate(is_already_in_saved=Subquery(is_already_in_saved))
    return render(request, "main/home.html", {"ads": ads})


@login_required
def saved_ads_view(request):
    ad_ids = SavedAd.objects.filter(user=request.user).values_list(
        "advertisement__id", flat=True
    )
    ads = Advertisement.objects.filter(id__in=ad_ids)
    return render(request, "main/favorites.html", {"ads": ads})


@login_required
def save_favorite_ad(request, pk):
    if request.method == "POST":
        redirect_to = request.POST.get("redirect_to")
        user = request.user
        ad = get_object_or_404(Advertisement, pk=pk)
        SavedAd.objects.create(user=user, advertisement=ad)
        if redirect_to == "home" or redirect_to == "favorites":
            return redirect(f"main:{redirect_to}")
        return redirect(f"main:{redirect_to}", pk=pk)


@login_required
def delete_favorite_ad(request, pk):
    if request.method == "POST":
        redirect_to = request.POST.get("redirect_to")
        user = request.user
        ad = get_object_or_404(Advertisement, pk=pk)
        delete_ad = SavedAd.objects.filter(user=user, advertisement=ad)
        delete_ad.delete()
        if redirect_to == "home" or redirect_to == "saved_ads":
            return redirect(f"main:{redirect_to}")
        return redirect(f"main:{redirect_to}", pk=pk)
