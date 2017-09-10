from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from giris.models import marka, demirbas, kategori, proje, musteri
from giris.forms import MarkaGirisForm
from django.core import serializers
from django.utils.translation import gettext as _



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


def home(request):
    return render(request, 'ilk.html')


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


class DemirbasCreate(LoginRequiredMixin,CreateView):
    model = demirbas
    fields = '__all__'
    success_url = "/giris/demirbas/create/"

class DemirbasUpdate(LoginRequiredMixin,UpdateView):
    model = demirbas
    fields = '__all__'
    success_url = "/giris/demirbas/"

class DemirbasDelete(LoginRequiredMixin,DeleteView):
    model = demirbas
    success_url = reverse_lazy('demirbas')


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



def markayenikaydet(request):
    if request.method == 'POST':
        form = MarkaGirisForm(request.POST)
        if  form.is_valid():
            marka_ad_gecici = request.POST.get('marka_adi')
            marka_obj = marka(marka_adi = marka_ad_gecici)
            marka.save()
    else:
        form = MarkaGirisForm()
    return render(request, '/giris/addbook.html', {'form': form})


@login_required
def markaduzeltsil(request):
    return render(request, 'giris/marka_duzeltsil.html')

@login_required
def markaekle(request):
    return render(request, 'giris/marka_giris.html')
#    return render(request, 'giris/deneme.html')
