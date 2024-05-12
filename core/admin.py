from django.contrib import admin
from django.db.models import Count
import core.models as models

# Register your models here.


class KategoriAdmin(admin.ModelAdmin):
    list_display = ["ad", "aciklama"]
    search_fields = ["ad", "aciklama"]
    list_filter = ["ad", "aciklama"]
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
        "created_at",
        "updated_at",
    ]
    list_per_page = 10
    list_display_links = ["ad"]
    inlines = [UrunResimAdmin]

    class Meta:
        model = models.Urun


class OtomatAdmin(admin.ModelAdmin):
    list_display = ["ad", "konum", "aciklama", "durum", "kapasite"]
    search_fields = ["ad", "konum", "aciklama", "durum"]
    list_filter = ["ad", "aciklama", "konum"]
    list_per_page = 10

    class Meta:
        model = models.Otomat


class OtomatSiraAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(otomat_count=Count("otomat"))

    list_display = ["otomat", "sira_harf", "sira_no", "durum"]
    search_fields = ["otomat", "sira_harf", "sira_no", "durum"]
    list_filter = ["otomat", "sira_harf", "sira_no", "durum"]
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


admin.site.register(models.Kategori, KategoriAdmin)
admin.site.register(models.OtomatUrun, OtomatUrunAdmin)
admin.site.register(models.OtomatSira, OtomatSiraAdmin)
admin.site.register(models.Otomat, OtomatAdmin)
admin.site.register(models.Urun, UrunAdmin)
