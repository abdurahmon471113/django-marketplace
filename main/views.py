from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Advertisement
from .forms import AdvertisementForm








def home_view(request):
    return render(request, 'user_app/home.html')



@login_required
def my_ads_list_view(request):
    my_ads = Advertisement.objects.filter(author=request.user)
    return render(request, 'main/my_ads_list.html', {'my_ads': my_ads})



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
            return redirect('main:my_ads')
    else:
        form = AdvertisementForm(user=request.user)

    return render(request, 'main/create_ad.html', {'form': form})



@login_required
def change_ad_view(request, pk):
    print(request.user)
    print(pk)
    ad = get_object_or_404(Advertisement, pk=pk, author=request.user)
    if request.method == "POST":
        form = AdvertisementForm(request.POST, instance=ad)
        print(form.data)
        print(form.errors)

        if form.is_valid():
            form.save()
            return redirect("main:my_ads")

    else:
        form = AdvertisementForm(instance=ad)

    return render(request, "main/change_ad.html", {"form": form})




   



