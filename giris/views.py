from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from giris.models import marka, demirbas, kategori, proje, musteri, deneme_giris
from giris.models import grup, sirket, ekipman_turu, servis, alt_kategori, yedek_parca, hareket, ariza
from giris.forms import MarkaForm, DemirbasForm, KategoriForm, MusteriForm, ProjeForm, Demirbas_Ara_Form
from giris.forms import GrupForm, SirketForm, Ekipman_turuForm, ServisForm, Alt_kategoriForm, Yedek_parcaForm
from giris.forms import HareketForm, ArizaForm, Hareket_Ara_Form, Ariza_Ara_Form

from django.core import serializers
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.search import SearchVector
from django.views.generic import FormView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NameForm
import datetime
from datetime import date
from django.template.loader import render_to_string






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
        #global deneme_giris_nesne
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
    num_musteri=musteri.objects.count()
    return render(request, 'ana_menu.html',
        context={'num_demirbas':num_demirbas,'num_proje':num_proje,'num_marka':num_marka,'num_kategori':num_kategori, 'num_musteri':num_musteri},
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
            yaratildi = date.today()
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
            #text = form.cleaned_data["demirbasadi"]
            form = DemirbasForm()
            #args = {'form': form, 'text': text}
            #return render(request, 'name.html', args)
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
    obj = get_object_or_404(demirbas, pk=pk)
    form = DemirbasForm(request.POST or None,
                        request.FILES or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
           form.save()
           messages.success(request, 'Başarıyla güncelledi....')
           return redirect('demirbas')
    return render(request, '/giris/demirbas_list.html', {'form': form})


@login_required
def demirbas_sil(request, object_id):
    return render(request, 'demirbas_sil_soru.html')

@login_required
def demirbas_sil_kesin(request, object_id):
    object = get_object_or_404(Model, pk=object_id)
    object.delete()
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






#hareket  yaratma işlemi .......

@login_required
def hareket_yarat(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HareketForm(request.POST)
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
            yaratildi = date.today()
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
            #text = form.cleaned_data["demirbasadi"]
            form = HareketForm()
            #args = {'form': form, 'text': text}
            #return render(request, 'name.html', args)
            messages.success(request, 'Başarıyla kaydetti....')
            return redirect('hareket_yarat')
        else:
            return render(request, 'giris/hareket_yarat.html', {'form': form})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = HareketForm()
        #deneme_giris_QS = deneme_giris.objects.all().order_by('-tarih')
        #args = {'form': form, 'deneme_giris_QS': deneme_giris_QS}
        #return render(request, '/giris/demirbas_yarat.html', args)
        return render(request, 'giris/hareket_yarat.html', {'form': form})



@login_required
def hareket_guncelle(request, pk=None):
    obj = get_object_or_404(hareket, pk=pk)
    form = HareketForm(request.POST or None,
                        request.FILES or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
           form.save()
           messages.success(request, 'Başarıyla güncelledi....')
           return redirect('hareket')
    return render(request, '/giris/hareket_list.html', {'form': form})



@login_required
def hareket_sil(request, object_id):
    return render(request, 'hareket_sil_soru.html')


@login_required
def hareket_sil_kesin(request, object_id):
    object = get_object_or_404(Model, pk=object_id)
    object.delete()
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








#ariza yaratma işlemi .......

@login_required
def ariza_yarat(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ArizaForm(request.POST)
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
            yaratildi = date.today()
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
                        request.FILES or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
           form.save()
           messages.success(request, 'Başarıyla güncelledi....')
           return redirect('ariza')
    return render(request, '/giris/ariza_list.html', {'form': form})


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
    model = demirbas
    #paginate_by = 20

class GrupDetailView(LoginRequiredMixin,generic.DetailView):
    model = demirbas

class SirketListView(LoginRequiredMixin,generic.ListView):
    model = proje
    #paginate_by = 20

class SirketDetailView(LoginRequiredMixin,generic.DetailView):
    model = proje

class Ekipman_turuListView(LoginRequiredMixin,generic.ListView):
    model = marka
    paginate_by = 5

class Ekipman_turuDetailView(LoginRequiredMixin,generic.DetailView):
    model = marka

class ServisListView(LoginRequiredMixin,generic.ListView):
    model = kategori
    #paginate_by = 20

class ServisDetailView(LoginRequiredMixin,generic.DetailView):
    model = kategori

class Alt_kategoriListView(LoginRequiredMixin,generic.ListView):
    model = musteri
    #paginate_by = 20

class Alt_kategoriDetailView(LoginRequiredMixin,generic.DetailView):
    model = musteri

#-------------------------

class Yedek_parcaListView(LoginRequiredMixin,generic.ListView):
    model = kategori
    #paginate_by = 20

class Yedek_parcaDetailView(LoginRequiredMixin,generic.DetailView):
    model = kategori

class HareketListView(LoginRequiredMixin,generic.ListView):
    model = musteri
    #paginate_by = 20

class HareketDetailView(LoginRequiredMixin,generic.DetailView):
    model = musteri

class ArizaListView(LoginRequiredMixin,generic.ListView):
    model = musteri
    #paginate_by = 20

class ArizaDetailView(LoginRequiredMixin,generic.DetailView):
    model = musteri
