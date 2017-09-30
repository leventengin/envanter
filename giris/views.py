from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from giris.models import marka, demirbas, kategori, proje, musteri, deneme_giris
from giris.forms import MarkaGirisForm, DemirbasGirisForm, KategoriGirisForm, MusteriGirisForm, ProjeGirisForm
from django.core import serializers
from django.utils.translation import ugettext_lazy as _

from django.views.generic import FormView
from giris.forms import DenemeForm

class DenemeView(FormView):
    template_name = "deneme.html"
    form_class = DenemeForm

from django.shortcuts import render, redirect, get_object_or_404

from .forms import NameForm, DemirbasForm



def deneme_picker(request):
    return render(request, 'deneme_picker.html')


def home(request):
    return render(request, 'ilk.html')


def demirbas_popup(request):
    return render(request, 'demirbas_popup.html')


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
            form = DemirbasForm()
            #args = {'form': form, 'text': text}
            #return render(request, 'name.html', args)
            messages.success(request, 'Başarıyla kaydetti....')
            return redirect('demirbas_yarat')
        else:
            return render(request, '/giris/demirbas_yarat.html', {'form': form})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = DemirbasForm()
        deneme_giris_QS = deneme_giris.objects.all().order_by('-tarih')
        args = {'form': form, 'deneme_giris_QS': deneme_giris_QS}
        return render(request, '/giris/demirbas_yarat.html', args)



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




def demirbas_sil(request, object_id):
    object = get_object_or_404(Model, pk=object_id)
    object.delete()
    messages.success(request, 'Başarıyla silindi....')
    return redirect('demirbas')




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




# demirbaş  yaratma, güncelleme, silme....

class DemirbasCreate(LoginRequiredMixin,CreateView):
    model = demirbas
    fields = '__all__'
    #messages.success(request, 'Başarıyla kaydedildi...')
    #success_url = "/giris/demirbas_popup/"
    success_url = "/giris/demirbas/create/"


class DemirbasUpdate(LoginRequiredMixin,UpdateView):
    model = demirbas
    fields = '__all__'
    success_url = "/giris/demirbas/"

class DemirbasDelete(LoginRequiredMixin,DeleteView):
    model = demirbas
    success_url = reverse_lazy('demirbas')



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


# burası denemeler için......................

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import MarkaGirisForm
from django.utils.translation import gettext as _



def DemirbasAktar(request):
    if request.method == 'POST':
        form = DemirbasAktar(request.POST)
        if  form.is_valid():
            proje_ad_gecici = request.POST.get('proje_adi')
            proje_adi = proje(proje_adi = proje_ad_gecici)
            proje.update()
    else:
        form = DemirbasAktar()
    #return render(request, '/giris/addbook.html', {'form': form})


@login_required
def markaduzeltsil(request):
    return render(request, 'giris/marka_duzeltsil.html')

@login_required
def markaekle(request):
    return render(request, 'giris/marka_giris.html')
#    return render(request, 'giris/deneme.html')
