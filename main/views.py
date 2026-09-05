import json

from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Q, Subquery
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from .choices import StatusChoices
from .forms import AdvertisementForm
from .models import Advertisement, Category, SavedAd


@login_required
def my_ads_list_view(request):

    current_status = request.GET.get("status", StatusChoices.ACTIVE)

    my_ads = Advertisement.objects.filter(
        author=request.user, status=current_status
    ).order_by("-created_at")

    return render(
        request,
        "main/my-ads-list.html",
        {"my_ads": my_ads, "current_status": current_status},
    )


# Tested function
@login_required
def my_ads_list_ajax_view(request):

    if request.method != "GET":
        return JsonResponse({
            "status": "error",
            "message": "Only GET requests are allowed"
        }, status=405)


    current_status = request.GET.get(
        "status",
        StatusChoices.ACTIVE
    )


    my_ads = Advertisement.objects.filter(
        author=request.user,
        status=current_status
    ).order_by("-created_at")



    content_html = render_to_string(
        "main/partials/my-ads-content.html",
        {
            "my_ads": my_ads,
            "current_status": current_status,
        },
        request=request
    )


    return JsonResponse({
        "status": "success",
        "content": content_html,
    })



@login_required
def archive_ad_view(request, pk):
    ad = get_object_or_404(Advertisement, author=request.user, pk=pk)
    if ad.status == StatusChoices.ACTIVE:
        ad.status = StatusChoices.ARCHIVED
        ad.save()
    else:
        ad.status = StatusChoices.ACTIVE
        ad.save()
    return redirect("main:my_ads")


# Tested function
@login_required
def archive_ad_ajax_view(request, pk):

    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Only POST requests are allowed",
        }, status=405)

    ad = get_object_or_404(
        Advertisement,
        author=request.user,
        pk=pk
    )

    if ad.status == StatusChoices.ACTIVE:
        ad.status = StatusChoices.ARCHIVED
        ad.save()

    return JsonResponse({
        "status": "success",
        "message": "Объявление добавлено в архив",
        "ad_id": pk,
    })


# Tested function
@login_required
def from_archive_ajax_view(request, pk):
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Only POST requests are allowed",
        }, status=405)

    ad = get_object_or_404(
        Advertisement,
        author=request.user,
        pk=pk
    )

    if ad.status == StatusChoices.ARCHIVED:
        ad.status = StatusChoices.ACTIVE
        ad.save()

    return JsonResponse({
        "status": "success",
        "message": "Объявление выведено из архива",
        "ad_id": pk,
    })
    










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
    catg = Category.objects.filter(parent=None)
    if request.method == "POST":
        print("POST:", request.POST)
        form = AdvertisementForm(
            request.POST,
            request.FILES,
            user=request.user,
        )

        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.email = request.user.email
            ad.save()

            return redirect("main:my_ads")

    else:
        form = AdvertisementForm(user=request.user)

    return render(request, "main/create-ad.html", {"form": form, "catg": catg})


@login_required
def change_ad_view(request, pk):
    catg = Category.objects.filter(parent=None)
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

    return render(request, "main/change-ad.html", {"form": form, "catg": catg})



# Tested function
@login_required
def change_ad_ajax_view(request, pk):

    catg = Category.objects.filter(parent=None)

    ad = get_object_or_404(
        Advertisement,
        pk=pk,
        author=request.user
    )


    # =========================================================
    # GET — показать форму
    # =========================================================

    if request.method == "GET":

        form = AdvertisementForm(
            instance=ad,
            user=request.user
        )


        edit_form = render_to_string(
            "main/partials/change-ad-only-form.html",
            {
                "form": form,
                "catg": catg,
                "ad": ad,
            },
            request=request
        )


        return JsonResponse({
            "status": "success",
            "edit": edit_form,
        })


    # =========================================================
    # POST — сохранить
    # =========================================================

    if request.method == "POST":

        form = AdvertisementForm(
            request.POST,
            request.FILES,
            instance=ad,
            user=request.user
        )


        if form.is_valid():

            ad = form.save()


            # ВАЖНО:
            # берём статус уже ПОСЛЕ сохранения

            current_status = ad.status


            # Берём ТОЛЬКО объявления
            # с этим статусом

            my_ads = Advertisement.objects.filter(
                author=request.user,
                status=current_status
            ).order_by("-created_at")


            # Возвращаем статусы + карточки

            content_html = render_to_string(
                "main/partials/my-ads-content.html",
                {
                    "my_ads": my_ads,
                    "current_status": current_status,
                },
                request=request
            )


            return JsonResponse({
                "status": "success",
                "content": content_html,
            })


        # =====================================================
        # Ошибка формы
        # =====================================================

        edit_form = render_to_string(
            "main/partials/change-ad-only-form.html",
            {
                "form": form,
                "catg": catg,
                "ad": ad,
            },
            request=request
        )


        return JsonResponse({
            "status": "error",
            "edit": edit_form,
        }, status=400)



    return JsonResponse({
        "status": "error",
        "message": "Only GET and POST requests are allowed",
    }, status=405)




@login_required
def delete_ad_view(request, pk):
    my_ads = Advertisement.objects.filter(author=request.user, pk=pk)
    my_ads.delete()
    return redirect(reverse("main:my_ads") + "?status=waiting")


# Tested function
@login_required
def delete_ad_ajax_view(request, pk):
    if request.method == "POST":

        ad = get_object_or_404(
            Advertisement,
            pk=pk,
            author=request.user
        )


        ad.delete()


        return JsonResponse({
            "status": "success",
            "message": "Объявление удалено",
            "ad_id": pk,
        })

    return JsonResponse({
        "status": "error",
        "message": "Only POST requests are allowed",
    }, status=405)


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



# Tested function
@login_required
def save_favorite_ad_ajax(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "Успешно добавлено")
            user = request.user
            ad = get_object_or_404(Advertisement, pk=pk)
            SavedAd.objects.get_or_create(user=user, advertisement=ad)

            response_data = {"status": "success", "received_message": message}
            print("Всё успешно сработало----", response_data)
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}, status=400
            )

    return JsonResponse(
        {"status": "error", "message": "Only POST requests allowed"}, status=405
    )


@login_required
def delete_favorite_ad_ajax(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "Успешно удалено")

            user = request.user
            ad = get_object_or_404(Advertisement, pk=pk)
            delete_ad = SavedAd.objects.filter(user=user, advertisement=ad)
            delete_ad.delete()

            response_data = {"status": "success", "received_message": message}
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}, status=400
            )

    return JsonResponse(
        {"status": "error", "message": "Only POST requests allowed"}, status=405
    )

