from django import forms
from django.forms import ModelForm
from giris.models import marka, demirbas, proje, kategori, musteri
from giris.models import grup, sirket, ekipman_turu, servis, alt_kategori, yedek_parca, hareket, ariza
from django.contrib.admin.widgets import AdminDateWidget

#from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from bootstrap_datepicker.widgets import DatePicker
import datetime
from datetime import date





DURUM = (
('A', 'Aktif'),
('P', 'Pasif'),
)

VARMI = (
('E', 'Evet'),
('H', 'Hayır'),
)

TIPI = (
('T', 'Taşıma'),
('D', 'Depoya Taşı'),
('P', 'Pert'),
('G', 'Depodan Taşı'),
('X', 'Pert İptal'),
('Z', 'Proje Sonrası Verildi')
)

ILLER = (
('ANK', 'Ankara'),
('IST', 'İstanbul'),
('IZM', 'İzmir'),
('ADA', 'Adana'),
('BUR', 'Bursa'),
('KON', 'Konya'),
('KAY', 'Kayseri'),
('MER', 'Mersin'),
('ANT', 'Antalya'),
('SAM', 'Samsun'),
('TRA', 'Trabzon'),
('MAL', 'Malatya'),
)

FATURA_TURU = (
('S', 'SabitÜcret'),
('P', 'ProjeSaati'),
('G', 'GörevSaati'),
)

FATURA_DURUMU = (
('B', 'Başlamadı'),
('D', 'DevamEdiyor'),
('X', 'Beklemede'),
('I', 'İptal'),
('T', 'Tamamlandı'),
)




class NameForm(forms.Form):
    your_name = forms.CharField(label='senin adın......:', max_length=100)
    tarih = forms.DateField(label='senin tarihin...:',
        widget=forms.TextInput(attrs={ 'class':'datepicker' }),
        #widget=forms.DateInput(format='%d/%m/%Y'),
        #input_formats=('%d/%m/%Y',)
        )
    def clean(self):
        cleaned_data = super(NameForm, self).clean()
        cc_name = cleaned_data.get("your_name")
        cc_date = cleaned_data.get("tarih")
        base_date = "2017-08-29"
        print (cc_name)
        print (cc_date)
        if cc_name and cc_date:
            # Only do something if both fields are valid so far.
            if cc_name == "levent" :
                conv_date = cc_date.strftime('%Y-%m-%d')
                print (conv_date)
                if not (conv_date == base_date):
                    raise forms.ValidationError(
                        " isim ve tarihte uyuşmazlık var.... "
                    )





class DemirbasForm(forms.Form):
    adi = forms.CharField(label='Demirbaş Adı..:', max_length=100)
    proje = forms.ModelChoiceField(label='Proje Adı..:', queryset=proje.objects.all())
    bolum = forms.CharField(label='Bölümü...:', max_length=100)
    marka = forms.ModelChoiceField(label='Marka........:', queryset=marka.objects.all())
    ekipman_turu = forms.ModelChoiceField(label='Ekipman Türü..:', queryset=ekipman_turu.objects.all())
    alt_kategori = forms.ModelChoiceField(label='Alt Kategori..:', queryset=alt_kategori.objects.all())
    modeli = forms.CharField(label='Modeli..:', max_length=100)
    durumu = forms.ChoiceField(label='Durumu........:', widget=forms.Select, choices=DURUM,)
    garanti_varmi = forms.ChoiceField(label='Garanti Var Mı.:',  widget=forms.Select, choices=VARMI,)
    garanti_bitis = forms.DateField(label='Garanti Bitiş Tarihi...:', required=False,
        widget=forms.TextInput(attrs={ 'class':'datepicker',})
        )
    amts_kalanyil = forms.IntegerField(label='Kalan Amortisman Yılı...:', min_value=0)
    bedeli = forms.IntegerField(label='Bedeli...:', min_value=0)
    aciklama = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}),)


    def clean(self):
        cleaned_data = super(DemirbasForm, self).clean()
        cc_adi = cleaned_data.get("adi")
        cc_proje = cleaned_data.get("proje")
        cc_bolum = cleaned_data.get("bolum")
        cc_marka = cleaned_data.get("marka")
        cc_ekipman_turu = cleaned_data.get("ekipman_turu")
        cc_alt_kategori = cleaned_data.get("alt_kategori")
        cc_modeli = cleaned_data.get("modeli")
        cc_durumu = cleaned_data.get("durumu")
        cc_garanti_varmi = cleaned_data.get("garanti_varmi")
        cc_garanti_bitis = cleaned_data.get("garanti_bitis")
        cc_amts_kalanyil = cleaned_data.get("amts_kalanyil")
        cc_bedeli = cleaned_data.get("bedeli")
        cc_aciklama = cleaned_data.get("aciklama")
        print (cc_adi, cc_proje, cc_bedeli, cc_garanti_varmi, cc_garanti_bitis)
        #if cc_garanti_varmi and cc_garanti_bitis:
            # Only do something if both fields are valid so far.
        if cc_garanti_varmi == "E" :
            print (cc_garanti_bitis)
            print (date.today())
            if cc_garanti_bitis == None:
                raise forms.ValidationError(
                    " garanti bitiş süresi girmelisiniz.... "
                )
            if cc_garanti_bitis < date.today():
                raise forms.ValidationError(
                    " ileri bir tarih girmelisiniz.... "
                )
        if cc_garanti_varmi == "H" :
            print (cc_garanti_bitis)
            if not (cc_garanti_bitis == None):
                raise forms.ValidationError(
                    " garanti bitiş süresi boş olmalı.... "
                )




class Demirbas_Ara_Form(forms.Form):
    alan = forms.CharField(label='demirbaş adında arama..', widget=forms.Textarea(attrs={'cols': 30, 'rows': 1}),)



class HareketForm(forms.Form):
    adi = forms.CharField(label='Demirbaş Adı..:', max_length=100)
    proje = forms.ModelChoiceField(label='Proje Adı..:', queryset=proje.objects.all())
    bolum = forms.CharField(label='Bölümü...:', max_length=100)
    marka = forms.ModelChoiceField(label='Marka........:', queryset=marka.objects.all())
    ekipman_turu = forms.ModelChoiceField(label='Ekipman Türü..:', queryset=ekipman_turu.objects.all())
    alt_kategori = forms.ModelChoiceField(label='Alt Kategori..:', queryset=alt_kategori.objects.all())
    modeli = forms.CharField(label='Modeli..:', max_length=100)
    durumu = forms.ChoiceField(label='Durumu........:', widget=forms.Select, choices=DURUM,)
    garanti_varmi = forms.ChoiceField(label='Garanti Var Mı.:',  widget=forms.Select, choices=VARMI,)
    garanti_bitis = forms.DateField(label='Garanti Bitiş Tarihi...:', required=False,
        widget=forms.TextInput(attrs={ 'class':'datepicker',})
        )
    amts_kalanyil = forms.IntegerField(label='Kalan Amortisman Yılı...:', min_value=0)
    bedeli = forms.IntegerField(label='Bedeli...:', min_value=0)
    aciklama = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}),)


    def clean(self):
        cleaned_data = super(HareketForm, self).clean()
        cc_adi = cleaned_data.get("adi")
        cc_proje = cleaned_data.get("proje")
        cc_bolum = cleaned_data.get("bolum")
        cc_marka = cleaned_data.get("marka")
        cc_ekipman_turu = cleaned_data.get("ekipman_turu")
        cc_alt_kategori = cleaned_data.get("alt_kategori")
        cc_modeli = cleaned_data.get("modeli")
        cc_durumu = cleaned_data.get("durumu")
        cc_garanti_varmi = cleaned_data.get("garanti_varmi")
        cc_garanti_bitis = cleaned_data.get("garanti_bitis")
        cc_amts_kalanyil = cleaned_data.get("amts_kalanyil")
        cc_bedeli = cleaned_data.get("bedeli")
        cc_aciklama = cleaned_data.get("aciklama")
        print (cc_adi, cc_proje, cc_bedeli, cc_garanti_varmi, cc_garanti_bitis)
        #if cc_garanti_varmi and cc_garanti_bitis:
            # Only do something if both fields are valid so far.
        if cc_garanti_varmi == "E" :
            print (cc_garanti_bitis)
            print (date.today())
            if cc_garanti_bitis == None:
                raise forms.ValidationError(
                    " garanti bitiş süresi girmelisiniz.... "
                )
            if cc_garanti_bitis < date.today():
                raise forms.ValidationError(
                    " ileri bir tarih girmelisiniz.... "
                )
        if cc_garanti_varmi == "H" :
            print (cc_garanti_bitis)
            if not (cc_garanti_bitis == None):
                raise forms.ValidationError(
                    " garanti bitiş süresi boş olmalı.... "
                )


class Hareket_Ara_Form(forms.Form):
    alan = forms.CharField(label='hareket açıklamada arama..', widget=forms.Textarea(attrs={'cols': 30, 'rows': 1}),)


class ArizaForm(forms.Form):
    adi = forms.CharField(label='Demirbaş Adı..:', max_length=100)
    proje = forms.ModelChoiceField(label='Proje Adı..:', queryset=proje.objects.all())
    bolum = forms.CharField(label='Bölümü...:', max_length=100)
    marka = forms.ModelChoiceField(label='Marka........:', queryset=marka.objects.all())
    ekipman_turu = forms.ModelChoiceField(label='Ekipman Türü..:', queryset=ekipman_turu.objects.all())
    alt_kategori = forms.ModelChoiceField(label='Alt Kategori..:', queryset=alt_kategori.objects.all())
    modeli = forms.CharField(label='Modeli..:', max_length=100)
    durumu = forms.ChoiceField(label='Durumu........:', widget=forms.Select, choices=DURUM,)
    garanti_varmi = forms.ChoiceField(label='Garanti Var Mı.:',  widget=forms.Select, choices=VARMI,)
    garanti_bitis = forms.DateField(label='Garanti Bitiş Tarihi...:', required=False,
        widget=forms.TextInput(attrs={ 'class':'datepicker',})
        )
    amts_kalanyil = forms.IntegerField(label='Kalan Amortisman Yılı...:', min_value=0)
    bedeli = forms.IntegerField(label='Bedeli...:', min_value=0)
    aciklama = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}),)


    def clean(self):
        cleaned_data = super(HareketForm, self).clean()
        cc_adi = cleaned_data.get("adi")
        cc_proje = cleaned_data.get("proje")
        cc_bolum = cleaned_data.get("bolum")
        cc_marka = cleaned_data.get("marka")
        cc_ekipman_turu = cleaned_data.get("ekipman_turu")
        cc_alt_kategori = cleaned_data.get("alt_kategori")
        cc_modeli = cleaned_data.get("modeli")
        cc_durumu = cleaned_data.get("durumu")
        cc_garanti_varmi = cleaned_data.get("garanti_varmi")
        cc_garanti_bitis = cleaned_data.get("garanti_bitis")
        cc_amts_kalanyil = cleaned_data.get("amts_kalanyil")
        cc_bedeli = cleaned_data.get("bedeli")
        cc_aciklama = cleaned_data.get("aciklama")
        print (cc_adi, cc_proje, cc_bedeli, cc_garanti_varmi, cc_garanti_bitis)
        #if cc_garanti_varmi and cc_garanti_bitis:
            # Only do something if both fields are valid so far.
        if cc_garanti_varmi == "E" :
            print (cc_garanti_bitis)
            print (date.today())
            if cc_garanti_bitis == None:
                raise forms.ValidationError(
                    " garanti bitiş süresi girmelisiniz.... "
                )
            if cc_garanti_bitis < date.today():
                raise forms.ValidationError(
                    " ileri bir tarih girmelisiniz.... "
                )
        if cc_garanti_varmi == "H" :
            print (cc_garanti_bitis)
            if not (cc_garanti_bitis == None):
                raise forms.ValidationError(
                    " garanti bitiş süresi boş olmalı.... "
                )




class Ariza_Ara_Form(forms.Form):
    alan = forms.CharField(label='ariza adında arama..', widget=forms.Textarea(attrs={'cols': 30, 'rows': 1}),)



#  model formlar buradan başlıyor.......................


def ProjeForm(ModelForm):
    class Meta:
            model = proje
            fields = '__all__'
            labels = { 'proje_adi': _('Proje Adı')}
            help_texts = { 'proje_adi': _('lüften proje adı giriniz..')}



def MarkaForm(ModelForm):
    class Meta:
            model = marka
            fields = ('marka_adi')
            labels = {
                "marka_adi": "Marka Adı"
                }
            help_texts = { 'marka_adi': _('lüften marka adı giriniz..')}


def KategoriForm(ModelForm):
    class Meta:
            model = kategori
            fields = '__all__'
            labels = { 'kategori_adi': _('Kategori Adı')}
            help_texts = { 'kategori_adi': _('lüften kategori adı giriniz..')}


def MusteriForm(ModelForm):
    class Meta:
            model = musteri
            fields = '__all__'
            labels = { 'musteri_adi': _('Müşteri Adı')}
            help_texts = { 'musteri_adi': _('lüften müşteri adı giriniz..')}


def GrupForm(ModelForm):
    class Meta:
            model = grup
            fields = '__all__'
            labels = { 'grup_adi': _('Grup Adı')}
            help_texts = { 'grup_adi': _('lüften grup adı giriniz..')}


def SirketForm(ModelForm):
    class Meta:
            model = sirket
            fields = ('sirket_adi')
            labels = {
                "sirket_adi": "Şirket Adı"
                }
            help_texts = { 'sirket_adi': _('lüften şirket adı giriniz..')}


def Ekipman_turuForm(ModelForm):
    class Meta:
            model = ekipman_turu
            fields = '__all__'
            labels = { 'ekipman_turu': _('Ekipman türü')}
            help_texts = { 'ekipman_turu': _('lüften ekipman türü giriniz..')}


def ServisForm(ModelForm):
    class Meta:
            model = servis
            fields = '__all__'
            labels = { 'servis_adi': _('Servis Adı')}
            help_texts = { 'servis_adi': _('lüften servis adı giriniz..')}


def Alt_kategoriForm(ModelForm):
    class Meta:
            model = alt_kategori
            fields = '__all__'
            labels = { 'alt_kategori_adi': _('Alt Kategori Adı')}
            help_texts = { 'kategori_adi': _('lüften kategori adı giriniz..')}


def Yedek_parcaForm(ModelForm):
    class Meta:
            model = yedek_parca
            fields = '__all__'
            labels = { 'yparca_adi': _('Yedek parça adı')}
            help_texts = { 'yparca_adi': _('lüften yedek parça adı giriniz..')}
