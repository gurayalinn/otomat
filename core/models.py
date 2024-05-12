import uuid
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import (
    AbstractUser,
    User,
    Group,
    Permission,
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models.signals import post_save


class Kategori(models.Model):
    ad = models.CharField(max_length=150)
    slug = models.SlugField(
        null=False, blank=True, unique=True, db_index=True, editable=False
    )
    aciklama = models.TextField(blank=True)

    def __str__(self):
        return f"{self.ad}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.ad)
        super().save(*args, **kwargs)

    objects = models.Manager()


class Urun(models.Model):
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    ad = models.CharField(max_length=200)
    fiyat = models.DecimalField(max_digits=6, decimal_places=2)
    stok = models.PositiveIntegerField(default=0)
    aciklama = models.TextField(blank=True)
    durum = models.BooleanField(default=True)
    slug = models.SlugField(
        null=False, blank=True, unique=True, db_index=True, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ad}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.ad)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("urun", kwargs={"slug": self.slug})

    def get_kategori(self):
        return self.kategori

    def get_durum_display(self):
        if self.durum:
            return "Aktif"
        return "Pasif"

    objects = models.Manager()


def handle_upload_urun(instance, filename):
    return f"urunler/urun_{instance.urun.pk}/{filename}"


class UrunResim(models.Model):
    urun = models.ForeignKey(
        Urun, on_delete=models.CASCADE, default=1, related_name="images"
    )
    image = models.ImageField(
        upload_to=handle_upload_urun,
        null=True,
        blank=True,
        height_field=None,
        width_field=None,
        max_length=100,
    )
    objects = models.Manager()

    def __str__(self):
        return f"{self.urun} - {self.image}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.image = self.compressImage(self.image)
        super(UrunResim, self).save(*args, **kwargs)

    def compressImage(self, image):
        from PIL import Image
        from io import BytesIO
        from django.core.files import File
        import os
        from django.core.files.uploadedfile import InMemoryUploadedFile

        img = Image.open(image)
        if img.mode != "RGB":
            img = img.convert("RGB")
        im_io = BytesIO()
        img.save(im_io, format="JPEG", quality=60)
        new_image = File(im_io, name=image.name)
        batch = os.path.split(image.name)
        new_image.name = os.path.join(batch[0], "compressed_" + batch[1])
        if image.size > new_image.size:
            new_image = InMemoryUploadedFile(
                new_image,
                None,
                new_image.name,
                "image/jpeg",
                new_image.tell,
                None,
            )

        return new_image


class Otomat(models.Model):
    ad = models.CharField(
        max_length=100,
        unique=True,
        error_messages={"unique": "Bu otomat adı zaten kullanılmış."},
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        null=False, blank=True, unique=True, db_index=True, editable=False
    )
    aciklama = models.TextField(blank=True)
    durum = models.BooleanField(default=True)
    konum = models.CharField(max_length=200)
    kapasite = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return f"{self.ad}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.ad)
        super().save(*args, **kwargs)


class OtomatSira(models.Model):
    otomat = models.ForeignKey(Otomat, on_delete=models.CASCADE)
    sira_harf = models.CharField(
        max_length=1,
        verbose_name="Sıra Harf",
        help_text="Sıra harf",
    )
    sira_no = models.PositiveIntegerField(
        default=1,
        verbose_name="Sıra",
        help_text="Sıra numarası",
    )
    durum = models.BooleanField(default=False)
    slug = models.SlugField(
        null=False, blank=True, unique=True, db_index=True, editable=False
    )
    objects = models.Manager()

    def __str__(self):
        return f"{self.sira_harf} {self.sira_no}"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.sira_harf}{self.sira_no}")
        super().save(*args, **kwargs)


class OtomatUrun(models.Model):
    otomat = models.ForeignKey(Otomat, on_delete=models.CASCADE)
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE)
    sira = models.ForeignKey(OtomatSira, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.urun} - {self.sira}"
