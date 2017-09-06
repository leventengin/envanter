# Create your models here.


from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.db import models


class marka(models.Model):
    marka_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.marka_adi)

class kategori(models.Model):
    kategori_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.kategori_adi)

class musteri(models.Model):
    musteri_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.muster_adi)


class proje(models.Model):
    FATURA_TURU = (
    ('S', 'SabitÜcret'),
    ('P', 'ProjeSaati'),
    ('G', 'GörevSaati'),
    )
    FATURA_DURUMU = (
    ('B', 'Başlamadı'),
    ('D', 'DevamEdiyor'),
    ('X', 'Beklemede'),
    ('I', 'İptal'),
    ('T', 'Tamamlandı'),
    )
    proje_adi = models.TextField(max_length=200)
    musteri = models.ForeignKey(musteri)
    fat_turu = models.CharField(max_length=1, choices=FATURA_TURU)
    fat_durumu = models.CharField(max_length=1, choices=FATURA_DURUMU)
    toplam_ucret = models.IntegerField()
    aciklama = models.TextField()
    yaratildi = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return(self.proje_adi)



class demirbas(models.Model):
    DURUM = (
    ('A', 'Aktif'),
    ('P', 'Pasif'),
    )
    demirbasadi = models.CharField(max_length=200)
    proje = models.ForeignKey(proje)
    bolum = models.CharField(max_length=200)
    marka = models.ForeignKey(marka)
    kategori = models.ForeignKey(kategori)
    modeli = models.TextField()
    durum = models.CharField(max_length=1, choices=DURUM)
    garanti_bitis = models.DateField()
    amts_kalanyil = models.PositiveIntegerField()
    env_bedeli = models.IntegerField()
    aciklama = models.TextField()
    yetkinlik_skalasi = models.CharField(max_length=1)
    yaratildi = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return(self.demirbasadi)
