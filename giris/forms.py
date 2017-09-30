from django import forms
from django.forms import ModelForm
from giris.models import marka, demirbas, proje, kategori, musteri
from django.contrib.admin.widgets import AdminDateWidget

#from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)

from bootstrap_datepicker.widgets import DatePicker


  #class ToDoForm(forms.Form):
    #  todo = forms.CharField(
    #      widget=forms.TextInput(attrs={"class": "form-control"}))
     # date = forms.DateField(
    #      widget=DatePicker(options={"format": "mm/dd/yyyy","autoclose": True}))


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





class DenemeForm(forms.Form):
    numarasi = forms.CharField(label="No:", required=True)
    projesi = forms.CharField(
        label="Projesi:", required=True)
    terih_alani = forms.DateField(
        widget=DatePicker(options={"format": "mm/dd/yyyy","autoclose": True}))

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'gir..', css_class='btn-primary'))



def DemirbasGirisForm(ModelForm):
    class Meta:
        model = demirbas
        fields = '__all__'
        #help_texts = { 'demirbasadi': _('lüften demirbaş adı giriniz..')}
        #initial={'garanti_bitis':'2020-06-06',}


def ProjeGirisForm(ModelForm):
    class Meta:
            model = proje
            fields = '__all__'
            labels = { 'proje_adi': _('Proje Adı')}
            help_texts = { 'proje_adi': _('lüften proje adı giriniz..')}



def MarkaGirisForm(ModelForm):
    class Meta:
            model = marka
            fields = ('marka_adi')
            labels = {
                "marka_adi": "Marka Adı"
                }
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
