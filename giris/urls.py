

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^demirbas/$', views.DemirbasListView.as_view(), name='demirbas'),
    url(r'^demirbas/(?P<pk>\d+)$', views.DemirbasDetailView.as_view(), name='demirbas-detail'),
    url(r'^proje/$', views.ProjeListView.as_view(), name='proje'),
    url(r'^proje/(?P<pk>\d+)$', views.ProjeDetailView.as_view(), name='proje-detail'),
    url(r'^marka/$', views.MarkaListView.as_view(), name='marka'),
    url(r'^marka/(?P<pk>\d+)$', views.MarkaDetailView.as_view(), name='marka-detail'),
    url(r'^kategori/$', views.KategoriListView.as_view(), name='kategori'),
    url(r'^kategori/(?P<pk>\d+)$', views.KategoriDetailView.as_view(), name='kategori-detail'),
    url(r'^musteri/$', views.MusteriListView.as_view(), name='musteri'),
    url(r'^musteri/(?P<pk>\d+)$', views.MusteriDetailView.as_view(), name='musteri-detail'),
    ]
