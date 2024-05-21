from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
import core.models as core_models


@receiver(post_save, sender=core_models.OtomatUrun)
def update_stock_on_add(sender, instance, created, **kwargs):
    try:
        if created:
            urun = instance.urun
            urun.stok -= 1
            urun.save()
            print(f"Stok güncellendi: {urun.ad} - Yeni stok: {urun.stok}")
    except Exception as e:
        print(f"Stok güncellenirken hata oluştu: {e}")


@receiver(post_delete, sender=core_models.OtomatUrun)
def update_stock_on_delete(sender, instance, **kwargs):
    try:
        urun = instance.urun
        urun.stok += 1
        urun.save()
        print(f"Stok güncellendi: {urun.ad} - Yeni stok: {urun.stok}")
    except Exception as e:
        print(f"Stok güncellenirken hata oluştu: {e}")


@receiver(post_delete, sender=core_models.OtomatSira)
def update_kapasite_on_delete(sender, instance, **kwargs):
    try:
        otomat = instance.otomat
        otomat.kapasite += 20
        otomat.save()
        print(f"Kapasite güncellendi: {otomat.ad} - Kapasite: {otomat.kapasite}")
    except Exception as e:
        print(f"Kapasite güncellenirken hata oluştu: {e}")


@receiver(post_save, sender=core_models.OtomatSira)
def update_kapasite_on_add(sender, instance, created, **kwargs):
    try:
        if created:
            otomat = instance.otomat
            otomat.kapasite -= 20
            otomat.save()
            print(f"Kapasite güncellendi: {otomat.ad} - Kapasite: {otomat.kapasite}")
    except Exception as e:
        print(f"Kapasite güncellenirken hata oluştu: {e}")


@receiver(pre_save, sender=core_models.OtomatSira)
def update_kapasite_on_update(sender, instance, **kwargs):
    try:
        if instance.pk:
            otomat = instance.otomat
            otomat.kapasite += 20
            otomat.save()
            print(f"Kapasite güncellendi: {otomat.ad} - Kapasite: {otomat.kapasite}")
    except Exception as e:
        print(f"Kapasite güncellenirken hata oluştu: {e}")
    try:
        if instance.pk:
            otomat = instance.otomat
            otomat.kapasite -= 20
            otomat.save()
            print(f"Kapasite güncellendi: {otomat.ad} - Kapasite: {otomat.kapasite}")
    except Exception as e:
        print(f"Kapasite güncellenirken hata oluştu: {e}")
