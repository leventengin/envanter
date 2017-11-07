

from django.views.generic import RedirectView
from django.conf.urls import include, url
from . import views
from django.utils.translation import gettext as _
from rest_framework import routers, serializers, viewsets



urlpatterns = [
    url(r'^$', views.index, name='index'),

    # demirbaş urlleri aşağıda....
    url(r'^demirbas/$', views.DemirbasListView.as_view(), name='demirbas'),
    url(r'^demirbas/(?P<pk>\d+)$', views.DemirbasDetailView.as_view(), name='demirbas-detail'),
    url(r'^demirbas_depo/(?P<pk>\d+)$', views.demirbas_depo_detail, name='demirbas_depo_detail'),
    url(r'^demirbas/yarat/$', views.demirbas_yarat, name='demirbas_yarat'),
    url(r'^demirbas/(?P<pk>\d+)/guncelle/$', views.demirbas_guncelle, name='demirbas_guncelle'),
    url(r'^demirbas/(?P<pk>\d+)/sil/kesin/$', views.demirbas_sil_kesin, name='demirbas_sil_kesin'),
    url(r'^demirbas/(?P<pk>\d+)/sil/$', views.demirbas_sil, name='demirbas_sil'),
    url(r'^demirbas/aktar$', views.get_name, name='get_name'),
    url(r'^demirbas_ara$', views.demirbas_ara, name='demirbas_ara'),
    url(r'^demirbas/yarat/demirbas_garanti/$', views.demirbas_garanti, name='demirbas_garanti'),
    url(r'^demirbas/proje/$', views.proje_sor, name='proje_sor'),
    url(r'^demirbas/proje/(?P<pk>\d+)$', views.secili_proje, name='secili_proje'),

    # proje urlleri aşağıda....
    url(r'^proje/$', views.ProjeListView.as_view(), name='proje'),
    url(r'^proje/(?P<pk>\d+)$', views.ProjeDetailView.as_view(), name='proje-detail'),
    url(r'^proje/create/$', views.ProjeCreate.as_view(), name='proje_create'),
    url(r'^proje/(?P<pk>\d+)/update/$', views.ProjeUpdate.as_view(), name='proje_update'),
    url(r'^proje/(?P<pk>\d+)/delete/$', views.proje_sil, name='proje_sil'),
    url(r'^proje/(?P<pk>\d+)/delete/kesin/$', views.proje_sil_kesin, name='proje_sil_kesin'),



    # marka urlleri aşağıda....
    url(r'^marka/$', views.MarkaListView.as_view(), name='marka'),
    url(r'^marka/(?P<pk>\d+)$', views.MarkaDetailView.as_view(), name='marka-detail'),
    url(r'^marka/create/$', views.MarkaCreate.as_view(), name='marka_create'),
    url(r'^marka/(?P<pk>\d+)/update/$', views.MarkaUpdate.as_view(), name='marka_update'),
    url(r'^marka/(?P<pk>\d+)/delete/$', views.marka_sil, name='marka_sil'),
    url(r'^marka/(?P<pk>\d+)/delete/kesin/$', views.demirbas_sil_kesin, name='demirbas_sil_kesin'),



    # kategori urlleri aşağıda....
    url(r'^kategori/$', views.KategoriListView.as_view(), name='kategori'),
    url(r'^kategori/(?P<pk>\d+)$', views.KategoriDetailView.as_view(), name='kategori-detail'),
    url(r'^kategori/create/$', views.KategoriCreate.as_view(), name='kategori_create'),
    url(r'^kategori/(?P<pk>\d+)/update/$', views.KategoriUpdate.as_view(), name='kategori_update'),
    url(r'^kategori/(?P<pk>\d+)/delete/$', views.kategori_sil, name='kategori_sil'),
    url(r'^kategori/(?P<pk>\d+)/delete/kesin/$', views.kategori_sil_kesin, name='kategori_sil_kesin'),


    # müşteri urlleri aşağıda....
    url(r'^musteri/$', views.MusteriListView.as_view(), name='musteri'),
    url(r'^musteri/(?P<pk>\d+)$', views.MusteriDetailView.as_view(), name='musteri-detail'),
    url(r'^musteri/create/$', views.MusteriCreate.as_view(), name='musteri_create'),
    url(r'^musteri/(?P<pk>\d+)/update/$', views.MusteriUpdate.as_view(), name='musteri_update'),
    url(r'^musteri/(?P<pk>\d+)/delete/$', views.musteri_sil, name='musteri_sil'),
    url(r'^musteri/(?P<pk>\d+)/delete/kesin/$', views.musteri_sil_kesin, name='musteri_sil_kesin'),


    # grup urlleri aşağıda....
    url(r'^grup/$', views.GrupListView.as_view(), name='grup'),
    url(r'^grup/(?P<pk>\d+)$', views.GrupDetailView.as_view(), name='grup-detail'),
    url(r'^grup/create/$', views.GrupCreate.as_view(), name='grup_create'),
    url(r'^grup/(?P<pk>\d+)/update/$', views.GrupUpdate.as_view(), name='grup_update'),
    url(r'^grup/(?P<pk>\d+)/delete/$', views.grup_sil, name='grup_sil'),
    url(r'^grup/(?P<pk>\d+)/delete/kesin/$', views.grup_sil_kesin, name='grup_sil_kesin'),



    # şirket urlleri aşağıda....
    url(r'^sirket/$', views.SirketListView.as_view(), name='sirket'),
    url(r'^sirket/(?P<pk>\d+)$', views.SirketDetailView.as_view(), name='sirket-detail'),
    url(r'^sirket/create/$', views.SirketCreate.as_view(), name='sirket_create'),
    url(r'^sirket/(?P<pk>\d+)/update/$', views.SirketUpdate.as_view(), name='sirket_update'),
    url(r'^sirket/(?P<pk>\d+)/delete/$', views.sirket_sil, name='sirket_sil'),
    url(r'^sirket/(?P<pk>\d+)/delete/kesin/$', views.sirket_sil_kesin, name='sirket_sil_kesin'),




    # ekipman_turu urlleri aşağıda....
    url(r'^ekipman_turu/$', views.Ekipman_turuListView.as_view(), name='ekipman_turu'),
    url(r'^ekipman_turu/(?P<pk>\d+)$', views.Ekipman_turuDetailView.as_view(), name='ekipman_turu-detail'),
    url(r'^ekipman_turu/create/$', views.Ekipman_turuCreate.as_view(), name='ekipman_turu_create'),
    url(r'^ekipman_turu/(?P<pk>\d+)/update/$', views.Ekipman_turuUpdate.as_view(), name='ekipman_turu_update'),
    url(r'^ekipman_turu/(?P<pk>\d+)/delete/$', views.ekipman_turu_sil, name='ekipman_turu_sil'),
    url(r'^ekipman_turu/(?P<pk>\d+)/delete/kesin/$', views.ekipman_turu_sil_kesin, name='ekipman_turu_sil_kesin'),




    # servis urlleri aşağıda....
    url(r'^servis/$', views.ServisListView.as_view(), name='servis'),
    url(r'^servis/(?P<pk>\d+)$', views.ServisDetailView.as_view(), name='servis-detail'),
    url(r'^servis/create/$', views.ServisCreate.as_view(), name='servis_create'),
    url(r'^servis/(?P<pk>\d+)/update/$', views.ServisUpdate.as_view(), name='servis_update'),
    url(r'^servis/(?P<pk>\d+)/delete/$', views.servis_sil, name='servis_sil'),
    url(r'^servis/(?P<pk>\d+)/delete/kesin/$', views.servis_sil_kesin, name='servis_sil_kesin'),




    # alt_kategori urlleri aşağıda....
    url(r'^alt_kategori/$', views.Alt_kategoriListView.as_view(), name='alt_kategori'),
    url(r'^alt_kategori/(?P<pk>\d+)$', views.Alt_kategoriDetailView.as_view(), name='alt_kategori-detail'),
    url(r'^alt_kategori/create/$', views.Alt_kategoriCreate.as_view(), name='alt_kategori_create'),
    url(r'^alt_kategori/(?P<pk>\d+)/update/$', views.Alt_kategoriUpdate.as_view(), name='alt_kategori_update'),
    url(r'^alt_kategori/(?P<pk>\d+)/delete/$', views.alt_kategori_sil, name='alt_kategori_sil'),
    url(r'^alt_kategori/(?P<pk>\d+)/delete/kesin/$', views.alt_kategori_sil_kesin, name='alt_kategori_sil_kesin'),



    # yedek_parça urlleri aşağıda....
    url(r'^yedek_parca/$', views.Yedek_parcaListView.as_view(), name='yedek_parca'),
    url(r'^demirbas/yedek_parca_listesi/$', views.yparca_sec, name='yparca_sec'),
    url(r'^yedek_parca/(?P<pk>\d+)$', views.Yedek_parcaDetailView.as_view(), name='yedek_parca-detail'),
    url(r'^yedek_parca/create/$', views.Yedek_parcaCreate.as_view(), name='yedek_parca_create'),
    url(r'^yedek_parca/(?P<pk>\d+)/update/$', views.Yedek_parcaUpdate.as_view(), name='yedek_parca_update'),
    url(r'^yedek_parca/(?P<pk>\d+)/delete/$', views.yedek_parca_sil, name='yedek_parca_sil'),
    url(r'^yedek_parca/(?P<pk>\d+)/delete/kesin/$', views.yedek_parca_sil_kesin, name='yedek_parca_sil_kesin'),




    # hareket urlleri aşağıda....
    url(r'^hareket/$', views.HareketListView.as_view(), name='hareket'),
    url(r'^hareket/(?P<pk>\d+)$', views.HareketDetailView.as_view(), name='hareket-detail'),
    url(r'^hareket/yarat/(?P<pk>\d+)$', views.hareket_yarat, name='hareket_yarat'),
    url(r'^hareket/depodan_geri/(?P<pk>\d+)$', views.depodan_geri, name='depodan_geri'),
    url(r'^hareket/perteayir/(?P<pk>\d+)$', views.dem_perteayir, name='dem_perteayir'),
    url(r'^hareket/perteayir/(?P<pk>\d+)/kesin/$', views.dem_perteayir_kesin, name='dem_perteayir_kesin'),
    url(r'^hareket/devret/(?P<pk>\d+)$', views.dem_devret, name='dem_devret'),
    url(r'^hareket/devret/(?P<pk>\d+)/kesin/$', views.dem_devret_kesin, name='dem_devret_kesin'),
    url(r'^hareket/depoya/(?P<pk>\d+)$', views.dem_depoya, name='dem_depoya'),
    url(r'^hareket/depoya/(?P<pk>\d+)/kesin/$', views.dem_depoya_kesin, name='dem_depoya_kesin'),
    url(r'^hareket/(?P<pk>\d+)/guncelle/$', views.hareket_guncelle, name='hareket_guncelle'),
    url(r'^hareket/(?P<pk>\d+)/sil/$', views.hareket_sil, name='hareket_sil'),
    url(r'^hareket_ara$', views.hareket_ara, name='hareket_ara'),
    url(r'^hareket/proje_dem/$', views.proje_dem_sor, name='proje_dem_sor'),
    url(r'^hareket/p_d_js/$', views.deneme, name='deneme'),
    url(r'^depo/$', views.depo_listesi, name='depo_listesi'),



    # arıza urlleri aşağıda....
    url(r'^ariza/$', views.ArizaListView.as_view(), name='ariza'),
    url(r'^ariza/(?P<pk>\d+)$', views.ArizaDetailView.as_view(), name='ariza-detail'),
    url(r'^ariza/yarat/$', views.ariza_yarat, name='ariza_yarat'),
    url(r'^ariza/yarat/demirbas_ariza_listesi/$', views.demirbas_ariza_listesi, name='demirbas_ariza_listesi'),
    url(r'^ariza/yarat/yedekparca_ariza_listesi/$', views.yedekparca_ariza_listesi, name='yedekparca_ariza_listesi'),
    url(r'^ariza/(?P<pk>\d+)/guncelle/$', views.ariza_guncelle, name='ariza_guncelle'),
    url(r'^ariza/(?P<pk>\d+)/sil/$', views.ariza_sil, name='ariza_sil'),
    url(r'^ariza_ara$', views.ariza_ara, name='ariza_ara'),
    url(r'^ariza/(?P<pk>\d+)/guncelle/demirbas_ariza_listesi_g/$', views.demirbas_ariza_listesi_g, name='demirbas_ariza_listesi_g'),
    url(r'^ariza/(?P<pk>\d+)/guncelle/yedekparca_ariza_listesi_g/$', views.yedekparca_ariza_listesi_g, name='yedekparca_ariza_listesi_g'),
    url(r'^ariza/(?P<pk>\d+)/sil/kesin/$', views.ariza_sil_kesin, name='ariza_sil_kesin'),


    ]
