from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
import core.models as core_models


class UrunResimForm(forms.ModelForm):
    class Meta:
        model = core_models.UrunResim
        fields = ["urun", "image"]


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]


class KategoriForm(ModelForm):
    class Meta:
        model = core_models.Kategori
        fields = "__all__"


class UrunForm(ModelForm):
    class Meta:
        model = core_models.Urun
        fields = "__all__"


class OtomatForm(ModelForm):
    class Meta:
        model = core_models.Otomat
        fields = "__all__"


class OtomatSiraForm(ModelForm):
    class Meta:
        model = core_models.OtomatSira
        fields = "__all__"


class OtomatUrunForm(ModelForm):
    class Meta:
        model = core_models.OtomatUrun
        fields = "__all__"
