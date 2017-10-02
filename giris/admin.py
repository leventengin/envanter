from django.contrib import admin

# Register your models here.

from .models import grup
from .models import sirket
from .models import ekipman_turu
from .models import servis
from .models import marka
from .models import kategori
from .models import alt_kategori
from .models import yedek_parca
from .models import musteri
from .models import proje
from .models import demirbas
from .models import hareket
from .models import ariza


admin.site.register(grup)
admin.site.register(sirket)
admin.site.register(ekipman_turu)
admin.site.register(servis)
admin.site.register(marka)
admin.site.register(kategori)
admin.site.register(alt_kategori)
admin.site.register(yedek_parca)
admin.site.register(musteri)
admin.site.register(proje)
admin.site.register(demirbas)
admin.site.register(hareket)
admin.site.register(ariza)
