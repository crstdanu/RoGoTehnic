from django.contrib import admin
from StudiiFezabilitate.models import Judet, Localitate, Inginer, Lot, Lucrare, FirmaProiectare, Beneficiar, PersoanaContact, Aviz, AvizeCU, UAT, CertificatUrbanism


admin.site.register(Judet)
admin.site.register(Localitate)
admin.site.register(Inginer)
admin.site.register(Lot)
admin.site.register(PersoanaContact)
admin.site.register(FirmaProiectare)
admin.site.register(Beneficiar)
admin.site.register(Lucrare)
admin.site.register(Aviz)
admin.site.register(AvizeCU)
admin.site.register(UAT)
admin.site.register(CertificatUrbanism)
