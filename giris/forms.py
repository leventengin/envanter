from django import forms
from django.forms import ModelForm
from giris.models import marka, demirbas, proje, kategori, musteri
from giris.models import yparca_demirbas, yp_choice, yparca_ariza, dem_ariza
from giris.models import grup, sirket, ekipman_turu, servis, alt_kategori, yedek_parca
from giris.models import hareket, ariza
from django.contrib.admin.widgets import AdminDateWidget

#from __future__ import unicode_literals
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from bootstrap_datepicker.widgets import DatePicker
import datetime
from datetime import date

from django.core import serializers
from django.contrib.postgres.search import SearchVector
from django.views.generic import FormView
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from datetime import date, datetime
from django.template.loader import render_to_string
import requests



DURUM = (
('A', 'Aktif'),
('P', 'Pasif'),
)

VARMI = (
('E', 'Evet'),
('H', 'Hayır'),
)

KIMIN = (
('Ş', 'Şirketin'),
('M', 'Müşterinin'),
)

KULLANIM_DURUMU = (
('K', 'Kullanımda'),
('P', 'Pert oldu'),
('V', 'Proje sonunda müşteriye verildi'),
('D', 'Depoda'),
)

TIPI = (
('T', 'Diğer Projeye Taşı'),
('D', 'Depoya Taşı'),
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


json_choices =[('a','a'),]

class NameForm(forms.Form):
    #json_choices.insert('0',('',' önce demirbaş seç...'))
    gizli = forms.CharField(required=False, initial=None)
    your_name = forms.CharField(label='senin adın......:', max_length=100)
    tarih = forms.DateField(label='senin tarihin...:', widget=forms.TextInput(attrs={ 'class':'datepicker' }))
    demirbas = forms.ModelChoiceField(label='Demirbaş Adı..:', queryset=demirbas.objects.all())
    #yedek_parca = forms.ModelChoiceField(label='Yedek parça ........:', queryset=yedek_parca.objects.all(),
    #                    widget=forms.TextInput(attrs={ 'class':'myFunction' }))
    yparca_choice = forms.ChoiceField(label='Yedek parça choice ile ........:',
            widget=forms.Select, choices=json_choices)
    yedek_parca = forms.ModelChoiceField(label='Yedek parça...:', queryset=yedek_parca.objects.none())

    def __init__(self, *args, **kwargs):
        sel_alt = kwargs.pop("selected_alt")
        print("initial içinden selected_alt", sel_alt)
        super(NameForm, self).__init__(*args, **kwargs)
        self.fields['yedek_parca'].queryset = yedek_parca.objects.filter(alt_kategori=sel_alt)
        print("queryset initial içinden..:", self.fields['yedek_parca'].queryset)

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
    pk_no = forms.IntegerField(required=False, widget=forms.HiddenInput())
    adi = forms.CharField(label='Demirbaş Adı..:', max_length=100)
    proje = forms.ModelChoiceField(label='Proje Adı..:', queryset=proje.objects.all())
    bolum = forms.CharField(label='Bölümü...:', max_length=100)
    marka = forms.ModelChoiceField(label='Marka........:', queryset=marka.objects.all())
    ekipman_turu = forms.ModelChoiceField(label='Ekipman Türü..:', queryset=ekipman_turu.objects.all())
    alt_kategori = forms.ModelChoiceField(label='Alt Kategori..:', queryset=alt_kategori.objects.all())
    modeli = forms.CharField(label='Modeli..:', max_length=100)
    durumu = forms.ChoiceField(label='Durumu........:', widget=forms.Select, choices=DURUM,)
    kimin = forms.ChoiceField(label='Kimin........:', widget=forms.Select, choices=KIMIN,)
    garanti_varmi = forms.ChoiceField(label='Garanti Var Mı.:',  widget=forms.Select, choices=VARMI,)
    garanti_bitis = forms.DateField(label='Gar. Bitiş Tarihi...:', required=False,
                widget=forms.TextInput(attrs={ 'class': 'datepicker'}))
    amts_kalanyil = forms.IntegerField(label='Kalan Amts Yılı...:', min_value=0)
    bedeli = forms.CharField(label='Bedeli..(TL).:')
    bedeli_int = forms.IntegerField(required=False,widget=forms.HiddenInput())
    aciklama = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}),)




    def clean(self):
        cleaned_data = super(DemirbasForm, self).clean()
        cc_pk = cleaned_data.get("pk_no")
        cc_adi = cleaned_data.get("adi")
        cc_proje = cleaned_data.get("proje")
        cc_bolum = cleaned_data.get("bolum")
        cc_marka = cleaned_data.get("marka")
        cc_ekipman_turu = cleaned_data.get("ekipman_turu")
        cc_alt_kategori = cleaned_data.get("alt_kategori")
        cc_modeli = cleaned_data.get("modeli")
        cc_durumu = cleaned_data.get("durumu")
        cc_kimin = cleaned_data.get("kimin")
        cc_garanti_varmi = cleaned_data.get("garanti_varmi")
        cc_garanti_bitis = cleaned_data.get("garanti_bitis")
        cc_amts_kalanyil = cleaned_data.get("amts_kalanyil")
        cc_bedeli = cleaned_data.get("bedeli")
        cc_bedeli_int = cleaned_data.get("bedeli_int")
        cc_aciklama = cleaned_data.get("aciklama")
        print ("pk...önemli...:", cc_pk)
        print (cc_adi, cc_proje, cc_bedeli, cc_bedeli_int, cc_garanti_varmi, cc_garanti_bitis)
        try:
            cc = int(cc_bedeli_int)
        except:
            raise forms.ValidationError(" lütfen proje bedeli alanına sayı giriniz.... ")
        #if cc_garanti_varmi and cc_garanti_bitis:
            # Only do something if both fields are valid so far.
        #conv_date = cc_garanti_bitis.strftime('%Y-%m-%d')
        if cc_garanti_varmi == "E" :
            print ("E - garanti bitiş ", cc_garanti_bitis)
            print ("date today....",  date.today())
            #print ("conv date", conv_date)
            if cc_garanti_bitis == None:
                raise forms.ValidationError(
                    " garanti bitiş tarihi girmelisiniz.... "
                )
            if cc_garanti_bitis < date.today():
                if cc_pk == None:
                    raise forms.ValidationError(
                        " garanti bitiş için ileri bir tarih girmelisiniz.... "
                        )
        if cc_garanti_varmi == "H" :
            print ("H -  garanti bitiş", cc_garanti_bitis)
            #print ("conv date", conv_date)
            if not (cc_garanti_bitis == None):
                raise forms.ValidationError(
                    " garanti bitiş tarihi boş olmalı.... "
                )






class Demirbas_Ara_Form(forms.Form):
    alan = forms.CharField(label='Demirbaş adında arama..', widget=forms.Textarea(attrs={'cols': 30, 'rows': 1}),)


class Proje_SorForm(forms.Form):
    hangi_proje = forms.ModelChoiceField(label='Proje seçin..........:', queryset=proje.objects.all())


class Proje_Dem_SorForm(forms.Form):
    hangi_proje = forms.ModelChoiceField(label='Proje seçin..........:', queryset=proje.objects.all())
    hangi_dem = forms.ModelChoiceField(label='Demirbaş seçin.......:', queryset=demirbas.objects.all())
    def __init__(self, *args, **kwargs):
        proje_no = kwargs.pop("proje_no")
        print("proje no init içinden...:", proje_no)
        super(Proje_SorForm, self).__init__(*args, **kwargs)
        self.fields['hangi_dem'].queryset = demirbas.objects.filter(proje=proje_no)






class HareketForm(forms.Form):
    dem_id = forms.IntegerField(label='Demirbaş id....:', disabled=True, required=False )
    dem_adi = forms.CharField(label='Demirbaş adı....:', disabled=True, required=False)
    dem_proj = forms.CharField(label='Mevcut proje....:', disabled=True, required=False)
    har_tipi = forms.ChoiceField(label='Hareket tipi........:', widget=forms.Select, choices=TIPI,)
    sonraki_proj = forms.ModelChoiceField(label='Sonraki proje.......:', queryset=proje.objects.all())
    aciklama = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}),)
    hidd_proje = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(HareketForm, self).clean()
        cc_dem_id = self.cleaned_data.get("dem_id")
        cc_dem_adi = self.cleaned_data.get("dem_adi")
        cc_dem_proje = self.cleaned_data.get("dem_proje")
        cc_har_tipi = self.cleaned_data.get("har_tipi")
        cc_sonraki_proj = self.cleaned_data.get("sonraki_proj")
        cc_aciklama = self.cleaned_data.get("aciklama")
        cc_hidd_proje = self.cleaned_data.get("hidd_proje")
        #if 'aa_pk' in request.session:
        #cc_pk = request.session.get('aa_pk')
        #print("cc_pk ,  aktarılan değer....:", aa_pk)
        #a = str(cc_sonraki_proj)
        #if (cc_hidd_proje == a):
        #    HareketForm(dem_pk=pk)
        #    self.add_error("sonraki_proj", "iki proje aynı olamaz.......")
        #return cleaned_data
        #   raise forms.ValidationError(" iki proje aynı olamaz.... ", )




class Hareket_Ara_Form(forms.Form):
    alan = forms.CharField(label='hareket açıklamada arama..', widget=forms.Textarea(attrs={'cols': 30, 'rows': 1}),)


class ArizaForm(forms.Form):
    pk_no = forms.IntegerField(required=False, widget=forms.HiddenInput())
    proje = forms.ModelChoiceField(label='Proje..:', queryset=proje.objects.all())
    demirbas = forms.ModelChoiceField(label='Demirbaş Adı..:', queryset=demirbas.objects.all())
    ariza_adi = forms.CharField(label='Arıza Tanımı..:', max_length=100)
    servis = forms.ModelChoiceField(label='Servis Adı..:', queryset=servis.objects.all())
    yedek_parca_1 = forms.ModelChoiceField(label='Yedek parça -1........:', queryset=yedek_parca.objects.all(), required=False)
    yedek_parca_2 = forms.ModelChoiceField(label='Yedek parça -2........:', queryset=yedek_parca.objects.all(), required=False)
    yedek_parca_3 = forms.ModelChoiceField(label='Yedek parça -3........:', queryset=yedek_parca.objects.all(), required=False)
    yedek_parca_4 = forms.ModelChoiceField(label='Yedek parça -4........:', queryset=yedek_parca.objects.all(), required=False)
    yedek_parca_5 = forms.ModelChoiceField(label='Yedek parça -5........:', queryset=yedek_parca.objects.all(), required=False)
    kayit_acilis = forms.DateField(label='Kayıt açılış tarihi...:', required=True,
        widget=forms.TextInput(attrs={ 'class':'datepicker',})
        )
    kayit_kapanis = forms.DateField(label='Kayıt kapanış tarihi...:', required=True,
        widget=forms.TextInput(attrs={ 'class':'datepicker',})
        )
    tutar = forms.CharField(label='Tutarı..(TL).:')
    tutar_int = forms.IntegerField(required=False,widget=forms.HiddenInput())
    aciklama = forms.CharField(label='Açıklama', widget=forms.Textarea(attrs={'cols': 50, 'rows': 8}),)

    def __init__(self, *args, **kwargs):
        proje_no = kwargs.pop("proje_no")
        alt_kat = kwargs.pop("alt_kat")
        print("proje no init içinden...:", proje_no)
        print("demirbas - alt kategori... init içinden...:", alt_kat)
        super(ArizaForm, self).__init__(*args, **kwargs)
        self.fields['demirbas'].queryset = demirbas.objects.filter(proje=proje_no)
        self.fields['yedek_parca_1'].queryset = yedek_parca.objects.filter(alt_kategori=alt_kat)
        self.fields['yedek_parca_2'].queryset = yedek_parca.objects.filter(alt_kategori=alt_kat)
        self.fields['yedek_parca_3'].queryset = yedek_parca.objects.filter(alt_kategori=alt_kat)
        self.fields['yedek_parca_4'].queryset = yedek_parca.objects.filter(alt_kategori=alt_kat)
        self.fields['yedek_parca_5'].queryset = yedek_parca.objects.filter(alt_kategori=alt_kat)

    def clean(self):
        cleaned_data = super(ArizaForm, self).clean()
        cc_ariza_adi = cleaned_data.get("ariza_adi")
        cc_servis = cleaned_data.get("servis")
        cc_yedek_parca_1 = cleaned_data.get("yedek_parca_1")
        cc_yedek_parca_2 = cleaned_data.get("yedek_parca_2")
        cc_yedek_parca_3 = cleaned_data.get("yedek_parca_3")
        cc_yedek_parca_4 = cleaned_data.get("yedek_parca_4")
        cc_yedek_parca_5 = cleaned_data.get("yedek_parca_5")
        cc_kayit_acilis = cleaned_data.get("kayit_acilis")
        cc_kayit_kapanis = cleaned_data.get("kayit_kapanis")
        cc_tutar = cleaned_data.get("tutar")
        cc_tutar_int = cleaned_data.get("tutar_int")
        cc_aciklama = cleaned_data.get("aciklama")
        print (cc_ariza_adi, cc_servis, cc_tutar, cc_tutar_int, cc_aciklama,)
        print (cc_yedek_parca_1, cc_yedek_parca_2, cc_yedek_parca_3, cc_yedek_parca_4, cc_yedek_parca_5)
        print (cc_kayit_acilis, cc_kayit_kapanis)

        if cc_yedek_parca_1 == None :
            if ( not(cc_yedek_parca_2 == None) or not(cc_yedek_parca_3 == None) or not(cc_yedek_parca_4 == None) or not(cc_yedek_parca_5 == None)):
                raise forms.ValidationError(
                    " yedek parçaları sıralı girmelisiniz .... "
                )
        if cc_yedek_parca_2 == None :
            if ( not(cc_yedek_parca_3 == None) or not(cc_yedek_parca_4 == None) or not(cc_yedek_parca_5 == None)):
                raise forms.ValidationError(
                    " yedek parçaları sıralı girmelisiniz .... "
                )
        if cc_yedek_parca_3 == None:
            if ( not(cc_yedek_parca_4 == None) or not(cc_yedek_parca_5 == None)):
                raise forms.ValidationError(
                    " yedek parçaları sıralı girmelisiniz .... "
                )
        if cc_yedek_parca_4 == None:
            if ( not(cc_yedek_parca_5 == None)):
                raise forms.ValidationError(
                    " yedek parçaları sıralı girmelisiniz .... "
                )
        if (cc_kayit_acilis > cc_kayit_kapanis):
            raise forms.ValidationError(
                "açılış kapanış tarihleri hatalı....."
        )
        try:
            cc = int(cc_tutar_int)
        except:
            raise forms.ValidationError(" lütfen tutar alanına sayı giriniz.... ")



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
