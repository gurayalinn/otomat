from django.contrib import admin
from django.db.models import Count
import core.models as models

# Register your models here.


class KategoriAdmin(admin.ModelAdmin):
    list_display = ["ad", "aciklama", "slug"]
    search_fields = ["ad", "aciklama"]
    prepopulated_fields = {"slug": ("ad",)}
    list_filter = ["ad"]
    list_per_page = 10

    class Meta:
        model = models.Kategori


class UrunResimAdmin(admin.StackedInline):
    model = models.UrunResim


class UrunAdmin(admin.ModelAdmin):
    list_display = [
        "ad",
        "kategori",
        "fiyat",
        "stok",
        "aciklama",
        "durum",
        "slug",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "ad",
        "kategori",
        "fiyat",
        "stok",
        "aciklama",
        "durum",
        "slug",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "ad",
        "kategori",
        "fiyat",
        "stok",
        "aciklama",
        "durum",
        "slug",
        "created_at",
        "updated_at",
    ]
    list_per_page = 10
    list_display_links = ["kategori"]
    inlines = [UrunResimAdmin]

    class Meta:
        model = models.Urun


class OtomatAdmin(admin.ModelAdmin):
    list_display = ["ad", "konum", "aciklama", "durum", "slug"]
    search_fields = ["ad", "konum", "aciklama", "durum", "slug"]
    prepopulated_fields = {"slug": ("ad",)}
    list_filter = ["ad", "aciklama", "konum", "slug"]
    list_per_page = 10

    class Meta:
        model = models.Otomat


class OtomatSiraAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(otomat_count=Count("otomat"))

    list_display = ["otomat", "sira_harf", "sira_no", "durum", "slug"]
    search_fields = ["otomat", "sira_harf", "sira_no", "durum", "slug"]
    list_filter = ["otomat", "sira_harf", "sira_no", "durum", "slug"]
    prepopulated_fields = {"slug": ("sira_harf", "sira_no")}
    list_per_page = 10
    list_display_links = ["otomat"]

    class Meta:
        model = models.OtomatSira


class OtomatUrunAdmin(admin.ModelAdmin):
    list_display = ["urun", "sira", "created_at", "updated_at"]
    search_fields = ["urun", "sira", "created_at", "updated_at"]
    list_filter = ["urun", "sira", "created_at", "updated_at"]
    list_per_page = 10
    list_display_links = ["urun", "sira"]

    class Meta:
        model = models.OtomatUrun


class AbonmanKartAdmin(admin.ModelAdmin):
    list_display = ["user", "kart_no", "bakiye", "durum", "slug"]
    search_fields = ["user", "kart_no", "bakiye", "durum", "slug"]
    list_filter = ["user", "kart_no", "bakiye", "durum", "slug"]
    prepopulated_fields = {"slug": ("kart_no",)}
    list_per_page = 10
    list_editable = ["bakiye", "durum"]
    list_display_links = ["user"]

    class Meta:
        model = models.AbonmanKart


admin.site.register(models.Barkod)
admin.site.register(models.CustomUser)
admin.site.register(models.Kategori, KategoriAdmin)
admin.site.register(models.OtomatUrun, OtomatUrunAdmin)
admin.site.register(models.OtomatSira, OtomatSiraAdmin)
admin.site.register(models.Otomat, OtomatAdmin)
admin.site.register(models.Urun, UrunAdmin)
admin.site.register(models.AbonmanKart, AbonmanKartAdmin)
