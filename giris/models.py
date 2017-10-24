# Create your models here.


from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


DURUM = (
('A', 'Aktif'),
('P', 'Pasif'),
)
VARMI = (
('E', 'Evet'),
('H', 'Hayır'),
)

TIPI = (
('T', 'Taşıma'),
('D', 'Depoya Taşı'),
('P', 'Pert'),
('G', 'Depodan Taşı'),
('X', 'Pert İptal'),
('Z', 'Proje Sonrası Verildi')
)

ILLER = (
('ANK', 'Ankara'),
('IST', 'İstanbul'),
('IZM', 'İzmir'),
('ADA', 'Adana'),
('BUR', 'Bursa'),
('KON', 'Konya'),
('KAY', 'Kayseri'),
('MER', 'Mersin'),
('ANT', 'Antalya'),
('SAM', 'Samsun'),
('TRA', 'Trabzon'),
('MAL', 'Malatya'),
)

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



class deneme_giris(models.Model):
    yazi = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    tarih = models.DateField()
    def __str__(self):
        return(self.yazi)




class grup(models.Model):
    grup_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.grup_adi)

class sirket(models.Model):
    sirket_adi = models.CharField(max_length=200)
    grubu = models.ForeignKey(grup, on_delete=models.PROTECT)
    def __str__(self):
        return(self.sirket_adi)

class ekipman_turu(models.Model):
    ekipman_turu = models.CharField(max_length=200)
    def __str__(self):
        return(self.ekipman_turu)

class servis(models.Model):
    servis_adi = models.CharField(max_length=200)
    mail_adresi = models.EmailField()
    kisi_adi = models.CharField(max_length=200)
    kisi_soyadi = models.CharField(max_length=200)
    yaratildi = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return(self.servis_adi)

class marka(models.Model):
    marka_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.marka_adi)

class kategori(models.Model):
    kategori_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.kategori_adi)

class alt_kategori(models.Model):
    alt_kategori_adi = models.CharField(max_length=200)
    kategorisi = models.ForeignKey(kategori, on_delete=models.PROTECT)
    def __str__(self):
        return(self.alt_kategori_adi)

class yedek_parca(models.Model):
    yparca_adi = models.CharField(max_length=200)
    alt_kategori = models.ForeignKey(alt_kategori, on_delete=models.PROTECT)
    def __str__(self):
        return(self.yparca_adi)

class musteri(models.Model):
    musteri_adi = models.CharField(max_length=200)
    def __str__(self):
        return(self.musteri_adi)

class yp_choice(models.Model):
    yp_choice = models.CharField(max_length=200)
    def __str__(self):
        return(self.yp_choice)

class proje(models.Model):
    proje_adi = models.TextField(max_length=200)
    ili = models.CharField(max_length=3, choices=ILLER, default='ANK')
    musteri = models.ForeignKey(musteri, on_delete=models.PROTECT)
    sirket = models.ForeignKey(sirket, on_delete=models.PROTECT)
    fat_turu = models.CharField(max_length=1, choices=FATURA_TURU)
    fat_durumu = models.CharField(max_length=1, choices=FATURA_DURUMU)
    toplam_ucret = models.PositiveIntegerField()
    aciklama = models.TextField()
    yaratildi = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return(self.proje_adi)




class demirbas(models.Model):
    demirbasadi = models.CharField(max_length=200)
    proje = models.ForeignKey(proje, on_delete=models.PROTECT)
    bolum = models.CharField(max_length=200)
    marka = models.ForeignKey(marka, on_delete=models.PROTECT)
    ekipman_turu = models.ForeignKey(ekipman_turu, on_delete=models.PROTECT)
    alt_kategori = models.ForeignKey(alt_kategori, on_delete=models.PROTECT)
    modeli = models.CharField(max_length=200)
    durum = models.CharField(max_length=1, choices=DURUM)
    gar_varmi = models.CharField(max_length=1, choices=VARMI, default='E')
    garanti_bitis = models.DateField(default="2000-01-01", blank=True)
    amts_kalanyil = models.PositiveIntegerField()
    env_bedeli = models.PositiveIntegerField()
    aciklama = models.TextField()
    kullanici = models.CharField(max_length=100, default='admin')
    yaratildi = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return(self.demirbasadi)



class hareket(models.Model):
    demirbas_id = models.ForeignKey(demirbas, on_delete=models.PROTECT)
    demirbas_adi = models.CharField(max_length=100, default="demirbas")
    har_tipi = models.CharField(max_length=1, choices=TIPI)
    mevcut_proj = models.ForeignKey(proje, related_name='current_project', on_delete=models.PROTECT)
    sonraki_proj = models.ForeignKey(proje, related_name='next_project', on_delete=models.PROTECT)
    aciklama = models.TextField()
    kullanici = models.CharField(max_length=100, default='admin')
    yaratildi = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return(self.demirbas_adi)



class ariza(models.Model):
    ariza_adi = models.CharField(max_length=200)
    demirbas = models.ForeignKey(demirbas, on_delete=models.PROTECT)
    servis = models.ForeignKey(servis, on_delete=models.PROTECT)
    yedek_parca_1 = models.ForeignKey(yedek_parca, related_name='ilk_parca', on_delete=models.PROTECT, blank=True, null=True)
    yedek_parca_2 = models.ForeignKey(yedek_parca, related_name='ikinci_parca', on_delete=models.PROTECT, blank=True, null=True)
    yedek_parca_3 = models.ForeignKey(yedek_parca, related_name='ucuncu_parca', on_delete=models.PROTECT, blank=True, null=True)
    yedek_parca_4 = models.ForeignKey(yedek_parca, related_name='dorduncu_parca', on_delete=models.PROTECT, blank=True, null=True)
    yedek_parca_5 = models.ForeignKey(yedek_parca, related_name='besinci_parca', on_delete=models.PROTECT, blank=True, null=True)
    kayit_acilis = models.DateField(default=date.today,)
    kayit_kapanis = models.DateField(default=date.today,)
    tutar = models.PositiveIntegerField()
    aciklama = models.TextField()
    kullanici = models.CharField(max_length=100, default='admin')
    yaratildi = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return(self.ariza_adi)
