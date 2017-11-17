from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from giris.models import marka, demirbas, kategori, proje, musteri, deneme_giris, yp_choice, dem_ariza, yparca_ariza, yparca_demirbas
from giris.models import grup, sirket, ekipman_turu, servis, alt_kategori, yedek_parca, hareket, ariza
from giris.forms import MarkaForm, DemirbasForm, KategoriForm, MusteriForm, ProjeForm, Demirbas_Ara_Form
from giris.forms import GrupForm, SirketForm, Ekipman_turuForm, ServisForm, Alt_kategoriForm, Yedek_parcaForm
from giris.forms import HareketForm, ArizaForm, Hareket_Ara_Form, Ariza_Ara_Form, Proje_SorForm, Proje_Dem_SorForm

from django.core import serializers
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.search import SearchVector
from django.views.generic import FormView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NameForm
import datetime
from datetime import date, datetime
from django.template.loader import render_to_string
import requests
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from django.core import serializers
from django.db.models import ProtectedError
from rest_framework import routers, serializers, viewsets







def deneme_picker(request):
    return render(request, 'deneme_picker.html')


def home(request):
    return render(request, 'ilk.html')


# deneme için yapılan nameform un çalıştırdığı view...
# javascript ile yparca_sec  entegrasyonu oluyor...

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            isim = request.POST.get('your_name', "")
            tarih = request.POST.get('tarih', "")
            kullanici = request.user
            print (isim, kullanici, tarih)
            #import pdb; pdb.set_trace()
            kaydetme_obj = deneme_giris(yazi = isim, user = kullanici, tarih = tarih)
            kaydetme_obj.save()
            text = form.cleaned_data["your_name"]
            #myQS = yedek_parca.objects.none()
            form = NameForm(selected_alt=None)
            messages.success(request, 'Başarıyla kaydetti....')
            return redirect('get_name')
        else:
            return render(request, 'name.html', {'form': form})


    # if a GET (or any other method) we'll create a blank form
    else:
        selected_alt = request.session.get('selected_alt')
        form = NameForm(selected_alt=selected_alt)
        deneme_giris_QS = deneme_giris.objects.all().order_by('-tarih')
        args = {'form': form, 'deneme_giris_QS': deneme_giris_QS}
        #import pdb; pdb.set_trace()
        return render(request, 'name.html', args)



# deneme için nameform ile birlikte...
# javascript sonrasında çalışan kod....

def yparca_sec(request):
    print("selam buraya geldik.... yparca_sec")
    response_data ={}
    yparca_demirbas.objects.filter(kullanici=request.user.id).delete()
    print("hepsi silindi, liste...:")
    if request.method == 'GET':
        aj_adi = str(request.GET.get('aj_tarihi', None))
        aj_tarihi = request.GET.get('aj_tarihi', None)
        selected = request.GET.get('selected', None)
        aj_gizli = request.GET.get('aj_gizli', None)
        print("aj_adi...:", aj_adi)
        print("aj_tarihi...:", aj_tarihi)
        print("selected...:", selected)
        print("aj_gizli", aj_gizli)
        if selected != None:
            obj = demirbas.objects.get(id=selected)
            selected_altkat = obj.alt_kategori
            selected_alt = alt_kategori.objects.get(alt_kategori_adi=selected_altkat).id
            print("selected_altkat", selected_altkat)
            print("selected_alt aktarım için...", selected_alt)
            obj2 = yedek_parca.objects.filter(alt_kategori=selected_altkat)
            print("obj2...:", obj2)
            print(request.user.id)

            for yedek_parca.yparca_adi in obj2:
                print("yedek parça...:", yedek_parca.yparca_adi)
                kaydetme_obj = yparca_demirbas(yparca_demirbas = yedek_parca.yparca_adi,
                                               kullanici_id = request.user.id)
                kaydetme_obj.save()

            response_data = list(obj2)
            print("response data 1111...:", response_data)
            request.session['selected_alt'] = selected_alt
            form = NameForm(selected_alt=selected_alt)
            if not (aj_gizli == "A"):
                form.fields["gizli"].initial = "A"
                print("gizlice bas onu...:", form.fields["gizli"].initial)
            form.fields["your_name"].initial = aj_adi
            form.fields["tarih"].initial = aj_tarihi
            form.fields["demirbas"].initial = selected
            print("sonca...demce....:", form.fields["yedek_parca"].queryset )
            args = {'form': form,}

    print ("son noktaya geliyor mu acaba", response_data)
    return HttpResponse(response_data, content_type='application/json')




#  esas kodlama buradan başlıyor denemeler yukarıda......


@login_required
def index(request):
    num_demirbas=demirbas.objects.all().count()
    num_proje=proje.objects.all().count()
    num_marka=marka.objects.count()
    num_kategori=kategori.objects.all().count()
    num_alt_kategori=alt_kategori.objects.all().count()
    num_musteri=musteri.objects.count()
    num_grup=grup.objects.all().count()
    num_sirket=sirket.objects.all().count()
    num_ekipman_turu=ekipman_turu.objects.count()
    num_servis=servis.objects.all().count()
    num_yedek_parca=yedek_parca.objects.all().count()
    num_hareket=hareket.objects.count()
    num_ariza=ariza.objects.count()

    return render(request, 'ana_menu.html',
        context={'num_demirbas':num_demirbas,'num_proje':num_proje,'num_marka':num_marka,'num_kategori':num_kategori, 'num_alt_kategori':num_alt_kategori,
        'num_musteri':num_musteri, 'num_grup': num_grup, 'num_sirket': num_sirket, 'num_ekipman_turu': num_ekipman_turu,
        'num_servis': num_servis, 'num_yedek_parca': num_yedek_parca, 'num_hareket': num_hareket, 'num_ariza': num_ariza},
    )




#demirbaş yaratma işlemi .......

@login_required
def demirbas_yarat(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DemirbasForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            dd_demirbasadi = request.POST.get('adi', "")
            dd_proje = request.POST.get('proje', "")
            dd_bolum = request.POST.get('bolum', "")
            dd_marka = request.POST.get('marka', "")
            dd_ekipman_turu = request.POST.get('ekipman_turu', "")
            dd_alt_kategori = request.POST.get('alt_kategori', "")
            dd_modeli = request.POST.get('modeli', "")
            dd_durumu = request.POST.get('durumu', "")
            dd_kullanim_durumu = "K"
            dd_kimin = request.POST.get('kimin', "")
            dd_garanti_varmi = request.POST.get('garanti_varmi', "")
            dd_garanti_bitis = request.POST.get('garanti_bitis', "")
            dd_amts_kalanyil = request.POST.get('amts_kalanyil', "")
            dd_bedeli = request.POST.get('bedeli', "")
            dd_bedeli_int = request.POST.get('bedeli_int', "")
            dd_aciklama = request.POST.get('aciklama', "")
            kullanan = request.user.id
            yaratildi = datetime.now()
            if dd_garanti_bitis == "":
                dd_garanti_bitis = "2000-01-01"
            print ("demirbasadi", dd_demirbasadi)
            print ("proje", dd_proje)
            print ("bölüm", dd_bolum)
            print ("marka", dd_marka)
            print ("ekipman_turu", dd_ekipman_turu)
            print ("alt_kategori", dd_alt_kategori)
            print ("modeli", dd_modeli)
            print ("durumu", dd_durumu)
            print ("kimin", dd_kimin)
            print ("kullanım durumu", dd_kullanim_durumu)
            print ("garanti_varmi", dd_garanti_varmi)
            print ("garanti_bitis", dd_garanti_bitis)
            print ("amts_kalanyil", dd_amts_kalanyil)
            print ("bedeli", dd_bedeli)
            print ("bedeli_int", dd_bedeli_int)
            print ("aciklama", dd_aciklama)
            print ("kullanan", kullanan)
            print ("yaratildi", yaratildi)
            #import pdb; pdb.set_trace()
            kaydetme_obj = demirbas(demirbasadi = dd_demirbasadi, proje_id = dd_proje,  bolum = dd_bolum,
                marka_id = dd_marka, ekipman_turu_id = dd_ekipman_turu, alt_kategori_id = dd_alt_kategori,
                modeli = dd_modeli, durum = dd_durumu, kimin = dd_kimin,  gar_varmi = dd_garanti_varmi,
                garanti_bitis = dd_garanti_bitis, amts_kalanyil = dd_amts_kalanyil, env_bedeli = dd_bedeli_int,
                aciklama = dd_aciklama, kullanan_id = kullanan, yaratildi = yaratildi, kullanim_durumu = dd_kullanim_durumu)
            kaydetme_obj.save()
            form = DemirbasForm()
            messages.success(request, 'Başarıyla kaydetti....')
            return redirect('demirbas_yarat')
        else:
            return render(request, 'giris/demirbas_yarat.html', {'form': form})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = DemirbasForm()
        #deneme_giris_QS = deneme_giris.objects.all().order_by('-tarih')
        #args = {'form': form, 'deneme_giris_QS': deneme_giris_QS}
        #return render(request, '/giris/demirbas_yarat.html', args)
        return render(request, 'giris/demirbas_yarat.html', {'form': form})




@login_required
def secili_proje(request, pk=None):
    demirbas_proje_list = demirbas.objects.filter(proje=pk)
    print("ilk şeçilen demirbaşlar...", demirbas_proje_list)
    demirbas_proje_list = demirbas_proje_list.filter(kullanim_durumu="K")
    print("seçilen demirbaşları listele bakalım...", demirbas_proje_list)
    request.session['secili_proje'] = pk
    return render(request, 'giris/demirbas_proje_list.html', {'demirbas_proje_list': demirbas_proje_list,})


@login_required
def depo_listesi(request, pk=None):
    demirbas_depo_list = demirbas.objects.filter(kullanim_durumu="D")
    print("depodaki demirbaşlar listele bakalım...", demirbas_depo_list)
    return render(request, 'giris/demirbas_depo_list.html', {'demirbas_depo_list': demirbas_depo_list})


@login_required
def demirbas_depo_detail(request, pk=None):
    demirbas_obj = demirbas.objects.filter(id=pk)
    print("depodaki demirbaş ......", demirbas_obj)
    return render(request, 'giris/demirbas_depo_detail.html', {'demirbas_obj': demirbas_obj})



@login_required
def demirbas_guncelle(request, pk=None):
    obje = get_object_or_404(demirbas, pk=pk)
    print("guncelle", pk)
    print(obje)
    print(obje.proje)
    print(obje.bolum)
    print("...........")
    print(request.user)
    print(request.user.id)

    if request.method == 'POST':
        print("post  .....", pk)
        form = DemirbasForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            dd_demirbasadi = request.POST.get('adi', "")
            dd_proje = request.POST.get('proje', "")
            dd_bolum = request.POST.get('bolum', "")
            dd_marka = request.POST.get('marka', "")
            dd_ekipman_turu = request.POST.get('ekipman_turu', "")
            dd_alt_kategori = request.POST.get('alt_kategori', "")
            dd_modeli = request.POST.get('modeli', "")
            dd_durumu = request.POST.get('durumu', "")
            dd_kimin = request.POST.get('kimin', "")
            dd_garanti_varmi = request.POST.get('garanti_varmi', "")
            dd_garanti_bitis = request.POST.get('garanti_bitis', "")
            dd_amts_kalanyil = request.POST.get('amts_kalanyil', "")
            dd_bedeli = request.POST.get('bedeli', "")
            dd_bedeli_int = request.POST.get('bedeli_int', "")
            dd_aciklama = request.POST.get('aciklama', "")
            kullanan = request.user.id
            yaratildi = datetime.now()
            if dd_garanti_bitis == "":
                dd_garanti_bitis = "2000-01-01"
            print ("demirbasadi", dd_demirbasadi)
            print ("proje", dd_proje)
            print ("bölüm", dd_bolum)
            print ("marka", dd_marka)
            print ("ekipman_turu", dd_ekipman_turu)
            print ("alt_kategori", dd_alt_kategori)
            print ("modeli", dd_modeli)
            print ("durumu", dd_durumu)
            print ("kimin", dd_kimin)
            print ("garanti_varmi", dd_garanti_varmi)
            print ("garanti_bitis", dd_garanti_bitis)
            print ("amts_kalanyil", dd_amts_kalanyil)
            print ("bedeli", dd_bedeli)
            print ("bedeli_int", dd_bedeli_int)
            print ("aciklama", dd_aciklama)
            print ("kullanan", kullanan)
            print ("yaratildi", yaratildi)
            #import pdb; pdb.set_trace()
            kaydetme_obj = demirbas(id=pk,
                                    demirbasadi = dd_demirbasadi,
                                    proje_id = dd_proje,
                                    bolum = dd_bolum,
                                    marka_id = dd_marka,
                                    ekipman_turu_id = dd_ekipman_turu,
                                    alt_kategori_id = dd_alt_kategori,
                                    modeli = dd_modeli,
                                    durum = dd_durumu,
                                    kullanim_durumu = "K",
                                    kimin = dd_kimin,
                                    gar_varmi = dd_garanti_varmi,
                                    garanti_bitis = dd_garanti_bitis,
                                    amts_kalanyil = dd_amts_kalanyil,
                                    env_bedeli = dd_bedeli_int,
                                    aciklama = dd_aciklama,
                                    kullanan_id = kullanan,
                                    yaratildi = yaratildi)
            kaydetme_obj.save()
            messages.success(request, 'Başarıyla güncelledi....')
            return redirect('demirbas')
        else:
            return render(request, 'giris/demirbas_yarat.html', {'form': form})


    else:
        print("get .....", pk)
        print("obje.id...:", obje.id)
        form = DemirbasForm()
        form.fields["pk_no"].initial = obje.id
        form.fields["adi"].initial = obje.demirbasadi
        form.fields["proje"].initial = obje.proje
        form.fields["bolum"].initial = obje.bolum
        form.fields["marka"].initial = obje.marka
        form.fields["ekipman_turu"].initial = obje.ekipman_turu
        form.fields["alt_kategori"].initial = obje.alt_kategori
        form.fields["modeli"].initial = obje.modeli
        form.fields["durumu"].initial = obje.durum
        form.fields["garanti_varmi"].initial = obje.gar_varmi
        if obje.gar_varmi == "E":
            form.fields["garanti_bitis"].initial = obje.garanti_bitis
        else:
            form.fields["garanti_bitis"].initial = ""
        form.fields["amts_kalanyil"].initial = obje.amts_kalanyil
        form.fields["bedeli"].initial = obje.env_bedeli
        form.fields["bedeli_int"].initial = obje.env_bedeli
        form.fields["aciklama"].initial = obje.aciklama

        args = {'form': form,}
        return render(request, 'giris/demirbas_yarat.html', args)





@login_required
def demirbas_p_guncelle(request, pk=None):
    obje = get_object_or_404(demirbas, pk=pk)
    print("guncelle", pk)
    print(obje)
    print(obje.proje)
    print(obje.bolum)
    print("...........")
    print(request.user)
    print(request.user.id)

    if request.method == 'POST':
        print("post  .....", pk)
        form = DemirbasForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            dd_demirbasadi = request.POST.get('adi', "")
            dd_proje = request.POST.get('proje', "")
            dd_bolum = request.POST.get('bolum', "")
            dd_marka = request.POST.get('marka', "")
            dd_ekipman_turu = request.POST.get('ekipman_turu', "")
            dd_alt_kategori = request.POST.get('alt_kategori', "")
            dd_modeli = request.POST.get('modeli', "")
            dd_durumu = request.POST.get('durumu', "")
            dd_kimin = request.POST.get('kimin', "")
            dd_garanti_varmi = request.POST.get('garanti_varmi', "")
            dd_garanti_bitis = request.POST.get('garanti_bitis', "")
            dd_amts_kalanyil = request.POST.get('amts_kalanyil', "")
            dd_bedeli = request.POST.get('bedeli', "")
            dd_bedeli_int = request.POST.get('bedeli_int', "")
            dd_aciklama = request.POST.get('aciklama', "")
            kullanan = request.user.id
            yaratildi = datetime.now()
            if dd_garanti_bitis == "":
                dd_garanti_bitis = "2000-01-01"
            print ("demirbasadi", dd_demirbasadi)
            print ("proje", dd_proje)
            print ("bölüm", dd_bolum)
            print ("marka", dd_marka)
            print ("ekipman_turu", dd_ekipman_turu)
            print ("alt_kategori", dd_alt_kategori)
            print ("modeli", dd_modeli)
            print ("durumu", dd_durumu)
            print ("kimin", dd_kimin)
            print ("garanti_varmi", dd_garanti_varmi)
            print ("garanti_bitis", dd_garanti_bitis)
            print ("amts_kalanyil", dd_amts_kalanyil)
            print ("bedeli", dd_bedeli)
            print ("bedeli_int", dd_bedeli_int)
            print ("aciklama", dd_aciklama)
            print ("kullanan", kullanan)
            print ("yaratildi", yaratildi)
            #import pdb; pdb.set_trace()
            kaydetme_obj = demirbas(id=pk,
                                    demirbasadi = dd_demirbasadi,
                                    proje_id = dd_proje,
                                    bolum = dd_bolum,
                                    marka_id = dd_marka,
                                    ekipman_turu_id = dd_ekipman_turu,
                                    alt_kategori_id = dd_alt_kategori,
                                    modeli = dd_modeli,
                                    durum = dd_durumu,
                                    kullanim_durumu = "K",
                                    kimin = dd_kimin,
                                    gar_varmi = dd_garanti_varmi,
                                    garanti_bitis = dd_garanti_bitis,
                                    amts_kalanyil = dd_amts_kalanyil,
                                    env_bedeli = dd_bedeli_int,
                                    aciklama = dd_aciklama,
                                    kullanan_id = kullanan,
                                    yaratildi = yaratildi)
            kaydetme_obj.save()
            messages.success(request, 'Başarıyla güncelledi....')
            secili_proje = request.session.get('secili_proje')
            return redirect('/giris/demirbas/proje/'+secili_proje)
            #return render(request, 'giris/demirbas/proje/'+secili_proje,)
        else:
            return render(request, 'giris/demirbas_yarat.html', {'form': form})


    else:
        print("get .....", pk)
        print("obje.id...:", obje.id)
        form = DemirbasForm()
        form.fields["pk_no"].initial = obje.id
        form.fields["adi"].initial = obje.demirbasadi
        form.fields["proje"].initial = obje.proje
        form.fields["bolum"].initial = obje.bolum
        form.fields["marka"].initial = obje.marka
        form.fields["ekipman_turu"].initial = obje.ekipman_turu
        form.fields["alt_kategori"].initial = obje.alt_kategori
        form.fields["modeli"].initial = obje.modeli
        form.fields["durumu"].initial = obje.durum
        form.fields["garanti_varmi"].initial = obje.gar_varmi
        if obje.gar_varmi == "E":
            form.fields["garanti_bitis"].initial = obje.garanti_bitis
        else:
            form.fields["garanti_bitis"].initial = ""
        form.fields["amts_kalanyil"].initial = obje.amts_kalanyil
        form.fields["bedeli"].initial = obje.env_bedeli
        form.fields["bedeli_int"].initial = obje.env_bedeli
        form.fields["aciklama"].initial = obje.aciklama

        args = {'form': form,}
        return render(request, 'giris/demirbas_yarat.html', args)





@login_required
def demirbas_sil(request, pk=None):
    print("demirbaş sildeki pk:", pk)
    object = get_object_or_404(demirbas, pk=pk)
    sil_demirbas = object.demirbasadi
    sil_id = object.id
    har_obje = hareket.objects.filter(demirbas_id=object.id)
    ar_obje = ariza.objects.filter(demirbas=object.id)
    har_count = har_obje.count()
    ar_count = ar_obje.count()
    print(" hareket......", har_count)
    print(" ariza.....", ar_count)
    if har_count != 0 or ar_count != 0:
        return render(request, 'giris/demirbas_silemezsin.html',)
    print("sil_demirbas", sil_demirbas)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_demirbas': sil_demirbas, 'pk': pk,}
    return render(request, 'giris/demirbas_sil_soru.html', args)


@login_required
def demirbas_sil_kesin(request, pk=None):
    print("demirbaş sil kesindeki pk:", pk)
    object = get_object_or_404(demirbas, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        return JsonResponse(error_message)
    messages.success(request, 'Başarıyla silindi....')
    return redirect('demirbas')


@login_required
def demirbas_p_sil(request, pk=None):
    print("demirbaş p sildeki pk:", pk)
    object = get_object_or_404(demirbas, pk=pk)
    sil_demirbas = object.demirbasadi
    sil_id = object.id
    har_obje = hareket.objects.filter(demirbas_id=object.id)
    ar_obje = ariza.objects.filter(demirbas=object.id)
    har_count = har_obje.count()
    ar_count = ar_obje.count()
    print(" hareket......", har_count)
    print(" ariza.....", ar_count)
    secili_proje = request.session.get('secili_proje')
    args = {'secili_proje' : secili_proje}
    if har_count != 0 or ar_count != 0:
        return render(request, 'giris/demirbas_p_silemezsin.html', args)
    print("sil_demirbas", sil_demirbas)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_demirbas': sil_demirbas, 'pk': pk,}
    return render(request, 'giris/demirbas_sil_soru.html', args)


@login_required
def demirbas_p_sil_kesin(request, pk=None):
    print("demirbaş sil kesindeki pk:", pk)
    object = get_object_or_404(demirbas, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        return JsonResponse(error_message)
    messages.success(request, 'Başarıyla silindi....')
    secili_proje = request.session.get('secili_proje')
    return redirect('/giris/demirbas/proje/'+secili_proje)





@login_required
def demirbas_ara(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Demirbas_Ara_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            arama = request.POST.get('alan', "")
            print (arama)
            demirbas_arama_filtresi = demirbas.objects.annotate(search=SearchVector('demirbasadi'),).filter(search=arama)
            return render(request, 'giris/demirbas_arm_list.html', {'demirbas_arama_filtresi': demirbas_arama_filtresi},)
        else:
            return render(request, 'giris/demirbas_arm_list.html', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = Demirbas_Ara_Form()
        return render(request, 'giris/demirbas_ara.html', {'form': form})




# neden yaptım bilmiyorum ,  bakalım nasıl gelişecek...
class demirbas_sec(forms.TextInput):
    class Media:
        print("demirbas_sec class...:")
        js = ('giris/js/dem_sec.js')







# javascript ile çalışan kod ,  garanti seçeneği hayır ise garanti süresi alanını kapatıyor..

def demirbas_garanti(request):
    print("selam buraya geldik.... demirbas garanti")
    response_data ={}
    if request.method == 'GET':
        garanti_varmi = str(request.GET.get('garanti_varmi', None))
        print("garanti_varmi...:", garanti_varmi)
        form = DemirbasForm()
        if garanti_varmi == "H":
            form.fields["garanti_bitis"].widget = forms.HiddenInput()
            print("garanti_varmi ....hhhhh:", )
            args = {'form': form,}
        else:
            form.fields["garanti_bitis"].widget = forms.TextInput()
            print("garanti_varmi ....eeeee:", )
            args = {'form': form,}
    print ("son noktaya geliyor mu acaba", response_data)
    return HttpResponse(response_data, content_type='application/json')







#hareket  yaratma işlemi .......

@login_required
def hareket_yarat(request, pk=None):
    obje = get_object_or_404(demirbas, pk=pk)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HareketForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            dd_demirbas_id = obje.id
            dd_demirbas_adi = obje.demirbasadi
            #dd_har_tipi = request.POST.get('har_tipi', "")
            dd_mevcut_proj_id = obje.proje.id
            dd_mevcut_proj = obje.proje
            dd_sonraki_proj = request.POST.get('sonraki_proj', "")
            dd_aciklama = request.POST.get('aciklama', "")
            kullanan = request.user.id
            yaratildi = datetime.now()
            print ("demirbas_id", dd_demirbas_id)
            print ("demirbas_adi", dd_demirbas_adi)
            #print ("har tipi", dd_har_tipi)
            print ("mevcut_proj_id", dd_mevcut_proj_id)
            print ("sonraki_proj", dd_sonraki_proj)
            print ("aciklama", dd_aciklama)
            print ("kullanan", kullanan)
            print ("yaratildi", yaratildi)


            if str(dd_mevcut_proj_id) == str(dd_sonraki_proj):
                        deneme_1 = obje.id
                        deneme_2 = obje.demirbasadi
                        deneme_3 = obje.proje
                        deneme_4 = "iki proje aynı olamaz...."
                        form = HareketForm()
                        form.fields["hidd_proje"].initial = obje.proje
                        form.fields["dem_id"].initial = obje.id
                        form.fields["dem_adi"].initial = obje.demirbasadi
                        form.fields["dem_proj"].initial = obje.proje
                        #form.fields["har_tipi"].initial = dd_har_tipi
                        form.fields["sonraki_proj"].initial = dd_sonraki_proj
                        form.fields["aciklama"].initial = dd_aciklama
                        args = {'form': form, 'deneme_1': deneme_1, 'deneme_2': deneme_2, 'deneme_3': deneme_3, 'deneme_4': deneme_4 }
                        return render(request, 'giris/hareket_yarat.html', args)


            obje_demirbas = get_object_or_404(demirbas, pk=pk)


            kaydetme_obj = hareket(demirbas_id_id = obje_demirbas.id,
                                   demirbas_adi = obje_demirbas.demirbasadi,
                                   har_tipi = "T",
                                   mevcut_proj_id = dd_mevcut_proj_id,
                                   sonraki_proj_id = dd_sonraki_proj,
                                   aciklama = dd_aciklama,
                                   kullanan_id = kullanan,
                                   yaratildi = yaratildi,)
            kaydetme_obj.save()
            dem_kaydet_obj = demirbas(id=obje_demirbas.id,
                                      demirbasadi = obje_demirbas.demirbasadi,
                                      proje_id = dd_sonraki_proj,
                                      bolum = obje_demirbas.bolum,
                                      marka_id = obje_demirbas.marka,
                                      ekipman_turu_id = obje_demirbas.ekipman_turu,
                                      alt_kategori_id = obje_demirbas.alt_kategori,
                                      modeli = obje_demirbas.modeli,
                                      durum = obje_demirbas.durum,
                                      kullanim_durumu = "K",
                                      gar_varmi = obje_demirbas.gar_varmi,
                                      garanti_bitis = obje_demirbas.garanti_bitis,
                                      amts_kalanyil = obje_demirbas.amts_kalanyil,
                                      env_bedeli = obje_demirbas.env_bedeli,
                                      aciklama = obje_demirbas.aciklama,
                                      kullanan = obje_demirbas.kullanan,
                                      yaratildi = obje_demirbas.yaratildi,)

            dem_kaydet_obj.save()
            #text = form.cleaned_data["demirbasadi"]
            form = HareketForm()
            #args = {'form': form, 'text': text}
            #return render(request, 'name.html', args)
            messages.success(request, 'Başarıyla kaydetti....')
            return redirect('proje_dem_sor')
        else:
            return render(request, 'giris/hareket_yarat.html', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
    # for GET ....form is intialized
        print ("en başta pk yı doğru alıyor mu ???..", pk)
        deneme_1 = obje.id
        deneme_2 = obje.demirbasadi
        deneme_3 = obje.proje
        deneme_4 = ""
        form = HareketForm()
        form.fields["hidd_proje"].initial = obje.proje
        form.fields["dem_id"].initial = obje.id
        form.fields["dem_adi"].initial = obje.demirbasadi
        form.fields["dem_proj"].initial = obje.proje
        args = {'form': form, 'deneme_1': deneme_1, 'deneme_2': deneme_2, 'deneme_3': deneme_3, 'deneme_4': deneme_4}
        return render(request, 'giris/hareket_yarat.html', args)




@login_required
def depodan_geri(request, pk=None):
    obje = get_object_or_404(demirbas, pk=pk)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HareketForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            dd_demirbas_id = obje.id
            dd_demirbas_adi = obje.demirbasadi
            #dd_har_tipi = request.POST.get('har_tipi', "")
            dd_mevcut_proj_id = obje.proje.id
            dd_mevcut_proj = obje.proje
            dd_sonraki_proj = request.POST.get('sonraki_proj', "")
            dd_aciklama = request.POST.get('aciklama', "")
            kullanan = request.user.id
            yaratildi = datetime.now()
            print ("demirbas_id", dd_demirbas_id)
            print ("demirbas_adi", dd_demirbas_adi)
            #print ("har tipi", dd_har_tipi)
            print ("mevcut_proj_id", dd_mevcut_proj_id)
            print ("sonraki_proj", dd_sonraki_proj)
            print ("aciklama", dd_aciklama)
            print ("kullanan", kullanan)
            print ("yaratildi", yaratildi)


            obje_demirbas = get_object_or_404(demirbas, pk=pk)


            kaydetme_obj = hareket(demirbas_id_id = obje_demirbas.id,
                                   demirbas_adi = obje_demirbas.demirbasadi,
                                   har_tipi = "T",
                                   mevcut_proj_id = dd_mevcut_proj_id,
                                   sonraki_proj_id = dd_sonraki_proj,
                                   aciklama = dd_aciklama,
                                   kullanan_id = kullanan,
                                   yaratildi = yaratildi,)
            kaydetme_obj.save()
            dem_kaydet_obj = demirbas(id=obje_demirbas.id,
                                      demirbasadi = obje_demirbas.demirbasadi,
                                      proje_id = dd_sonraki_proj,
                                      bolum = obje_demirbas.bolum,
                                      marka_id = obje_demirbas.marka,
                                      ekipman_turu_id = obje_demirbas.ekipman_turu,
                                      alt_kategori_id = obje_demirbas.alt_kategori,
                                      modeli = obje_demirbas.modeli,
                                      durum = obje_demirbas.durum,
                                      kullanim_durumu = "K",
                                      gar_varmi = obje_demirbas.gar_varmi,
                                      garanti_bitis = obje_demirbas.garanti_bitis,
                                      amts_kalanyil = obje_demirbas.amts_kalanyil,
                                      env_bedeli = obje_demirbas.env_bedeli,
                                      aciklama = obje_demirbas.aciklama,
                                      kullanan = obje_demirbas.kullanan,
                                      yaratildi = obje_demirbas.yaratildi,)

            dem_kaydet_obj.save()
            #text = form.cleaned_data["demirbasadi"]
            form = HareketForm()
            #args = {'form': form, 'text': text}
            #return render(request, 'name.html', args)
            messages.success(request, 'Başarıyla kaydetti....')
            return redirect('proje_sor')
        else:
            return render(request, 'giris/hareket_yarat.html', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
    # for GET ....form is intialized
        print ("en başta pk yı doğru alıyor mu ???..", pk)
        deneme_1 = obje.id
        deneme_2 = obje.demirbasadi
        deneme_3 = obje.proje
        deneme_4 = ""
        form = HareketForm()
        form.fields["hidd_proje"].initial = obje.proje
        form.fields["dem_id"].initial = obje.id
        form.fields["dem_adi"].initial = obje.demirbasadi
        form.fields["dem_proj"].initial = obje.proje
        args = {'form': form, 'deneme_1': deneme_1, 'deneme_2': deneme_2, 'deneme_3': deneme_3, 'deneme_4': deneme_4}
        return render(request, 'giris/hareket_yarat.html', args)








@login_required
def hareket_guncelle(request, pk=None):
    obje = get_object_or_404(hareket, pk=pk)
    form = HareketForm(request.POST or None, request.FILES or None,)
    if request.method == 'POST':
        if form.is_valid():
            dd_demirbas_id = request.POST.get('demirbas_id', "")
            dd_demirbas_adi = request.POST.get('demirbas_adi', "")
            dd_har_tipi = request.POST.get('har_tipi', "")
            dd_mevcut_proj = request.POST.get('mevcut_proj', "")
            dd_sonraki_proj = request.POST.get('sonraki_proj', "")
            dd_aciklama = request.POST.get('aciklama', "")
            kullanici = request.user.id
            yaratildi = datetime.now()
            print ("demirbaş_id", demirbas_id)
            print ("demirbas_adi", dd_demirbas_adi)
            print ("har tipi", dd_har_tipi)
            print ("mevcut_proj", dd_mevcut_proj)
            print ("sonraki_proj", dd_sonraki_proj)
            print ("aciklama", dd_aciklama)
            print ("kullanan", kullanan)
            print ("yaratildi", yaratildi)
            #import pdb; pdb.set_trace()
            kaydetme_obj = hareket(id=pk,
                                   demirbas_id_id = dd_demirbas_id,
                                   demirbas_adi = dd_demirbas_adi,
                                   har_tipi = dd_har_tipi,
                                   mevcut_proj_id = dd_mevcut_proj,
                                   sonraki_proj_id = dd_sonraki_proj,
                                   aciklama = dd_aciklama,
                                   kullanan = kullanan,
                                   yaratildi = yaratildi)
            kaydetme_obj.save()
            messages.success(request, 'Başarıyla güncelledi....')
            return redirect('hareket')
        else:
            return render(request, 'giris/hareket_list.html', {'form': form})
    else:
        form = HareketForm()
        form.fields["dem_id"].initial = obje.demirbas_id
        form.fields["dem_adi"].initial = obje.demirbas_adi
        form.fields["har_tipi"].initial = obje.har_tipi
        form.fields["dem_proj"].initial = obje.mevcut_proj
        form.fields["sonraki_proj"].initial = obje.sonraki_proj
        form.fields["aciklama"].initial = obje.aciklama
        return render(request, 'giris/hareket_list.html', {'form': form})



@login_required
def hareket_sil(request, object_id):
    return render(request, 'hareket_sil_soru.html')





@login_required
def hareket_sil_kesin(request, object_id):
    object = get_object_or_404(Model, pk=object_id)
    try:
        object.delete()
    except ProtectedError:
        error_message = "Veri bağlantıları nedeniyle silinemez..."
        return JsonResponse(error_message)
    messages.success(request, 'Başarıyla silindi....')
    return redirect('hareket')




@login_required
def hareket_ara(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Hareket_Ara_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            arama = request.POST.get('alan', "")
            print (arama)
            hareket_arama_filtresi = hareket.objects.annotate(search=SearchVector('aciklama'),).filter(search=arama)
            return render(request, 'giris/hareket_arm_list.html', {'hareket_arama_filtresi': hareket_arama_filtresi},)
        else:
            return render(request, 'giris/hareket_arm_list.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Hareket_Ara_Form()
        return render(request, 'giris/hareket_ara.html', {'form': form})






# hareket - taşıma işleminden önce proje ve demirbaş bilgisi alıyor...







def proje_dem_sor(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        proje_no = request.session['proje_no']
        print ("hangi proje ...:", proje_no)
        form = Proje_Dem_SorForm(request.POST, proje_no=proje_no)
        # check whether it's valid:
        if form.is_valid():
            hangi_dem = request.POST.get('hangi_dem', "")
            print ("hangi dem ...:", hangi_dem)
            #form = Proje_Dem_SorForm(proje_sor=proje_sor)
            args = {'form': form, 'proje_sor': proje_sor, 'hangi_dem': hangi_dem}
            #return render(request, 'giris/ariza_yarat.html', args)
            #return redirect('get_name')
            #return render(request, 'giris/hareket/yarat/?value=hangi_dem', args)
            return render(request, "giris/hareket/yarat/5", args)
        else:
            return render(request, 'giris/proje_dem_sor.html', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
        proje_no = request.session.get('proje_no')
        form = Proje_Dem_SorForm(proje_no=proje_no)
        form.fields["hangi_proje"].initial = proje_no
        args = {'form': form, }
        return render(request, 'giris/proje_dem_sor.html', args)





def deneme(request):
    print("selam buraya geldik.... demirbas listesi")
    print("User.id.....:", request.user.id)
    response_data ={}
    if request.method == 'GET':
        selected = request.GET.get('selected', None)
        print("selected...:", selected)
        if selected != None:
            request.session['proje_no'] = selected
            request.session.modified = True
            print("yetti artık....neden doğru yazmıyor...:", request.session['proje_no'])
            form = Proje_Dem_SorForm(proje_no=selected)
    print ("son nokta demirbas arıza listesi....", response_data)
    return HttpResponse(response_data, content_type='application/json')







def proje_sor(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Proje_SorForm(request.POST, proje_no=proje_no)
        # check whether it's valid:
        if form.is_valid():
            hangi_proje = request.POST.get('hangi_proje', "")
            print ("hangi proje ...:", hangi_proje)
            #form = Proje_Dem_SorForm(proje_sor=proje_sor)
            args = {'form': form,  'hangi_proje': hangi_proje}

            return render(request, "giris/proje_sor/", args)
        else:
            return render(request, 'giris/proje_sor.html', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:

        form = Proje_SorForm()
        args = {'form': form, }
        return render(request, 'giris/proje_sor.html', args)








#ariza yaratma işlemi .......

@login_required
def ariza_yarat(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        proje_no = request.session['ab_proje_no']
        alt_kat = request.session['alt_kat']
        form = ArizaForm(request.POST, proje_no=proje_no, alt_kat=alt_kat)
        # check whether it's valid:
        if form.is_valid():
            dd_proje = request.POST.get('proje',"")
            dd_demirbas = request.POST.get('demirbas', "")
            dd_ariza_adi = request.POST.get('ariza_adi', "")
            dd_servis = request.POST.get('servis', "")
            dd_yedek_parca_1 = request.POST.get('yedek_parca_1', "")
            dd_yedek_parca_2 = request.POST.get('yedek_parca_2', "")
            dd_yedek_parca_3 = request.POST.get('yedek_parca_3', "")
            dd_yedek_parca_4 = request.POST.get('yedek_parca_4', "")
            dd_yedek_parca_5 = request.POST.get('yedek_parca_5', "")
            dd_tutar = request.POST.get('tutar', "")
            dd_tutar_int = request.POST.get('tutar_int', "")
            dd_aciklama = request.POST.get('aciklama', "")
            kullanan = request.user.id
            yaratildi = datetime.now()
            print ("proje", dd_proje)
            print ("demirbaş", dd_demirbas)
            print ("ariza adı", dd_ariza_adi)
            print ("servis", dd_servis)
            print ("yedek parça 1", dd_yedek_parca_1)
            print ("yedek parça 2", dd_yedek_parca_2)
            print ("yedek parça 3", dd_yedek_parca_3)
            print ("yedek parça 4", dd_yedek_parca_4)
            print ("yedek parça 5", dd_yedek_parca_5)
            print ("tutar", dd_tutar)
            print ("tutar_int", dd_tutar_int)
            print ("aciklama", dd_aciklama)
            print ("kullanan", kullanan)
            print ("yaratildi", yaratildi)

            kaydetme_obj = ariza(ariza_adi = dd_ariza_adi,
                                 proje_id = dd_proje,
                                 demirbas_id = dd_demirbas,
                                 servis_id = dd_servis,
                                 yedek_parca_1_id = dd_yedek_parca_1,
                                 yedek_parca_2_id = dd_yedek_parca_2,
                                 yedek_parca_3_id = dd_yedek_parca_3,
                                 yedek_parca_4_id = dd_yedek_parca_4,
                                 yedek_parca_5_id = dd_yedek_parca_5,
                                 tutar = dd_tutar_int,
                                 aciklama = dd_aciklama,
                                 kullanan_id = kullanan,
                                 yaratildi = yaratildi)
            kaydetme_obj.save()
            request.session['ab_proje_no'] = None
            request.session['js_demirbas'] = None
            request.session['alt_kat'] = None
            request.session['js_ariza_adi'] = None
            request.session['js_servis'] = None
            request.session['js_yp1'] = None
            request.session['js_yp2'] = None
            request.session['js_yp3'] = None
            request.session['js_yp4'] = None
            request.session['js_yp5'] = None
            request.session['js_ka'] = None
            request.session['js_kk'] = None
            request.session['js_tutar'] = None
            request.session['js_aciklama'] = None
            form = ArizaForm(proje_no=None, alt_kat=None)
            messages.success(request, 'Başarıyla kaydetti....')
            return redirect('ariza_yarat')
        else:
            return render(request, 'giris/ariza_yarat.html', {'form': form})


    # if a GET (or any other method) we'll create a blank form
    else:
        #proje_no = request.session['ab_proje_no']
        #alt_kat = request.session['alt_kat']
        proje_no = request.session.get('ab_proje_no')
        alt_kat = request.session.get('alt_kat')
        dem_no = request.session.get('js_demirbas')
        ar_adi = request.session.get('js_ariza_adi')
        servis = request.session.get('js_servis')
        yp1 = request.session.get('js_yp1')
        yp2 = request.session.get('js_yp2')
        yp3 = request.session.get('js_yp3')
        yp4 = request.session.get('js_yp4')
        yp5 = request.session.get('js_yp5')
        ka = request.session.get('js_ka')
        kp = request.session.get('js_kk')
        tut = request.session.get('js_tutar')
        acik = request.session.get('js_aciklama')
        #print("bu da doğru değilse kafayı mı yiyeyim...:", request.session['ab_proje_no'])
        print("get işlemi form yaratırken arıza yarat...proje_no", proje_no)
        print("get işlemi form yaratırken arıza yarat...alt_kat", alt_kat)
        form = ArizaForm(proje_no=proje_no, alt_kat=alt_kat)
        form.fields["proje"].initial = proje_no
        form.fields["demirbas"].initial = dem_no
        form.fields["ariza_adi"].initial = ar_adi
        form.fields["servis"].initial = servis
        form.fields["yedek_parca_1"].initial = yp1
        form.fields["yedek_parca_2"].initial = yp2
        form.fields["yedek_parca_3"].initial = yp3
        form.fields["yedek_parca_4"].initial = yp4
        form.fields["yedek_parca_5"].initial = yp5
        form.fields["kayit_acilis"].initial = ka
        form.fields["kayit_kapanis"].initial = kp
        form.fields["tutar"].initial = tut
        form.fields["aciklama"].initial = acik

        return render(request, 'giris/ariza_yarat.html', {'form': form})


        #selected_alt = request.session.get('selected_alt')


@login_required
def ariza_guncelle(request, pk=None):
    obje = get_object_or_404(ariza, pk=pk)
    print("ariza guncelle", pk)
    print(obje)
    print(obje.ariza_adi)
    print(obje.demirbas)
    print("...........")
    print(request.user)
    print(request.user.id)

    if request.method == 'POST':
        print("post  .....", pk)
        proje_no = request.session['ab_proje_no']
        alt_kat = request.session['alt_kat']
        form = ArizaForm(request.POST or None, request.FILES or None, proje_no=proje_no, alt_kat=alt_kat)
        #dd_garanti_bitis = None
        if form.is_valid():
            dd_ariza_adi = request.POST.get('ariza_adi', "")
            dd_proje = request.POST.get('proje',"")
            dd_demirbas = request.POST.get('demirbas', "")
            dd_servis = request.POST.get('servis', "")
            dd_yp1 = request.POST.get('yedek_parca_1', "")
            dd_yp2 = request.POST.get('yedek_parca_2', "")
            dd_yp3 = request.POST.get('yedek_parca_3', "")
            dd_yp4 = request.POST.get('yedek_parca_4', "")
            dd_yp5 = request.POST.get('yedek_parca_5', "")
            dd_ac = request.POST.get('kayit_acilis', "")
            dd_kapa = request.POST.get('kayit_kapanis', "")
            dd_tutar = request.POST.get('tutar', "")
            dd_tutar_int = request.POST.get('tutar_int', "")
            dd_aciklama = request.POST.get('aciklama', "")
            kullanan = request.user.id
            yaratildi = datetime.now()
            print ("arıza adı", dd_ariza_adi)
            print ("proje", dd_proje)
            print ("demirbas", dd_demirbas)
            print ("servis", dd_servis)
            print ("yp1", dd_yp1)
            print ("yp2", dd_yp2)
            print ("yp3", dd_yp3)
            print ("yp4", dd_yp4)
            print ("yp5", dd_yp5)
            print ("kayıt açılış", dd_ac)
            print ("kayıt kapanış", dd_kapa)
            print ("tutar", dd_tutar)
            print ("tutar_int", dd_tutar_int)
            print ("aciklama", dd_aciklama)
            print ("kullanan", kullanan)
            print ("yaratildi", yaratildi)
            #import pdb; pdb.set_trace()
            kaydetme_obj = ariza(id=pk,
                                ariza_adi = dd_ariza_adi,
                                proje_id = dd_proje,
                                demirbas_id = dd_demirbas,
                                servis_id = dd_servis,
                                yedek_parca_1_id = dd_yp1,
                                yedek_parca_2_id = dd_yp2,
                                yedek_parca_3_id = dd_yp3,
                                yedek_parca_4_id = dd_yp4,
                                yedek_parca_5_id = dd_yp5,
                                kayit_acilis = dd_ac,
                                kayit_kapanis = dd_kapa,
                                tutar = dd_tutar_int,
                                aciklama = dd_aciklama,
                                kullanan_id = kullanan,
                                yaratildi = yaratildi)
            kaydetme_obj.save()
            messages.success(request, 'Başarıyla güncelledi....')
            return redirect('ariza')
        else:

            return render(request, 'giris/ariza_guncelle.html', {'form': form})


    else:
        print("get .....", pk)
        print("obje.id...:", obje.id)
        proje_no = request.session['ab_proje_no']
        alt_kat = request.session['alt_kat']
        form = ArizaForm(proje_no=proje_no, alt_kat=alt_kat)

        form.fields["pk_no"].initial = obje.id
        form.fields["proje"].initial = obje.proje
        form.fields["ariza_adi"].initial = obje.ariza_adi
        form.fields["demirbas"].initial = obje.demirbas
        form.fields["servis"].initial = obje.servis
        form.fields["yedek_parca_1"].initial = obje.yedek_parca_1
        form.fields["yedek_parca_2"].initial = obje.yedek_parca_2
        form.fields["yedek_parca_3"].initial = obje.yedek_parca_3
        form.fields["yedek_parca_4"].initial = obje.yedek_parca_4
        form.fields["yedek_parca_5"].initial = obje.yedek_parca_5
        form.fields["kayit_acilis"].initial = obje.kayit_acilis
        form.fields["kayit_kapanis"].initial = obje.kayit_kapanis
        form.fields["tutar"].initial = obje.tutar
        form.fields["tutar_int"].initial = obje.tutar
        form.fields["aciklama"].initial = obje.aciklama

        args = {'form': form}
        return render(request, 'giris/ariza_guncelle.html', {'form': form})



@login_required
def ariza_sil(request, pk=None):
    sil_ariza = ariza.objects.get(id=pk)
    sil_id = sil_ariza.id
    args = {'sil_id': sil_id, 'sil_ariza': sil_ariza, 'pk': pk,}
    return render(request, 'giris/ariza_sil_soru.html', args)


@login_required
def ariza_sil_kesin(request, pk=None):
    object = get_object_or_404(ariza, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        return JsonResponse(error_message)
    messages.success(request, 'Başarıyla silindi....')
    return redirect('ariza')


@login_required
def ariza_ara(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Ariza_Ara_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            arama = request.POST.get('alan', "")
            print (arama)
            ariza_arama_filtresi = ariza.objects.annotate(search=SearchVector('ariza_adi'),).filter(search=arama)
            return render(request, 'giris/ariza_arm_list.html', {'ariza_arama_filtresi': ariza_arama_filtresi},)

        else:
            return render(request, 'giris/ariza_arm_list.html', {'form': form})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = Ariza_Ara_Form()
        return render(request, 'giris/ariza_ara.html', {'form': form})


# arıza formunda seçilen projede uygun demirbaşların listelenmesi için
# çalıştırılan js entegre kod....

def demirbas_ariza_listesi(request):
    print("selam buraya geldik.... demirbas arıza listesi")
    print("User.id.....:", request.user.id)
    response_data ={}
    if request.method == 'GET':
        selected = request.GET.get('selected', None)
        js_demirbas = request.GET.get('js_demirbas', None)
        js_ariza_adi = request.GET.get('js_ariza_adi', None)
        js_servis = request.GET.get('js_servis', None)
        js_yp1 = request.GET.get('js_yp1', None)
        js_yp2 = request.GET.get('js_yp2', None)
        js_yp3 = request.GET.get('js_yp3', None)
        js_yp4 = request.GET.get('js_yp4', None)
        js_yp5 = request.GET.get('js_yp5', None)
        js_ka = request.GET.get('js_ka', None)
        js_kk = request.GET.get('js_kk', None)
        js_tutar = request.GET.get('js_tutar', None)
        js_aciklama = request.GET.get('js_aciklama', None)
        print("selected...:", selected, js_demirbas, js_ariza_adi, js_servis, js_yp1, js_yp2,)
        if selected != None:
            request.session['ab_proje_no'] = selected
            request.session['alt_kat'] = None
            request.session['js_demirbas'] = js_demirbas
            request.session['js_ariza_adi'] = js_ariza_adi
            request.session['js_servis'] = js_servis
            request.session['js_yp1'] = js_yp1
            request.session['js_yp2'] = js_yp2
            request.session['js_yp3'] = js_yp3
            request.session['js_yp4'] = js_yp4
            request.session['js_yp5'] = js_yp5
            request.session['js_ka'] = js_ka
            request.session['js_kk'] = js_kk
            request.session['js_tutar'] = js_tutar
            request.session['js_aciklama'] = js_aciklama
            request.session.modified = True
            print("yetti artık....neden doğru yazmıyor...:", request.session['ab_proje_no'])

    print ("son nokta demirbas arıza listesi....", response_data)
    return HttpResponse(response_data, content_type='application/json')












def demirbas_ariza_listesi_g(request, pk=None):
    print("selam buraya geldik...ggggggggggggggggg. demirbas arıza listesi")
    print("User.id.....:", request.user.id)
    response_data ={}
    if request.method == 'GET':
        selected = request.GET.get('selected', None)
        js_demirbas = request.GET.get('js_demirbas', None)
        js_ariza_adi = request.GET.get('js_ariza_adi', None)
        js_servis = request.GET.get('js_servis', None)
        js_yp1 = request.GET.get('js_yp1', None)
        js_yp2 = request.GET.get('js_yp2', None)
        js_yp3 = request.GET.get('js_yp3', None)
        js_yp4 = request.GET.get('js_yp4', None)
        js_yp5 = request.GET.get('js_yp5', None)
        js_ka = request.GET.get('js_ka', None)
        js_kk = request.GET.get('js_kk', None)
        js_tutar = request.GET.get('js_tutar', None)
        js_aciklama = request.GET.get('js_aciklama', None)
        print("selected...:", selected, js_demirbas, js_ariza_adi, js_servis, js_yp1, js_yp2,)
        if selected != None:
            request.session['ab_proje_no'] = selected
            request.session['alt_kat'] = None
            request.session['js_demirbas'] = js_demirbas
            request.session['js_ariza_adi'] = js_ariza_adi
            request.session['js_servis'] = js_servis
            request.session['js_yp1'] = js_yp1
            request.session['js_yp2'] = js_yp2
            request.session['js_yp3'] = js_yp3
            request.session['js_yp4'] = js_yp4
            request.session['js_yp5'] = js_yp5
            request.session['js_ka'] = js_ka
            request.session['js_kk'] = js_kk
            request.session['js_tutar'] = js_tutar
            request.session['js_aciklama'] = js_aciklama
            request.session.modified = True
            print("yetti artık....neden doğru yazmıyor...:", request.session['ab_proje_no'])
            form = ArizaForm(proje_no=selected, alt_kat=None)
    print ("son nokta demirbas arıza listesi..ggggggg..", response_data)
    return HttpResponse(response_data, content_type='application/json')


# arıza formunda seçili demirbaşın ilgili yedek parçalarına ulaşmak için
# alt kategori üzerinden çalışan js ile entegre kod....



def yedekparca_ariza_listesi(request):
    print("selam buraya geldik.... yedekparca_ariza_listesi")
    response_data = {}
    if request.method == 'GET':
        selected = request.GET.get('selected', None)
        js_ariza_adi = request.GET.get('js_ariza_adi', None)
        js_servis = request.GET.get('js_servis', None)
        js_yp1 = request.GET.get('js_yp1', None)
        js_yp2 = request.GET.get('js_yp2', None)
        js_yp3 = request.GET.get('js_yp3', None)
        js_yp4 = request.GET.get('js_yp4', None)
        js_yp5 = request.GET.get('js_yp5', None)
        js_ka = request.GET.get('js_ka', None)
        js_kk = request.GET.get('js_kk', None)
        js_tutar = request.GET.get('js_tutar', None)
        js_aciklama = request.GET.get('js_aciklama', None)
        print("selected...:", selected)
        if selected != None:
            obj = demirbas.objects.get(id=selected)
            obj_2 = obj.alt_kategori
            selected_altkat = obj_2.id
            print("selected_altkat", selected_altkat)
            proje_no = request.session['ab_proje_no']
            request.session['js_demirbas'] = selected
            request.session['alt_kat'] = selected_altkat
            request.session['js_ariza_adi'] = js_ariza_adi
            request.session['js_servis'] = js_servis
            request.session['js_yp1'] = js_yp1
            request.session['js_yp2'] = js_yp2
            request.session['js_yp3'] = js_yp3
            request.session['js_yp4'] = js_yp4
            request.session['js_yp5'] = js_yp5
            request.session['js_ka'] = js_ka
            request.session['js_kk'] = js_kk
            request.session['js_tutar'] = js_tutar
            request.session['js_aciklama'] = js_aciklama
            request.session.modified = True
            form = ArizaForm(proje_no=proje_no, alt_kat=selected_altkat)
            print("sonca...demce....yedek parça listesi  sonu :",  )
            #args = {'form': form,}
    print ("son nokta  yedek parça arıza listesi ....",)
    return HttpResponse(response_data, content_type='application/json')




def yedekparca_ariza_listesi_g(request, pk=None):
    print("selam buraya geldik...gggggggggggggg. yedekparca_ariza_listesi")
    response_data = {}
    if request.method == 'GET':
        selected = request.GET.get('selected', None)
        js_ariza_adi = request.GET.get('js_ariza_adi', None)
        js_servis = request.GET.get('js_servis', None)
        js_yp1 = request.GET.get('js_yp1', None)
        js_yp2 = request.GET.get('js_yp2', None)
        js_yp3 = request.GET.get('js_yp3', None)
        js_yp4 = request.GET.get('js_yp4', None)
        js_yp5 = request.GET.get('js_yp5', None)
        js_ka = request.GET.get('js_ka', None)
        js_kk = request.GET.get('js_kk', None)
        js_tutar = request.GET.get('js_tutar', None)
        js_aciklama = request.GET.get('js_aciklama', None)
        print("selected...:", selected)
        if selected != None:
            obj = demirbas.objects.get(id=selected)
            obj_2 = obj.alt_kategori
            selected_altkat = obj_2.id
            print("selected_altkat", selected_altkat)
            proje_no = request.session['ab_proje_no']
            request.session['js_demirbas'] = selected
            request.session['alt_kat'] = selected_altkat
            request.session['js_ariza_adi'] = js_ariza_adi
            request.session['js_servis'] = js_servis
            request.session['js_yp1'] = js_yp1
            request.session['js_yp2'] = js_yp2
            request.session['js_yp3'] = js_yp3
            request.session['js_yp4'] = js_yp4
            request.session['js_yp5'] = js_yp5
            request.session['js_ka'] = js_ka
            request.session['js_kk'] = js_kk
            request.session['js_tutar'] = js_tutar
            request.session['js_aciklama'] = js_aciklama
            request.session.modified = True
            form = ArizaForm(proje_no=proje_no, alt_kat=selected_altkat)
            print("sonca...demce....yedek parça listesi  sonu :",  )
            #args = {'form': form,}
    print ("son nokta  yedek parça arıza listesi .ggggggggggg...",)
    return HttpResponse(response_data, content_type='application/json')



# silme işlemleri için bölüm.......

@login_required
def proje_sil(request, pk=None):
    print("proje sildeki pk:", pk)
    object = get_object_or_404(proje, pk=pk)
    sil_proje = object.proje_adi
    sil_id = object.id
    print("sil_proje", sil_proje)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_proje': sil_proje, 'pk': pk,}
    return render(request, 'giris/proje_sil_soru.html', args)


@login_required
def proje_sil_kesin(request, pk=None):
    print("proje sil kesindeki pk:", pk)
    object = get_object_or_404(proje, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('proje')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('proje')




@login_required
def marka_sil(request, pk=None):
    print("marka sildeki pk:", pk)
    object = get_object_or_404(marka, pk=pk)
    sil_marka = object.marka_adi
    sil_id = object.id
    print("sil_marka", sil_marka)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_marka': sil_marka, 'pk': pk,}
    return render(request, 'giris/marka_sil_soru.html', args)


@login_required
def marka_sil_kesin(request, pk=None):
    print("marka sil kesindeki pk:", pk)
    object = get_object_or_404(marka, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('marka')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('marka')



@login_required
def kategori_sil(request, pk=None):
    print("kategori sildeki pk:", pk)
    object = get_object_or_404(kategori, pk=pk)
    sil_kategori = object.kategori_adi
    sil_id = object.id
    print("sil_kategori", sil_kategori)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_kategori': sil_kategori, 'pk': pk,}
    return render(request, 'giris/kategori_sil_soru.html', args)


@login_required
def kategori_sil_kesin(request, pk=None):
    print("kategori sil kesindeki pk:", pk)
    object = get_object_or_404(kategori, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('kategori')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('kategori')





@login_required
def alt_kategori_sil(request, pk=None):
    print("alt kategori sildeki pk:", pk)
    object = get_object_or_404(alt_kategori, pk=pk)
    sil_alt_kategori = object.alt_kategori_adi
    sil_id = object.id
    print("sil_alt_kategori", sil_alt_kategori)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_alt_kategori': sil_alt_kategori, 'pk': pk,}
    return render(request, 'giris/alt_kategori_sil_soru.html', args)


@login_required
def alt_kategori_sil_kesin(request, pk=None):
    print("alt kategori sil kesindeki pk:", pk)
    object = get_object_or_404(alt_kategori, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('alt_kategori')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('alt_kategori')




@login_required
def ekipman_turu_sil(request, pk=None):
    print("alt kategori sildeki pk:", pk)
    object = get_object_or_404(ekipman_turu, pk=pk)
    sil_ekipman_turu = object.ekipman_turu
    sil_id = object.id
    print("sil_ekipman_turu", sil_ekipman_turu)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_ekipman_turu': sil_ekipman_turu, 'pk': pk,}
    return render(request, 'giris/ekipman_turu_sil_soru.html', args)


@login_required
def ekipman_turu_sil_kesin(request, pk=None):
    print("ekipman türü sil kesindeki pk:", pk)
    object = get_object_or_404(ekipman_turu, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('ekipman_turu')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('ekipman_turu')



@login_required
def yedek_parca_sil(request, pk=None):
    print("yedek parça sildeki pk:", pk)
    object = get_object_or_404(yedek_parca, pk=pk)
    sil_yedek_parca = object.yparca_adi
    sil_id = object.id
    print("sil_yedek_parca", sil_yedek_parca)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_yedek_parca': sil_yedek_parca, 'pk': pk,}
    return render(request, 'giris/yedek_parca_sil_soru.html', args)


@login_required
def yedek_parca_sil_kesin(request, pk=None):
    print("yedek parça sil kesindeki pk:", pk)
    object = get_object_or_404(yedek_parca, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('yedek_parca')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('yedek_parca')



@login_required
def sirket_sil(request, pk=None):
    print("şirket sildeki pk:", pk)
    object = get_object_or_404(sirket, pk=pk)
    sil_sirket = object.sirket_adi
    sil_id = object.id
    print("sil_sirket", sil_marka)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_sirket': sil_sirket, 'pk': pk,}
    return render(request, 'giris/sirket_sil_soru.html', args)


@login_required
def sirket_sil_kesin(request, pk=None):
    print("sirket sil kesindeki pk:", pk)
    object = get_object_or_404(sirket, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('sirket')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('sirket')



@login_required
def musteri_sil(request, pk=None):
    print("müşteri sildeki pk:", pk)
    object = get_object_or_404(musteri, pk=pk)
    sil_musteri = object.musteri_adi
    sil_id = object.id
    print("sil_musteri", sil_musteri)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_musteri': sil_musteri, 'pk': pk,}
    return render(request, 'giris/musteri_sil_soru.html', args)


@login_required
def musteri_sil_kesin(request, pk=None):
    print("müşteri sil kesindeki pk:", pk)
    object = get_object_or_404(musteri, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('musteri')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('musteri')



@login_required
def grup_sil(request, pk=None):
    print("grup sildeki pk:", pk)
    object = get_object_or_404(grup, pk=pk)
    sil_musteri = object.grup_adi
    sil_id = object.id
    print("sil_grup", sil_grup)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_grup': sil_grup, 'pk': pk,}
    return render(request, 'giris/grup_sil_soru.html', args)


@login_required
def grup_sil_kesin(request, pk=None):
    print("grup sil kesindeki pk:", pk)
    object = get_object_or_404(grup, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('grup')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('grup')




@login_required
def servis_sil(request, pk=None):
    print("servis sildeki pk:", pk)
    object = get_object_or_404(servis, pk=pk)
    sil_servis = object.servis_adi
    sil_id = object.id
    print("sil_servis", sil_servis)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_servis': sil_servis, 'pk': pk,}
    return render(request, 'giris/servis_sil_soru.html', args)


@login_required
def servis_sil_kesin(request, pk=None):
    print("servis sil kesindeki pk:", pk)
    object = get_object_or_404(servis, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('servis')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('servis')




@login_required
def dem_perteayir(request, pk=None):
    print("perteayırdaki pk:", pk)
    object = get_object_or_404(demirbas, pk=pk)
    pert = object.demirbasadi
    pert_id = object.id
    print("pert ", pert)
    print("pert_id", pert_id)
    args = {'pert_id': pert_id, 'pert': pert, 'pk': pk,}
    return render(request, 'giris/pert_soru.html', args)


@login_required
def dem_perteayir_kesin(request, pk=None):
    print("pert kesindeki pk:", pk)
    object = get_object_or_404(demirbas, pk=pk)
    try:
        object.kullanim_durumu = "P"
        #object.proje = None
        object.save()
    except ProtectedError:
        error_message = "bağlantılı veri var, protected error...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var, protected error .......')
        return redirect('proje_sor')
    messages.success(request, 'Demirbaş başarıyla pert edildi....')
    return redirect('proje_sor')



@login_required
def dem_devret(request, pk=None):
    print("devretteki pk:", pk)
    object = get_object_or_404(demirbas, pk=pk)
    devret = object.demirbasadi
    devret_id = object.id
    print("devret ", devret)
    print("devret_id", devret_id)
    args = {'devret_id': devret_id, 'devret': devret, 'pk': pk,}
    return render(request, 'giris/devret_soru.html', args)


@login_required
def dem_devret_kesin(request, pk=None):
    print("devret kesindeki pk:", pk)
    object = get_object_or_404(demirbas, pk=pk)
    try:
        object.kullanim_durumu = "V"
        #object.proje = None
        object.save()

    except ProtectedError:
        error_message = "bağlantılı veri var, protected error...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var, protected error .......')
        return redirect('proje_sor')
    messages.success(request, 'Demirbaş başarıyla devir edildi....')
    return redirect('proje_sor')


@login_required
def dem_depoya(request, pk=None):
    print("depodaki pk:", pk)
    object = get_object_or_404(demirbas, pk=pk)
    depoya = object.demirbasadi
    depoya_id = object.id
    print("depoya ", depoya)
    print("depoya_id", depoya_id)
    args = {'depoya_id': depoya_id, 'depoya': depoya, 'pk': pk,}
    return render(request, 'giris/depoya_soru.html', args)


@login_required
def dem_depoya_kesin(request, pk=None):
    print("depoya kesindeki pk:", pk)
    object = get_object_or_404(demirbas, pk=pk)
    try:
        object.kullanim_durumu = "D"
        #object.proje = None
        object.save()

    except ProtectedError:
        error_message = "bağlantılı veri var, protected error...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var, protected error .......')
        return redirect('proje_sor')
    messages.success(request, 'Demirbaş başarıyla depoya aktarıldı....')
    return redirect('proje_sor')











# proje yaratma, güncelleme, silme...

class ProjeCreate(LoginRequiredMixin,CreateView):
    model = proje
    fields = '__all__'
    success_url = "/giris/proje/create/"

class ProjeUpdate(LoginRequiredMixin,UpdateView):
    model = proje
    fields = '__all__'
    success_url = "/giris/proje/"

class ProjeDelete(LoginRequiredMixin,DeleteView):
    model = proje
    success_url = reverse_lazy('proje')


# marka yaratma, güncelleme silme...

class MarkaCreate(LoginRequiredMixin,CreateView):
    model = marka
    fields = '__all__'
    success_url = "/giris/marka/create/"

class MarkaUpdate(LoginRequiredMixin,UpdateView):
    model = marka
    fields = '__all__'
    success_url = "/giris/marka/"

class MarkaDelete(LoginRequiredMixin,DeleteView):
    model = marka
    success_url = reverse_lazy('marka')


# kategori yaratma, güncelleme, silme...

class KategoriCreate(LoginRequiredMixin,CreateView):
    model = kategori
    fields = '__all__'
    success_url = "/giris/kategori/create/"

class KategoriUpdate(LoginRequiredMixin,UpdateView):
    model = kategori
    fields = '__all__'
    success_url = "/giris/kategori/"

class KategoriDelete(LoginRequiredMixin,DeleteView):
    model = kategori
    success_url = reverse_lazy('kategori')

# müşteri yaratma, güncelleme, silme ...

class MusteriCreate(LoginRequiredMixin,CreateView):
    model = musteri
    fields = '__all__'
    success_url = "/giris/musteri/create/"

class MusteriUpdate(LoginRequiredMixin,UpdateView):
    model = musteri
    fields = '__all__'
    success_url = "/giris/musteri/"

class MusteriDelete(LoginRequiredMixin,DeleteView):
    model = musteri
    success_url = reverse_lazy('musteri')


# grup yaratma, güncelleme, silme ...

class GrupCreate(LoginRequiredMixin,CreateView):
    model = grup
    fields = '__all__'
    success_url = "/giris/grup/create/"

class GrupUpdate(LoginRequiredMixin,UpdateView):
    model = grup
    fields = '__all__'
    success_url = "/giris/grup/"

class GrupDelete(LoginRequiredMixin,DeleteView):
    model = grup
    success_url = reverse_lazy('grup')



# şirket yaratma, güncelleme, silme...

class SirketCreate(LoginRequiredMixin,CreateView):
    model = sirket
    fields = '__all__'
    success_url = "/giris/sirket/create/"

class SirketUpdate(LoginRequiredMixin,UpdateView):
    model = sirket
    fields = '__all__'
    success_url = "/giris/sirket/"

class SirketDelete(LoginRequiredMixin,DeleteView):
    model = sirket
    success_url = reverse_lazy('sirket')


# ekipman türü  yaratma, güncelleme silme...

class Ekipman_turuCreate(LoginRequiredMixin,CreateView):
    model = ekipman_turu
    fields = '__all__'
    success_url = "/giris/ekipman_turu/create/"

class Ekipman_turuUpdate(LoginRequiredMixin,UpdateView):
    model = ekipman_turu
    fields = '__all__'
    success_url = "/giris/ekipman_turu/"

class Ekipman_turuDelete(LoginRequiredMixin,DeleteView):
    model = ekipman_turu
    success_url = reverse_lazy('ekipman_turu')


# servis yaratma, güncelleme, silme...

class ServisCreate(LoginRequiredMixin,CreateView):
    model = servis
    fields = '__all__'
    success_url = "/giris/servis/create/"

class ServisUpdate(LoginRequiredMixin,UpdateView):
    model = servis
    fields = '__all__'
    success_url = "/giris/servis/"

class ServisDelete(LoginRequiredMixin,DeleteView):
    model = servis
    success_url = reverse_lazy('servis')


# alt kategori yaratma, güncelleme, silme ...

class Alt_kategoriCreate(LoginRequiredMixin,CreateView):
    model = alt_kategori
    fields = '__all__'
    success_url = "/giris/alt_kategori/create/"

class Alt_kategoriUpdate(LoginRequiredMixin,UpdateView):
    model = alt_kategori
    fields = '__all__'
    success_url = "/giris/alt_kategori/"

class Alt_kategoriDelete(LoginRequiredMixin,DeleteView):
    model = alt_kategori
    success_url = reverse_lazy('alt_kategori')


# yedek parça  yaratma, güncelleme, silme ...

class Yedek_parcaCreate(LoginRequiredMixin,CreateView):
    model = yedek_parca
    fields = '__all__'
    success_url = "/giris/yedek_parca/create/"

class Yedek_parcaUpdate(LoginRequiredMixin,UpdateView):
    model = yedek_parca
    fields = '__all__'
    success_url = "/giris/yedek_parca/"

class Yedek_parcaDelete(LoginRequiredMixin,DeleteView):
    model = yedek_parca
    success_url = reverse_lazy('yedek_parca')













# tüm list-view ve detail-view'lar......

class DemirbasListView(LoginRequiredMixin,generic.ListView):
    model = demirbas
    #paginate_by = 20
    def get_queryset(self):
        return demirbas.objects.filter(kullanim_durumu="K")

class DemirbasDetailView(LoginRequiredMixin,generic.DetailView):
    model = demirbas

class ProjeListView(LoginRequiredMixin,generic.ListView):
    model = proje
    #paginate_by = 20

class ProjeDetailView(LoginRequiredMixin,generic.DetailView):
    model = proje

class MarkaListView(LoginRequiredMixin,generic.ListView):
    model = marka
    paginate_by = 5

class MarkaDetailView(LoginRequiredMixin,generic.DetailView):
    model = marka

class KategoriListView(LoginRequiredMixin,generic.ListView):
    model = kategori
    #paginate_by = 20

class KategoriDetailView(LoginRequiredMixin,generic.DetailView):
    model = kategori

class MusteriListView(LoginRequiredMixin,generic.ListView):
    model = musteri
    #paginate_by = 20

class MusteriDetailView(LoginRequiredMixin,generic.DetailView):
    model = musteri


#------------------------------------

class GrupListView(LoginRequiredMixin,generic.ListView):
    model = grup
    #paginate_by = 20

class GrupDetailView(LoginRequiredMixin,generic.DetailView):
    model = grup

class SirketListView(LoginRequiredMixin,generic.ListView):
    model = sirket
    #paginate_by = 20

class SirketDetailView(LoginRequiredMixin,generic.DetailView):
    model = sirket

class Ekipman_turuListView(LoginRequiredMixin,generic.ListView):
    model = ekipman_turu
    #paginate_by = 5

class Ekipman_turuDetailView(LoginRequiredMixin,generic.DetailView):
    model = ekipman_turu

class ServisListView(LoginRequiredMixin,generic.ListView):
    model = servis
    #paginate_by = 20

class ServisDetailView(LoginRequiredMixin,generic.DetailView):
    model = servis

class Alt_kategoriListView(LoginRequiredMixin,generic.ListView):
    model = alt_kategori
    #paginate_by = 20

class Alt_kategoriDetailView(LoginRequiredMixin,generic.DetailView):
    model = alt_kategori

#-------------------------

class Yedek_parcaListView(LoginRequiredMixin,generic.ListView):
    model = yedek_parca
    #paginate_by = 20

class Yedek_parcaDetailView(LoginRequiredMixin,generic.DetailView):
    model = yedek_parca

class HareketListView(LoginRequiredMixin,generic.ListView):
    model = hareket
    paginate_by = 20

class HareketDetailView(LoginRequiredMixin,generic.DetailView):
    model = hareket

class ArizaListView(LoginRequiredMixin,generic.ListView):
    model = ariza
    #paginate_by = 20

class ArizaDetailView(LoginRequiredMixin,generic.DetailView):
    model = ariza
