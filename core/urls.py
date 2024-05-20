from django.urls import path
import core.views as core_views

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
)

urlpatterns = [
    path("", core_views.home, name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", core_views.register, name="register"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("user", core_views.user, name="user"),
    path("user_update/", core_views.user_update, name="user_update"),
    path("user_delete/", core_views.user_delete, name="user_delete"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "sira/<slug:slug>/urun_sil/<int:pk>/",
        core_views.sira_urun_sil,
        name="sira_urun_sil",
    ),
    path(
        "sira/<slug:slug>/urun_ekle/",
        core_views.sira_urun_ekle,
        name="sira_urun_ekle",
    ),
    path("sira_sil/<int:pk>/", core_views.sira_sil, name="sira_sil"),
    path("sira/<slug:slug>/", core_views.sira, name="sira"),
    path(
        "sira_duzenle/<int:pk>/",
        core_views.sira_duzenle,
        name="sira_duzenle",
    ),
    path(
        "otomat/<slug:slug>/sira_ekle",
        core_views.otomat_sira_ekle,
        name="otomat_sira_ekle",
    ),
    path("otomatlar/", core_views.otomatlar, name="otomatlar"),
    path("otomat/<slug:slug>/", core_views.otomat_detay, name="otomat_detay"),
    path("otomat_ekle/", core_views.otomat_ekle, name="otomat_ekle"),
    path("otomat_sil/<int:pk>/", core_views.otomat_sil, name="otomat_sil"),
    path("otomat_durum/<int:pk>/", core_views.otomat_durum, name="otomat_durum"),
    path(
        "otomat_duzenle/<int:pk>/",
        core_views.otomat_duzenle,
        name="otomat_duzenle",
    ),
    path("kategoriler/", core_views.kategoriler, name="kategoriler"),
    path("kategori/<slug:slug>/", core_views.kategori_detay, name="kategori_detay"),
    path("kategori_ekle/", core_views.kategori_ekle, name="kategori_ekle"),
    path("kategori_sil/<int:pk>/", core_views.kategori_sil, name="kategori_sil"),
    path(
        "kategori_duzenle/<int:pk>/",
        core_views.kategori_duzenle,
        name="kategori_duzenle",
    ),
    path("urunler/", core_views.urunler, name="urunler"),
    path("urun/<slug:slug>/", core_views.urun, name="urun"),
    path(
        "kategori/<slug:slug>/urun_ekle/",
        core_views.kategori_urun_ekle,
        name="kategori_urun_ekle",
    ),
    path("urun_sil/<int:pk>/", core_views.urun_sil, name="urun_sil"),
    path("urun_duzenle/<int:pk>/", core_views.urun_duzenle, name="urun_duzenle"),
    path(
        "urun_resim_ekle/<int:pk>/",
        core_views.urun_resim_ekle,
        name="urun_resim_ekle",
    ),
    path(
        "urun_resim/<slug:slug>/",
        core_views.urun_resim_goruntule,
        name="urun_resim_goruntule",
    ),
    path(
        "urun_resim_sil/<int:pk>/",
        core_views.urun_resim_sil,
        name="urun_resim_sil",
    ),
    path("urun_durum/<int:pk>/", core_views.urun_durum, name="urun_durum"),
    path(
        "urun_ara/",
        core_views.urun_ara,
        name="urun_ara",
    ),
    # path("profile/", views.profile, name="profile"),
    # path("profile/edit/", views.profile_edit, name="profile_edit"),
    # path("abonman/", views.abonman, name="abonman"),
    # path("abonman/<int:id>/", views.abonman_bilgi, name="abonman_bilgi"),
    # path("abonman/<int:id>/yenile/", views.abonman_yenile, name="abonman_yenile"),
    # path("abonman/<int:id>/iptal/", views.abonman_iptal, name="abonman_iptal"),
    # path("abonman/create/", views.abonman_olustur, name="abonman_olustur"),
]
