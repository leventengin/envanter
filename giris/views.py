from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import demirbas, proje, marka, kategori, musteri

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

class DemirbasListView(generic.ListView):
    model = demirbas
    #paginate_by = 20

class DemirbasDetailView(generic.DetailView):
    model = demirbas

class ProjeListView(generic.ListView):
    model = proje
    #paginate_by = 20

class ProjeDetailView(generic.DetailView):
    model = proje

class MarkaListView(generic.ListView):
    model = marka
    paginate_by = 5

class MarkaDetailView(generic.DetailView):
    model = marka

class KategoriListView(generic.ListView):
    model = kategori
    #paginate_by = 20

class KategoriDetailView(generic.DetailView):
    model = kategori

class MusteriListView(generic.ListView):
    model = musteri
    #paginate_by = 20

class MusteriDetailView(generic.DetailView):
    model = musteri

def cikis(request):
    return render(request, 'registration/logged_out.html',
    )
