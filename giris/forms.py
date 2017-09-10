from django import forms
from django.forms import ModelForm
from giris.models import marka
from django.utils.translation import gettext as _



"""from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)"""


def DemirbasGirisForm(ModelForm):
    class Meta:
            model = demirbas
            fields = '__all__'
            labels = { 'demirbasadi': _('Demirbaş Adı')}
            help_texts = { 'demirbasadi': _('lüften demirbaş adı giriniz..')}


def ProjeGirisForm(ModelForm):
    class Meta:
            model = proje
            fields = '__all__'
            labels = { 'proje_adi': _('Proje Adı')}
            help_texts = { 'proje_adi': _('lüften proje adı giriniz..')}



def MarkaGirisForm(ModelForm):
    class Meta:
            model = marka
            fields = '__all__'
            labels = { 'marka_adi': _('Marka Adı')}
            help_texts = { 'marka_adi': _('lüften marka adı giriniz..')}


def KategoriGirisForm(ModelForm):
    class Meta:
            model = kategori
            fields = '__all__'
            labels = { 'kategori_adi': _('Marka Adı')}
            help_texts = { 'kategori_adi': _('lüften kategori adı giriniz..')}


def MusteriGirisForm(ModelForm):
    class Meta:
            model = musteri
            fields = '__all__'
            labels = { 'musteri_adi': _('Müşteri Adı')}
            help_texts = { 'musteri_adi': _('lüften müşteri adı giriniz..')}
