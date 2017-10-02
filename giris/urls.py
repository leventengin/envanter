

from django.views.generic import RedirectView
from django.conf.urls import include, url
from . import views
from django.utils.translation import gettext as _


urlpatterns = [
    url(r'^$', views.index, name='index'),

    # demirbaş urlleri aşağıda....
    url(r'^demirbas/$', views.DemirbasListView.as_view(), name='demirbas'),
    url(r'^demirbas/(?P<pk>\d+)$', views.DemirbasDetailView.as_view(), name='demirbas-detail'),
    url(r'^demirbas/yarat/$', views.demirbas_yarat, name='demirbas_yarat'),
    url(r'^demirbas/(?P<pk>\d+)/guncelle/$', views.demirbas_guncelle, name='demirbas_guncelle'),
    url(r'^demirbas/(?P<pk>\d+)/sil/$', views.demirbas_sil, name='demirbas_sil'),
    url(r'^demirbas/aktar$', views.get_name, name='get_name'),
    url(r'^demirbas_ara$', views.demirbas_ara, name='demirbas_ara'),


    # proje urlleri aşağıda....
    url(r'^proje/$', views.ProjeListView.as_view(), name='proje'),
    url(r'^proje/(?P<pk>\d+)$', views.ProjeDetailView.as_view(), name='proje-detail'),
    url(r'^proje/create/$', views.ProjeCreate.as_view(), name='proje_create'),
    url(r'^proje/(?P<pk>\d+)/update/$', views.ProjeUpdate.as_view(), name='proje_update'),
    url(r'^proje/(?P<pk>\d+)/delete/$', views.ProjeDelete.as_view(), name='proje_delete'),


    # marka urlleri aşağıda....
    url(r'^marka/$', views.MarkaListView.as_view(), name='marka'),
    url(r'^marka/(?P<pk>\d+)$', views.MarkaDetailView.as_view(), name='marka-detail'),
    url(r'^marka/create/$', views.MarkaCreate.as_view(), name='marka_create'),
    url(r'^marka/(?P<pk>\d+)/update/$', views.MarkaUpdate.as_view(), name='marka_update'),
    url(r'^marka/(?P<pk>\d+)/delete/$', views.MarkaDelete.as_view(), name='marka_delete'),



    # kategori urlleri aşağıda....
    url(r'^kategori/$', views.KategoriListView.as_view(), name='kategori'),
    url(r'^kategori/(?P<pk>\d+)$', views.KategoriDetailView.as_view(), name='kategori-detail'),
    url(r'^kategori/create/$', views.KategoriCreate.as_view(), name='kategori_create'),
    url(r'^kategori/(?P<pk>\d+)/update/$', views.KategoriUpdate.as_view(), name='kategori_update'),
    url(r'^kategori/(?P<pk>\d+)/delete/$', views.KategoriDelete.as_view(), name='kategori_delete'),


    # müşteri urlleri aşağıda....
    url(r'^musteri/$', views.MusteriListView.as_view(), name='musteri'),
    url(r'^musteri/(?P<pk>\d+)$', views.MusteriDetailView.as_view(), name='musteri-detail'),
    url(r'^musteri/create/$', views.MusteriCreate.as_view(), name='musteri_create'),
    url(r'^musteri/(?P<pk>\d+)/update/$', views.MusteriUpdate.as_view(), name='musteri_update'),
    url(r'^musteri/(?P<pk>\d+)/delete/$', views.MusteriDelete.as_view(), name='musteri_delete'),


    # grup urlleri aşağıda....
    url(r'^grup/$', views.GrupListView.as_view(), name='grup'),
    url(r'^grup/(?P<pk>\d+)$', views.GrupDetailView.as_view(), name='grup-detail'),
    url(r'^grup/create/$', views.GrupCreate.as_view(), name='grup_create'),
    url(r'^grup/(?P<pk>\d+)/update/$', views.GrupUpdate.as_view(), name='grup_update'),
    url(r'^grup/(?P<pk>\d+)/delete/$', views.GrupDelete.as_view(), name='grup_delete'),

    # şirket urlleri aşağıda....
    url(r'^sirket/$', views.SirketListView.as_view(), name='sirket'),
    url(r'^sirket/(?P<pk>\d+)$', views.SirketDetailView.as_view(), name='sirket-detail'),
    url(r'^sirket/create/$', views.SirketCreate.as_view(), name='sirket_create'),
    url(r'^sirket/(?P<pk>\d+)/update/$', views.SirketUpdate.as_view(), name='sirket_update'),
    url(r'^sirket/(?P<pk>\d+)/delete/$', views.SirketDelete.as_view(), name='sirket_delete'),

    # ekipman_turu urlleri aşağıda....
    url(r'^ekipman_turu/$', views.Ekipman_turuListView.as_view(), name='ekipman_turu'),
    url(r'^ekipman_turu/(?P<pk>\d+)$', views.Ekipman_turuDetailView.as_view(), name='ekipman_turu-detail'),
    url(r'^ekipman_turu/create/$', views.Ekipman_turuCreate.as_view(), name='ekipman_turu_create'),
    url(r'^ekipman_turu/(?P<pk>\d+)/update/$', views.Ekipman_turuUpdate.as_view(), name='ekipman_turu_update'),
    url(r'^ekipman_turu/(?P<pk>\d+)/delete/$', views.Ekipman_turuDelete.as_view(), name='ekipman_turu_delete'),


    # servis urlleri aşağıda....
    url(r'^servis/$', views.ServisListView.as_view(), name='servis'),
    url(r'^servis/(?P<pk>\d+)$', views.ServisDetailView.as_view(), name='servis-detail'),
    url(r'^servis/create/$', views.ServisCreate.as_view(), name='servis_create'),
    url(r'^servis/(?P<pk>\d+)/update/$', views.ServisUpdate.as_view(), name='servis_update'),
    url(r'^servis/(?P<pk>\d+)/delete/$', views.ServisDelete.as_view(), name='servis_delete'),


    # alt_kategori urlleri aşağıda....
    url(r'^alt_kategori/$', views.Alt_kategoriListView.as_view(), name='alt_kategori'),
    url(r'^alt_kategori/(?P<pk>\d+)$', views.Alt_kategoriDetailView.as_view(), name='alt_kategori-detail'),
    url(r'^alt_kategori/create/$', views.Alt_kategoriCreate.as_view(), name='alt_kategori_create'),
    url(r'^alt_kategori/(?P<pk>\d+)/update/$', views.Alt_kategoriUpdate.as_view(), name='alt_kategori_update'),
    url(r'^alt_kategori/(?P<pk>\d+)/delete/$', views.Alt_kategoriDelete.as_view(), name='alt_kategori_delete'),


    # yedek_parça urlleri aşağıda....
    url(r'^yedek_parca/$', views.Yedek_parcaListView.as_view(), name='yedek_parca'),
    url(r'^yedek_parca/(?P<pk>\d+)$', views.Yedek_parcaDetailView.as_view(), name='yedek_parca-detail'),
    url(r'^yedek_parca/create/$', views.Yedek_parcaCreate.as_view(), name='yedek_parca_create'),
    url(r'^yedek_parca/(?P<pk>\d+)/update/$', views.Yedek_parcaUpdate.as_view(), name='yedek_parca_update'),
    url(r'^yedek_parca/(?P<pk>\d+)/delete/$', views.Yedek_parcaDelete.as_view(), name='yedek_parca_delete'),


    # hareket urlleri aşağıda....
    url(r'^hareket/$', views.HareketListView.as_view(), name='hareket'),
    url(r'^hareket/(?P<pk>\d+)$', views.HareketDetailView.as_view(), name='hareket-detail'),
    url(r'^hareket/yarat/$', views.hareket_yarat, name='hareket_yarat'),
    url(r'^hareket/(?P<pk>\d+)/guncelle/$', views.hareket_guncelle, name='hareket_guncelle'),
    url(r'^hareket/(?P<pk>\d+)/sil/$', views.hareket_sil, name='hareket_sil'),
    url(r'^hareket_ara$', views.hareket_ara, name='hareket_ara'),



    # arıza urlleri aşağıda....
    url(r'^ariza/$', views.ArizaListView.as_view(), name='ariza'),
    url(r'^ariza/(?P<pk>\d+)$', views.ArizaDetailView.as_view(), name='ariza-detail'),
    url(r'^ariza/yarat/$', views.ariza_yarat, name='ariza_yarat'),
    url(r'^ariza/(?P<pk>\d+)/guncelle/$', views.ariza_guncelle, name='ariza_guncelle'),
    url(r'^ariza/(?P<pk>\d+)/sil/$', views.ariza_sil, name='ariza_sil'),
    url(r'^ariza_ara$', views.ariza_ara, name='ariza_ara'),




    ]
