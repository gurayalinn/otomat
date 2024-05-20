import os
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader, RequestContext
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, never_cache, cache_control
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.contrib.auth.views import LoginView, LogoutView
from collections import defaultdict
from django.views.generic.edit import CreateView
import core.models as core_models
import core.forms as core_forms
import uuid


class HomePageView(TemplateView):
    template_name = "home.html"


class LoginPageView(TemplateView):
    template_name = "registration/login.html"


class RegisterView(CreateView):
    form_class = core_forms.RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class PasswordChanePageView(TemplateView):
    template_name = "password_change.html"


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def sira_urun_sil(request, slug, pk):
    sira_urun = get_object_or_404(core_models.OtomatUrun, pk=pk)
    sira = sira_urun.sira
    sira_urun.delete()
    return redirect("sira", slug=slug)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def sira_urun_ekle(request, slug):
    urunler_listesi = core_models.Urun.objects.all()
    sira = get_object_or_404(core_models.OtomatSira, slug=slug)

    if request.method == "POST":
        secilen_urun = core_models.Urun.objects.get(pk=request.POST["urun"])
        sira_urun = core_models.OtomatUrun(urun=secilen_urun, sira=sira)
        sira_urun.save()
        return redirect("sira", slug=sira.slug)
    return render(request, "sira.html", {"sira": sira, "tum_urunler": urunler_listesi})


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def sira_sil(request, pk):
    sira = get_object_or_404(core_models.OtomatSira, pk=pk)
    sira.delete()
    return redirect("otomat_detay", slug=sira.otomat.slug)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def sira(request, slug):
    sira = get_object_or_404(core_models.OtomatSira, slug=slug)
    sira_urunler = core_models.OtomatUrun.objects.filter(sira=sira)
    urunler_listesi = core_models.Urun.objects.all()
    otomat_siralari = core_models.OtomatSira.objects.filter(
        otomat=sira.otomat
    ).order_by("sira_harf", "sira_no")

    context = {
        "sira": sira,
        "sira_urunler": sira_urunler,
        "tum_urunler": urunler_listesi,
        "otomat_siralari": otomat_siralari,
    }
    return render(request, "sira.html", context)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def sira_duzenle(request, pk):
    sira = get_object_or_404(core_models.OtomatSira, pk=pk)
    if request.method == "POST":
        kapasite = request.POST["kapasite"]
        sira_no = request.POST["sira_no"]
        sira_harf = request.POST["sira_harf"]
        sira.kapasite = kapasite
        sira.sira_no = sira_no
        sira.sira_harf = sira_harf
        sira.save()
        return redirect("sira", slug=sira.slug)
    return render(request, "sira.html", {"sira": sira})


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def otomat_sira_ekle(request, slug):
    otomat = get_object_or_404(core_models.Otomat, slug=slug)
    if request.method == "POST":
        otomat = core_models.Otomat.objects.get(pk=request.POST["otomat"])
        kapasite = request.POST["kapasite"]
        sira_harf = request.POST["sira_harf"]
        sira_no = request.POST["sira_no"]
        sira = core_models.OtomatSira(
            otomat=otomat, kapasite=kapasite, sira_harf=sira_harf, sira_no=sira_no
        )
        sira.save()
        return redirect("otomat_detay", slug=otomat.slug)
    return render(request, "otomat.html", {"otomat": otomat})


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def otomatlar(request):

    otomats = core_models.Otomat.objects.all()

    context = {
        "otomatlar": otomats,
    }

    return render(request, "otomatlar.html", context)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def otomat_detay(request, slug):
    otomat = get_object_or_404(core_models.Otomat, slug=slug)
    urunler_listesi = core_models.Urun.objects.all()
    otomat_siralari = core_models.OtomatSira.objects.filter(otomat=otomat).order_by(
        "sira_harf", "sira_no"
    )
    toplam_kapasite = 0
    sira_urunler = []
    for sira in otomat_siralari:
        tum_urunler = core_models.OtomatUrun.objects.filter(sira=sira)
        toplam_kapasite += sira.kapasite
        unique_urunler = {}
        for urun in tum_urunler:
            key = (urun.urun.kategori, urun.urun.ad)
            if key in unique_urunler:
                unique_urunler[key]["count"] += 1
            else:
                unique_urunler[key] = {"urun": urun.urun, "count": 1}
        sira_urunler.append(
            {
                "sira": sira,
                "urunler": unique_urunler.values(),
                "urun_sayisi": tum_urunler.count(),
            }
        )

    if request.method == "POST":
        secilen_urun = core_models.Urun.objects.get(pk=request.POST["urun"])
        secilen_sira = core_models.OtomatSira.objects.get(pk=request.POST["sira"])
        sira_urun = core_models.OtomatUrun(urun=secilen_urun, sira=secilen_sira)
        sira_urun.save()
        return redirect("otomat_detay", slug=otomat.slug)

    context = {
        "otomat": otomat,
        "sira_urunler": sira_urunler,
        "tum_urunler": urunler_listesi,
        "toplam_kapasite": toplam_kapasite,
    }
    return render(request, "otomat.html", context)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def otomat_ekle(request):

    if request.method == "POST":
        ad = request.POST["ad"]
        aciklama = request.POST["aciklama"]
        konum = request.POST["konum"]
        kapasite = request.POST["kapasite"]
        otomat = core_models.Otomat(
            ad=ad, aciklama=aciklama, konum=konum, kapasite=kapasite
        )
        otomat.save()
        return redirect("otomatlar")

    return render(request, "otomatlar.html")


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def otomat_duzenle(request, pk):
    otomat = get_object_or_404(core_models.Otomat, pk=pk)
    if request.method == "POST":
        ad = request.POST["ad"]
        aciklama = request.POST["aciklama"]
        konum = request.POST["konum"]
        kapasite = request.POST["kapasite"]
        otomat.ad = ad
        otomat.aciklama = aciklama
        otomat.konum = konum
        otomat.kapasite = kapasite
        otomat.save()
        return redirect("otomatlar")
    return render(request, "otomatlar.html")


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def otomat_sil(request, pk):
    otomat = get_object_or_404(core_models.Otomat, pk=pk)
    otomat.delete()

    return redirect("otomatlar")


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def otomat_durum(request, pk):
    otomat = get_object_or_404(core_models.Otomat, pk=pk)
    otomat.durum = not otomat.durum
    otomat.save()
    return redirect("otomat", slug=otomat.slug)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def kategoriler(request):

    categories = core_models.Kategori.objects.all()

    context = {
        "kategoriler": categories,
    }

    return render(request, "kategoriler.html", context)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def kategori_detay(request, slug):
    category = get_object_or_404(core_models.Kategori, slug=slug)
    category_products = core_models.Urun.objects.filter(kategori=category)
    product_count = category_products.count()
    product_images = core_models.UrunResim.objects.filter(urun__kategori=category)

    context = {
        "kategori": category,
        "urunler": category_products,
        "resimler": product_images,
        "urun_sayisi": product_count,
    }

    return render(request, "kategori.html", context)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def kategori_ekle(request):
    if request.method == "POST":
        name = request.POST["ad"]
        description = request.POST["aciklama"]
        category = core_models.Kategori(ad=name, aciklama=description)
        category.save()
        return redirect("kategoriler")
    return render(request, "kategoriler.html")


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def kategori_duzenle(request, pk):
    category = get_object_or_404(core_models.Kategori, pk=pk)
    if request.method == "POST":
        name = request.POST["ad"]
        description = request.POST["aciklama"]
        category.ad = name
        category.aciklama = description
        category.save()
        return redirect("kategoriler")
    return render(request, "kategoriler.html")


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def kategori_sil(request, pk):
    category = get_object_or_404(core_models.Kategori, pk=pk)
    category.delete()
    return redirect("kategoriler")


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def kategori_urun_ekle(request, slug):
    context = {}
    if request.method == "POST":
        name = request.POST["ad"]
        description = request.POST["aciklama"]
        price = request.POST["fiyat"]
        stock = request.POST["stok"]
        category = core_models.Kategori.objects.get(pk=request.POST["kategori"])
        product = core_models.Urun(
            ad=name, aciklama=description, kategori=category, fiyat=price, stok=stock
        )
        product.save()

        return redirect("kategori_detay", slug=category.slug)
    return render(request, "kategoriler.html", context)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def urun_ara(request):
    context = {}
    if "q" in request.GET:
        query = request.GET.get("q")
        urunler = core_models.Urun.objects.filter(
            Q(ad__icontains=query)
            | Q(aciklama__icontains=query)
            | Q(kategori__ad__icontains=query)
        ).distinct()

        context = {"urunler": urunler, "query": query}
    return render(request, "urun_ara.html", context)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def urun(request, slug):
    product = get_object_or_404(core_models.Urun, slug=slug)
    images = core_models.UrunResim.objects.filter(urun=product)
    categories = core_models.Kategori.objects.all()
    sira_urunler = core_models.OtomatUrun.objects.filter(urun=product)
    context = {
        "urun": product,
        "resimler": images,
        "kategoriler": categories,
        "urun_sira": sira_urunler,
    }
    return render(request, "urun.html", context)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def urunler(request):
    categories = core_models.Kategori.objects.all()
    products = core_models.Urun.objects.all()
    images = core_models.UrunResim.objects.all()

    context = {
        "urunler": products,
        "resimler": images,
        "kategoriler": categories,
    }
    return render(request, "urunler.html", context)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def urun_duzenle(request, pk):
    product = get_object_or_404(core_models.Urun, pk=pk)
    if request.method == "POST":
        name = request.POST["ad"]
        description = request.POST["aciklama"]
        price = request.POST["fiyat"]
        stock = request.POST["stok"]
        category = core_models.Kategori.objects.get(pk=request.POST["kategori"])
        status = request.POST.get("durum", False)
        product.ad = name
        product.aciklama = description
        product.kategori = category
        product.fiyat = price
        product.stok = stock
        product.durum = status
        product.save()
        return redirect("urun", slug=product.slug)
    return render(request, "urun.html", {"urun": product})


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def urun_resim_ekle(request, pk):
    urun = get_object_or_404(core_models.Urun, pk=pk)
    if request.method == "POST":
        form = core_forms.UrunResimForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES["image"]
            urun_image = form.save(commit=False)
            urun_image = core_models.UrunResim(urun=urun, image=image)
            urun_image.save()
        return redirect("urun", slug=urun.slug)
    else:
        form = core_forms.UrunResimForm()
    return render(request, "urun.html", {"form": form})


def urun_resim_goruntule(request, slug):
    image = get_object_or_404(core_models.UrunResim, urun__slug=slug)
    context = {"resim": image}
    http_response = HttpResponse(image.image, content_type="image/jpeg")
    return http_response


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def delete_image_local(image):
    if image:
        if os.path.isfile(image.path):
            os.remove(image.path)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def urun_resim_sil(request, pk):
    image = get_object_or_404(core_models.UrunResim, pk=pk)
    product = image.urun
    image.delete()
    delete_image_local(image.image)

    return redirect("urun", slug=product.slug)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def urun_sil(request, pk):
    product = get_object_or_404(core_models.Urun, pk=pk)
    product.delete()
    return redirect("kategori_detay", slug=product.kategori.slug)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def urun_durum(request, pk):
    product = get_object_or_404(core_models.Urun, pk=pk)
    product.durum = not product.durum
    product.save()
    return redirect("urun", slug=product.slug)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
@require_http_methods(["GET"])
def home(request):
    # if not request.user.is_authenticated:
    # return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    context = {"message": "Home Page"}
    return render(request, HomePageView.template_name, context)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
@require_http_methods(["GET"])
def user(request):
    user_profile = request.user
    context = {
        "user": user_profile,
    }
    return render(request, "user.html", context)


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def user_update(request):
    if request.method == "POST":
        session_user = get_object_or_404(User, pk=request.user.pk)
        form = core_forms.UpdateUserForm(request.POST, instance=session_user)
        if form.is_valid():
            form.save()
            return redirect("user")
    else:
        form = core_forms.UpdateUserForm(instance=request.user)
    return render(request, "user.html", {"form": form})


@login_required(redirect_field_name="next", login_url=reverse_lazy(settings.LOGIN_URL))
def user_delete(request):
    if request.method == "POST":
        session_user = get_object_or_404(User, pk=request.user.pk)
        session_user.delete()
        return redirect("home")


def auth_logout(request):
    logout(request)
    messages.success(request, "Çıkış Yapılıyor...")
    return redirect("home")


def auth_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    context = {"message": "Login Page"}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Kullanıcı adı veya şifre hatalı")
    return render(request, LoginPageView.template_name, context)


def register(request):
    if request.method == "POST":
        form = core_forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = core_forms.RegisterForm()
    return render(request, RegisterView.template_name, {"form": form})


def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Şifre değiştirildi")
            update_session_auth_hash(request, form.user)
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, PasswordChanePageView.template_name, {"form": form})
