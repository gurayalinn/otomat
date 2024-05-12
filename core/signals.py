from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.db.models.signals import delete
from . import models as core_models


@receiver(pre_save, sender=core_models.OtomatUrun)
def otomat_urun_pre_save(sender, instance, **kwargs):
    if instance.pk:
        instance.urun.stok -= 1
        instance.urun.save()
        instance.sira.sira_no += 1
        instance.sira.save()
        instance.sira.durum = True
        instance.sira.save()


@receiver(delete, sender=core_models.OtomatUrun)
def otomat_urun_delete(sender, instance, **kwargs):
    instance.urun.stok += 1
    instance.urun.save()
    instance.sira.sira_no -= 1
    instance.sira.save()
    instance.sira.durum = False
    instance.sira.save()


@receiver(post_save, sender=core_models.OtomatSira)
def otomat_sira_post_save(sender, instance, **kwargs):
    if instance.sira_no == 0:
        instance.durum = False
        instance.save()
    if instance.sira_no > 0:
        instance.durum = True
        instance.save()
    if instance.sira_no < 1:
        instance.durum = False
        instance.save()
        # send_mail(
        #     "Sıra Uyarısı",
        #     f"{instance.otomat} otomatının {instance.sira_no} numaralı sırası tükenmiştir.",
        #     settings.EMAIL_HOST_USER,
        #     [instance.otomat.barkod.barkod_no],
        #     fail_silently=False,
        # )


@receiver(post_save, sender=core_models.OtomatUrun)
def otomat_urun_post_save(sender, instance, **kwargs):
    if instance.urun.stok == 0:
        instance.urun.durum = False
        instance.urun.save()
    if instance.urun.stok > 0:
        instance.urun.durum = True
        instance.urun.save()
    if instance.urun.stok < 1:
        instance.urun.durum = False
        instance.urun.save()
        # send_mail(
        #     "Stok Uyarısı",
        #     f"{instance.urun.ad} ürününün stok miktarı tükenmiştir.",
        #     settings.EMAIL_HOST_USER,
        #     [instance.urun.barkod.barkod_no],
        #     fail_silently=False,
        # )
    if instance.sira.sira_no == 0:
        instance.sira.durum = False
        instance.sira.save()
    if instance.sira.sira_no > 0:
        instance.sira.durum = True
        instance.sira.save()
    if instance.sira.sira_no < 1:
        instance.sira.durum = False
        instance.sira.save()
        # send_mail(
        #     "Sıra Uyarısı",
        #     f"{instance.sira.otomat} otomatının {instance.sira.sira_no} numaralı sırası tükenmiştir.",
        #     settings.EMAIL_HOST_USER,
        #     [instance.sira.otomat.barkod.barkod_no],
        #     fail_silently=False,
        # )
