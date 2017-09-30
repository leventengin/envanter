

from django.views.generic import RedirectView
from django.conf.urls import include, url
from . import views
from django.utils.translation import gettext as _


urlpatterns = [
    url(r'^$', views.index, name='index'),
    # demirbaş urlleri aşağıda....
    url(r'^demirbas/$', views.DemirbasListView.as_view(), name='demirbas'),
    url(r'^demirbas/(?P<pk>\d+)$', views.DemirbasDetailView.as_view(), name='demirbas-detail'),
    url(r'^demirbas/create/$', views.DemirbasCreate.as_view(), name='demirbas_create'),
    url(r'^demirbas/yarat/$', views.demirbas_yarat, name='demirbas_yarat'),
    url(r'^demirbas/(?P<pk>\d+)/update/$', views.DemirbasUpdate.as_view(), name='demirbas_update'),
    url(r'^demirbas/(?P<pk>\d+)/guncelle/$', views.demirbas_guncelle, name='demirbas_guncelle'),
    url(r'^demirbas/(?P<pk>\d+)/delete/$', views.DemirbasDelete.as_view(), name='demirbas_delete'),
    url(r'^demirbas/(?P<pk>\d+)/sil/$', views.demirbas_sil, name='demirbas_sil'),
    #url(r'^demirbas/aktar$', views.DenemeView.as_view(), name='denemeview'),
    #url(r'^demirbas/aktar$', views.deneme_picker, name='deneme_picker'),
    url(r'^demirbas/aktar$', views.get_name, name='get_name'),
    url(r'^demirbas_popup/$', views.demirbas_popup, name='demirbas_popup'),

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
    #url(r'^markayenikaydet/$', views.markayenikaydet, name='markayenikaydet'),


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

    ]
