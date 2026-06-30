from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AdvertisementForm
from .models import Advertisement


def home_view(request):
    return render(request, "user_app/home.html")


@login_required
def my_ads_list_view(request):
    my_ads = Advertisement.objects.filter(author=request.user)
    return render(request, "main/my_ads_list.html", {"my_ads": my_ads})


@login_required
def create_ad_view(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST, user=request.user)
        print("this is error text----", form.errors)
        if form.is_valid():
            print("for is valid----")
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect("main:my_ads")
    else:
        form = AdvertisementForm(user=request.user)

    return render(request, "main/create_ad.html", {"form": form})


@login_required
def change_ad_view(request, pk):
    print(request.user)
    print(pk)
    ad = get_object_or_404(Advertisement, pk=pk, author=request.user)
    if request.method == "POST":
        form = AdvertisementForm(request.POST, instance=ad, user=request.user)
        print(form.errors)
        print(form.data)

        if form.is_valid():
            form.save()
            return redirect("main:my_ads")

    else:
        form = AdvertisementForm(instance=ad, user=request.user)
        print(form.changed_data)


    return render(request, "main/change_ad.html", {"form": form})




"""
1. create Readme.md file and include steps how to set up project locally
2. create .env file to include db credentials
3. in home page, it should not go to /user_app/ it should open /
4. in home page list all ads created by other users, exclude ads from request user
5. use cards as in olx to display ads in home page
6. create ad details page to show ad details to user
7. add search input in home to search ads by title
8. bonus: add image handling in ad creation

"""