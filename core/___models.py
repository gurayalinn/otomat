from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
from django.contrib.auth.models import (
    AbstractUser,
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


class Barkod(models.Model):
    barkod_no = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
    )
    urun = models.OneToOneField(Urun, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.barkod_no)


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

    def __str__(self):
        return f"{self.sira_harf} {self.sira_no}"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.sira_harf}{self.sira_no}")
        super().save(*args, **kwargs)


class OtomatUrun(models.Model):
    urun = models.ForeignKey(
        Urun, on_delete=models.CASCADE, related_name="otomat_urunler"
    )
    sira = models.ForeignKey(OtomatSira, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.urun} - {self.sira}"


def handle_upload_profile(instance, filename):
    return f"musteri/profile/user_{instance.user.pk}/{filename}"


class CustomUserManager(BaseUserManager):

    def create_user(self, email, tckn, username, password=None, **extra_fields):
        if not email:
            raise ValidationError("E-posta alanı boş bırakılamaz")
        if not tckn:
            raise ValidationError("TC Kimlik Numarası alanı boş bırakılamaz")
        if not tckn.isdigit():
            raise ValidationError("TC Kimlik Numarası sadece rakamlardan oluşmalıdır.")
        if len(tckn) != 11:
            raise ValidationError("TC Kimlik Numarası 11 haneli olmalıdır.")
        if tckn[0] == "0":
            raise ValidationError("TC Kimlik Numarası 0 ile başlayamaz.")
        if self.filter(tckn=tckn).exists():
            raise ValidationError("Bu TC Kimlik Numarası zaten kullanılmış.")
        if self.filter(email=email).exists():
            raise ValidationError("Bu e-posta adresi zaten kullanılmış.")
        if not password:
            raise ValidationError("Şifre alanı boş bırakılamaz")
        if not username:
            raise ValidationError("Kullanıcı adı alanı boş bırakılamaz")
        username = self.model.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(email=email, tckn=tckn, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, tckn, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, tckn, username, password, **extra_fields)

    def get_by_tckn(self, tckn):
        return self.get(tckn=tckn)

    def get_by_email(self, email):
        return self.get(email=email)

    def get_by_username(self, username):
        return self.get(username=username)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    tckn = models.CharField(
        max_length=11,
        unique=True,
        db_index=True,
        primary_key=True,
        verbose_name="TC Kimlik Numarası",
    )
    username = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name="Kullanıcı Adı",
    )
    email = models.EmailField(unique=True)
    ad = models.CharField(max_length=150)
    soyad = models.CharField(max_length=150)
    cinsiyet = models.CharField(max_length=1)
    dogum = models.DateField()
    adres = models.TextField()
    telefon = models.CharField(max_length=11)
    slug = models.SlugField(
        null=False, blank=True, unique=True, db_index=True, editable=False
    )
    profile = models.ImageField(
        default="musteri/profile/deafult_profile.svg",
        upload_to=handle_upload_profile,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["tckn"]

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.tckn)
        super().save(*args, **kwargs)

    def get_tckn(self):
        return self.tckn


class AbonmanKart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    kart_no = models.UUIDField(
        primary_key=True,
        editable=False,
        unique=True,
    )
    bakiye = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        null=False,
        blank=False,
    )
    durum = models.BooleanField(default=False)
    slug = models.SlugField(
        null=False, blank=True, unique=True, db_index=True, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.kart_no)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.kart_no}"

    def get_bakiye(self):
        return self.bakiye
