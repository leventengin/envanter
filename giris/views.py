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
from giris.forms import HareketForm, ArizaForm, Hareket_Ara_Form, Ariza_Ara_Form, Proje_SorForm

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








def deneme_picker(request):
    return render(request, 'deneme_picker.html')


def home(request):
    return render(request, 'ilk.html')



def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')
            #return HttpResponse('..........................')
            #return HttpResponse("<p>....... unutma</p>")

            #data = {'name': 'Vitor', 'location': 'Finland', 'is_active': True, 'count': 28
            #}
            #return JsonResponse(data)
            isim = request.POST.get('your_name', "")
            tarih = request.POST.get('tarih', "")
            kullanici = request.user
            print (isim, kullanici, tarih)
            #import pdb; pdb.set_trace()
            kaydetme_obj = deneme_giris(yazi = isim, user = kullanici, tarih = tarih)
            kaydetme_obj.save()

            text = form.cleaned_data["your_name"]
            form = NameForm()
            #args = {'form': form, 'text': text}
            #return render(request, 'name.html', args)
            messages.success(request, 'Başarıyla kaydetti....')
            return redirect('get_name')
        else:
            return render(request, 'name.html', {'form': form})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
        #request.session['bir_sefer'] = 0
        deneme_giris_QS = deneme_giris.objects.all().order_by('-tarih')
        args = {'form': form, 'deneme_giris_QS': deneme_giris_QS}
        #import pdb; pdb.set_trace()
        return render(request, 'name.html', args)




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
            dd_garanti_varmi = request.POST.get('garanti_varmi', "")
            dd_garanti_bitis = request.POST.get('garanti_bitis', "")
            dd_amts_kalanyil = request.POST.get('amts_kalanyil', "")
            dd_bedeli = request.POST.get('bedeli', "")
            dd_aciklama = request.POST.get('aciklama', "")
            kullanici = request.user
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
            print ("garanti_varmi", dd_garanti_varmi)
            print ("garanti_bitis", dd_garanti_bitis)
            print ("amts_kalanyil", dd_amts_kalanyil)
            print ("bedeli", dd_bedeli)
            print ("aciklama", dd_aciklama)
            print ("kullanici", kullanici)
            print ("yaratildi", yaratildi)
            #import pdb; pdb.set_trace()
            kaydetme_obj = demirbas(demirbasadi = dd_demirbasadi, proje_id = dd_proje,  bolum = dd_bolum,
                marka_id = dd_marka, ekipman_turu_id = dd_ekipman_turu, alt_kategori_id = dd_alt_kategori,
                modeli = dd_modeli, durum = dd_durumu, gar_varmi = dd_garanti_varmi,
                garanti_bitis = dd_garanti_bitis, amts_kalanyil = dd_amts_kalanyil, env_bedeli = dd_bedeli,
                aciklama = dd_aciklama, kullanici = kullanici, yaratildi = yaratildi)
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
        #dd_garanti_bitis = None
        if form.is_valid():
            dd_demirbasadi = request.POST.get('adi', "")
            dd_proje = request.POST.get('proje', "")
            dd_bolum = request.POST.get('bolum', "")
            dd_marka = request.POST.get('marka', "")
            dd_ekipman_turu = request.POST.get('ekipman_turu', "")
            dd_alt_kategori = request.POST.get('alt_kategori', "")
            dd_modeli = request.POST.get('modeli', "")
            dd_durumu = request.POST.get('durumu', "")
            dd_garanti_varmi = request.POST.get('garanti_varmi', "")
            dd_garanti_bitis = request.POST.get('garanti_bitis', "")
            dd_amts_kalanyil = request.POST.get('amts_kalanyil', "")
            dd_bedeli = request.POST.get('bedeli', "")
            dd_aciklama = request.POST.get('aciklama', "")
            kullanici = request.user.id
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
            print ("garanti_varmi", dd_garanti_varmi)
            print ("garanti_bitis", dd_garanti_bitis)
            print ("amts_kalanyil", dd_amts_kalanyil)
            print ("bedeli", dd_bedeli)
            print ("aciklama", dd_aciklama)
            print ("kullanici", kullanici)
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
                                    gar_varmi = dd_garanti_varmi,
                                    garanti_bitis = dd_garanti_bitis,
                                    amts_kalanyil = dd_amts_kalanyil,
                                    env_bedeli = dd_bedeli,
                                    aciklama = dd_aciklama,
                                    kullanici = kullanici,
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
def demirbas_ara(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Demirbas_Ara_Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            arama = request.POST.get('alan', "")
            print (arama)
            #import pdb; pdb.set_trace()
            #kaydetme_obj = deneme_giris(yazi = isim, user = kullanici, tarih = tarih)
            #kaydetme_obj.save()
            demirbas_arama_filtresi = demirbas.objects.annotate(search=SearchVector('demirbasadi'),).filter(search=arama)
            return render(request, 'giris/demirbas_arm_list.html', {'demirbas_arama_filtresi': demirbas_arama_filtresi},)
            #text = form.cleaned_data["alan"]
            #form = Demirbas_Ara_Form()
            #args = {'form': form, 'text': text}
            #return render(request, 'name.html', args)
            #messages.success(request, 'Başarıyla kaydetti....')
            #return redirect('get_name')
        else:
            return render(request, 'giris/demirbas_arm_list.html', {'form': form})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = Demirbas_Ara_Form()
        #global deneme_giris_nesne
        #deneme_giris_QS = deneme_giris.objects.all().order_by('-tarih')
        #args = {'form': form, 'deneme_giris_QS': deneme_giris_QS}
        #import pdb; pdb.set_trace()
        return render(request, 'giris/demirbas_ara.html', {'form': form})



class demirbas_sec(forms.TextInput):
    class Media:
        print("demirbas_sec class...:")
        js = ('giris/js/dem_sec.js')


import json
from django.core import serializers


def yparca_sec(request):
    print("selam buraya geldik.... yparca_sec")
    response_data ={}
    yparca_demirbas.objects.filter(kullanici=user.id).delete()
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
            print("selected_altkat", selected_altkat)
            obj2 = yedek_parca.objects.filter(alt_kategori=selected_altkat)
            print("obj2...:", obj2)
            print(user.id)

            for yedek_parca.yparca_adi in obj2:
                print("yedek parça...:", yedek_parca.yparca_adi)
                kaydetme_obj = yparca_demirbas(yparca_demirbas = yedek_parca.yparca_adi,
                                               kullanici = user.id)
                kaydetme_obj.save()

            #choice_list = [('--------','--------'),]
            #for yedek_parca.yparca_adi in obj2:
            #    print("yedek parça.iki..:", yedek_parca.yparca_adi)
            #    choice_list.append((yedek_parca.yparca_adi, yedek_parca.yparca_adi),)
            #print("choice list..:", choice_list)



            #response_data = serializers.serialize('json', [obj2,])
            response_data = list(obj2)
            print("response data 1111...:", response_data)
            form = NameForm()
            if not (aj_gizli == "A"):
                form.fields["gizli"].initial = "A"
                print("gizlice bas onu...:", form.fields["gizli"].initial)
            form.fields["your_name"].initial = aj_adi
            form.fields["tarih"].initial = aj_tarihi
            form.fields["demirbas"].initial = selected
            form.fields["yedek_parca"].initial = None
            form.fields["yedek_parca"].queryset = yp_choice.objects.all()
            choice_list = [('aaaaaa','aaaaaa'),]
            form.fields["yparca_choice"].choices = choice_list
            #form.fields['gizli'].initial = 1
            print("sonca...demce....:", form.fields["yparca_choice"].choices )
            args = {'form': form,}
            #return render(request, '/aktar.html', args)


            #struct = json.loads(response_data)
            #response_data = json.dumps(struct[0])
            #print("response data 2222...:", response_data)
    print ("son noktaya geliyor mu acaba", response_data)
    return HttpResponse(response_data, content_type='application/json')
            #selected_yparca = obj2
            #print("selected_yparca", selected_yparca)
            #response_data['selected_yparca'] = selected_yparca
            #print("sonuna geldik...", response_data)
    #return JsonResponse(response_data)



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
    #request.session['aa_pk'] = pk
    #cc_pk = request.session['aa_pk']
    #print ("aa_pk.....:", cc_pk)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HareketForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            dd_demirbas_id = obje.id
            dd_demirbas_adi = obje.demirbasadi
            dd_har_tipi = request.POST.get('har_tipi', "")
            dd_mevcut_proj_id = obje.proje.id
            dd_mevcut_proj = obje.proje
            dd_sonraki_proj = request.POST.get('sonraki_proj', "")
            dd_aciklama = request.POST.get('aciklama', "")
            kullanici = request.user
            yaratildi = datetime.now()
            print ("demirbas_id", dd_demirbas_id)
            print ("demirbas_adi", dd_demirbas_adi)
            print ("har tipi", dd_har_tipi)
            print ("mevcut_proj_id", dd_mevcut_proj_id)
            print ("sonraki_proj", dd_sonraki_proj)
            print ("aciklama", dd_aciklama)
            print ("kullanici", kullanici)
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
                        form.fields["har_tipi"].initial = dd_har_tipi
                        form.fields["sonraki_proj"].initial = dd_sonraki_proj
                        form.fields["aciklama"].initial = dd_aciklama
                        args = {'form': form, 'deneme_1': deneme_1, 'deneme_2': deneme_2, 'deneme_3': deneme_3, 'deneme_4': deneme_4 }
                        return render(request, 'giris/hareket_yarat.html', args)


            obje_demirbas = get_object_or_404(demirbas, pk=pk)


            kaydetme_obj = hareket(demirbas_id_id = obje_demirbas.id,
                                   demirbas_adi = obje_demirbas.demirbasadi,
                                   har_tipi = dd_har_tipi,
                                   mevcut_proj_id = dd_mevcut_proj_id,
                                   sonraki_proj_id = dd_sonraki_proj,
                                   aciklama = dd_aciklama,
                                   kullanici = kullanici,
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
                                      gar_varmi = obje_demirbas.gar_varmi,
                                      garanti_bitis = obje_demirbas.garanti_bitis,
                                      amts_kalanyil = obje_demirbas.amts_kalanyil,
                                      env_bedeli = obje_demirbas.env_bedeli,
                                      aciklama = obje_demirbas.aciklama,
                                      kullanici = obje_demirbas.kullanici,
                                      yaratildi = obje_demirbas.yaratildi,)

            dem_kaydet_obj.save()
            #text = form.cleaned_data["demirbasadi"]
            form = HareketForm()
            #args = {'form': form, 'text': text}
            #return render(request, 'name.html', args)
            messages.success(request, 'Başarıyla kaydetti....')
            return redirect('demirbas')
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
            kullanici = request.user
            yaratildi = datetime.now()
            print ("demirbaş_id", demirbas_id)
            print ("demirbas_adi", dd_demirbas_adi)
            print ("har tipi", dd_har_tipi)
            print ("mevcut_proj", dd_mevcut_proj)
            print ("sonraki_proj", dd_sonraki_proj)
            print ("aciklama", dd_aciklama)
            print ("kullanici", kullanici)
            print ("yaratildi", yaratildi)
            #import pdb; pdb.set_trace()
            kaydetme_obj = hareket(id=pk,
                                   demirbas_id_id = dd_demirbas_id,
                                   demirbas_adi = dd_demirbas_adi,
                                   har_tipi = dd_har_tipi,
                                   mevcut_proj_id = dd_mevcut_proj,
                                   sonraki_proj_id = dd_sonraki_proj,
                                   aciklama = dd_aciklama,
                                   kullanici = kullanici,
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


from django.db.models import ProtectedError

@login_required
def hareket_sil_kesin(request, object_id):
    object = get_object_or_404(Model, pk=object_id)
    try:
        object.delete()
    except ProtectedError:
        error_message = "This object can't be deleted!!"
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
            #import pdb; pdb.set_trace()
            #kaydetme_obj = deneme_giris(yazi = isim, user = kullanici, tarih = tarih)
            #kaydetme_obj.save()
            hareket_arama_filtresi = hareket.objects.annotate(search=SearchVector('aciklama'),).filter(search=arama)
            return render(request, 'giris/hareket_arm_list.html', {'hareket_arama_filtresi': hareket_arama_filtresi},)
            #text = form.cleaned_data["alan"]
            #form = Demirbas_Ara_Form()
            #args = {'form': form, 'text': text}
            #return render(request, 'name.html', args)
            #messages.success(request, 'Başarıyla kaydetti....')
            #return redirect('get_name')
        else:
            return render(request, 'giris/hareket_arm_list.html', {'form': form})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = Hareket_Ara_Form()
        #global deneme_giris_nesne
        #deneme_giris_QS = deneme_giris.objects.all().order_by('-tarih')
        #args = {'form': form, 'deneme_giris_QS': deneme_giris_QS}
        #import pdb; pdb.set_trace()
        return render(request, 'giris/hareket_ara.html', {'form': form})








def proje_sor(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Proje_SorForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            proje_no = request.POST.get('hangi_proje', "")

            print ("hangi proje ...:", proje_no)


            form = ArizaForm(proje_no=proje_no)
            #dem_qs = demirbas.objects.filter(proje=proje_no)
            args = {'form': form, 'proje_no': proje_no}
            return render(request, 'giris/ariza_yarat.html', args)

            #return redirect('get_name')
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
        form = ArizaForm(request.POST)
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
            dd_aciklama = request.POST.get('aciklama', "")
            kullanici = request.user
            yaratildi = datetime.now
            print ("proje", dd_proje)
            print ("demirbaş", dd_demirbas)
            print ("ariza adı", dd_ariza_adi)
            print ("servis", dd_servis)
            print ("yedek parça 1", dd_yedek_parca_1)
            print ("yedek parça 2", dd_yedek_parca_2)
            print ("yedek parça 1", dd_yedek_parca_1)
            print ("yedek parça 2", dd_yedek_parca_2)
            print ("yedek parça 1", dd_yedek_parca_1)
            print ("tutar", dd_tutar)
            print ("aciklama", dd_aciklama)
            print ("kullanici", kullanici)
            print ("yaratildi", yaratildi)
            #import pdb; pdb.set_trace()
            kaydetme_obj = ariza(ariza_adi = dd_ariza_adi,
                                 demirbas_id = dd_demirbas,
                                 servis_id = dd_servis,
                                 yedek_parca_1_id = dd_yedek_parca_1,
                                 yedek_parca_2_id = dd_yedek_parca_2,
                                 yedek_parca_3_id = dd_yedek_parca_3,
                                 yedek_parca_4_id = dd_yedek_parca_4,
                                 yedek_parca_5_id = dd_yedek_parca_5,
                                 tutar = dd_tutar,
                                 aciklama = dd_aciklama,
                                 kullanici = kullanici,
                                 yaratildi = yaratildi)
            kaydetme_obj.save()
            #text = form.cleaned_data["demirbasadi"]
            form = ArizaForm()
            #args = {'form': form, 'text': text}
            #return render(request, 'name.html', args)
            messages.success(request, 'Başarıyla kaydetti....')
            return redirect('ariza_yarat')
        else:
            return render(request, 'giris/ariza_yarat.html', {'form': form})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = ArizaForm()
        #deneme_giris_QS = deneme_giris.objects.all().order_by('-tarih')
        #args = {'form': form, 'deneme_giris_QS': deneme_giris_QS}
        #return render(request, '/giris/demirbas_yarat.html', args)
        return render(request, 'giris/ariza_yarat.html', {'form': form})





@login_required
def ariza_guncelle(request, pk=None):
    obj = get_object_or_404(ariza, pk=pk)
    form = ArizaForm(request.POST or None,
                        request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
           form.save()
           messages.success(request, 'Başarıyla güncelledi....')
           return redirect('ariza')
    return render(request, '/giris/ariza_list.html', {'form': form})



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
        form = ArizaForm(request.POST or None, request.FILES or None)
        #dd_garanti_bitis = None
        if form.is_valid():
            dd_ariza_adi = request.POST.get('ariza_adi', "")
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
            dd_aciklama = request.POST.get('aciklama', "")
            kullanici = request.user.id
            yaratildi = datetime.now()
            print ("arıza adı", dd_ariza_adi)
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
            print ("aciklama", dd_aciklama)
            print ("kullanici", kullanici)
            print ("yaratildi", yaratildi)
            #import pdb; pdb.set_trace()
            kaydetme_obj = ariza(id=pk,
                                ariza_adi = dd_ariza_adi,
                                demirbas_id = dd_demirbas,
                                servis_id = dd_servis,
                                yedek_parca_1_id = dd_yp1,
                                yedek_parca_2_id = dd_yp2,
                                yedek_parca_3_id = dd_yp3,
                                yedek_parca_4_id = dd_yp4,
                                yedek_parca_5_id = dd_yp5,
                                kayit_acilis = dd_ac,
                                kayit_kapanis = dd_kapa,
                                tutar = dd_tutar,
                                aciklama = dd_aciklama,
                                kullanici = kullanici,
                                yaratildi = yaratildi)
            kaydetme_obj.save()
            messages.success(request, 'Başarıyla güncelledi....')
            return redirect('ariza')
        else:

            return render(request, 'giris/ariza_yarat.html', {'form': form})


    else:
        print("get .....", pk)
        print("obje.id...:", obje.id)
        form = ArizaForm(proje_sec=1)
        form.fields["pk_no"].initial = obje.id
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
        form.fields["aciklama"].initial = obje.aciklama

        args = {'form': form,}
        return render(request, 'giris/ariza_yarat.html', args)








@login_required
def ariza_sil(request, object_id):
    return render(request, 'ariza_sil_soru.html')

@login_required
def ariza_sil_kesin(request, object_id):
    object = get_object_or_404(Model, pk=object_id)
    object.delete()
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
            #import pdb; pdb.set_trace()
            #kaydetme_obj = deneme_giris(yazi = isim, user = kullanici, tarih = tarih)
            #kaydetme_obj.save()
            ariza_arama_filtresi = ariza.objects.annotate(search=SearchVector('ariza_adi'),).filter(search=arama)
            return render(request, 'giris/ariza_arm_list.html', {'ariza_arama_filtresi': ariza_arama_filtresi},)
            #text = form.cleaned_data["alan"]
            #form = Demirbas_Ara_Form()
            #args = {'form': form, 'text': text}
            #return render(request, 'name.html', args)
            #messages.success(request, 'Başarıyla kaydetti....')
            #return redirect('get_name')
        else:
            return render(request, 'giris/ariza_arm_list.html', {'form': form})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = Ariza_Ara_Form()
        #global deneme_giris_nesne
        #deneme_giris_QS = deneme_giris.objects.all().order_by('-tarih')
        #args = {'form': form, 'deneme_giris_QS': deneme_giris_QS}
        #import pdb; pdb.set_trace()
        return render(request, 'giris/ariza_ara.html', {'form': form})


def demirbas_ariza_listesi(request):
    print("selam buraya geldik.... demirbas arıza listesi")
    print("User.id.....:", request.user.id)
    response_data ={}
    dem_ariza.objects.filter(kullanici=request.user.id).delete()
    print("hepsi silindi, liste...:")
    if request.method == 'GET':
        selected = request.GET.get('selected', None)
        print("selected...:", selected)
        if selected != None:
            obj = demirbas.objects.filter(proje=selected)
            #for demirbas.demirbasadi in obj:
            #    print("aaa..:", demirbas.demirbasadi)
            #    print("bbb...:", demirbas.alt_kategori)
            print("demirbaslar...:", obj)
            print("request.user.id...:", request.user.id)
            print("User id...:", User.id)
            user = User.objects.get(id=request.user.id)
            #global alt_kategori
            for demb in obj:
                print("demirbas..adı.:", demb.demirbasadi)
                print("demirbas alt kategori", demb.alt_kategori)
                print("yeter ulan...", )
                kaydetme_obj = dem_ariza(dem_ariza = demb.demirbasadi,
                                         alt_kategori = demb.alt_kategori,
                                         kullanici = user)
                kaydetme_obj.save()
            response_data = list(obj)
            print("response data 1111...:", response_data)
            form = ArizaForm()
            form.fields["demirbas"].queryset = dem_ariza.objects.all()
            args = {'form': form,}
    print ("son noktaya geliyor mu acaba", response_data)
    return HttpResponse(response_data, content_type='application/json')



def yedekparca_ariza_listesi(request):
    print("selam buraya geldik.... yedekparca_ariza_listesi")
    response_data ={}
    yparca_ariza.objects.filter(kullanici=request.user.id).delete()
    print("hepsi silindi, liste...:")
    if request.method == 'GET':
        selected = request.GET.get('selected', None)
        print("selected...:", selected)
        if selected != None:
            obj = dem_ariza.objects.get(id=selected)
            selected_altkat = obj.alt_kategori
            print("selected_altkat", selected_altkat)
            obj2 = yedek_parca.objects.filter(alt_kategori=selected_altkat)
            print("obj2...:", obj2)
            #print(user.id)
            user = User.objects.get(id=request.user.id)
            for yedek_parca.yparca_adi in obj2:
                print("yedek parça...:", yedek_parca.yparca_adi)
                kaydetme_obj = yparca_ariza(yparca_ariza = yedek_parca.yparca_adi,
                                            kullanici = user)
                kaydetme_obj.save()

            response_data = list(obj2)
            print("response data 1111...:", response_data)
            form = ArizaForm()
            form.fields["yedek_parca_1"].queryset = yparca_ariza.objects.all()
            form.fields["yedek_parca_2"].queryset = yparca_ariza.objects.all()
            form.fields["yedek_parca_3"].queryset = yparca_ariza.objects.all()
            form.fields["yedek_parca_4"].queryset = yparca_ariza.objects.all()
            form.fields["yedek_parca_5"].queryset = yparca_ariza.objects.all()
            print("sonca...demce....:",  )
            args = {'form': form,}
    print ("son noktaya geliyor mu acaba", response_data)
    return HttpResponse(response_data, content_type='application/json')



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
    paginate_by = 5

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
