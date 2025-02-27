from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.

cnp_validator = RegexValidator(
    regex=r'^[0-9]{13}$', message='CNP-ul trebuie să conțină exact 13 cifre')

numar_ci_validator = RegexValidator(
    regex=r'^[0-9]{6}$', message='Numărul CI trebuie să conțină exact 6 cifre')

serie_ci_validator = RegexValidator(
    regex=r'^[A-Za-z]{2}$', message='Seria CI trebuie să conțină exact 2 litere')


def validate_localitate(lucrare):
    if lucrare.localitate.judet != lucrare.judet:
        raise ValidationError(
            "Localitatea aleasă nu aparține județului selectat."
        )


class Judet(models.Model):
    nume = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Județ'
        verbose_name_plural = 'Județe'
        ordering = ['nume']

    def __str__(self):
        return self.nume


class Localitate(models.Model):
    nume = models.CharField(max_length=100)
    judet = models.ForeignKey(
        Judet, on_delete=models.PROTECT, related_name='localitati')

    TIP_CHOICES = [
        ('Municipiul', 'Municipiul'),
        ('Orașul', 'Orașul'),
        ('Comuna', 'Comuna'),
    ]
    tip = models.CharField(
        max_length=16, choices=TIP_CHOICES, null=True, blank=True)

    class Meta:
        unique_together = ('nume', 'judet')
        verbose_name = "Localitate"
        verbose_name_plural = "Localități"
        ordering = ['nume']

    def __str__(self):
        return f"{self.tip} {self.nume}"


class UAT(models.Model):
    nume = models.CharField(max_length=100)
    judet = models.ForeignKey(
        Judet, on_delete=models.PROTECT, blank=True, null=True, related_name='UAT',)
    localitate = models.ForeignKey(
        Localitate, on_delete=models.PROTECT, blank=True, null=True, related_name='UAT')
    adresa = models.CharField(max_length=512, blank=True, null=True,)
    cod_postal = models.CharField(max_length=6, blank=True, null=True,)
    telefon = models.CharField(max_length=20)
    email = models.EmailField()
    cont_trezorerie = models.CharField(max_length=30, blank=True, null=True,)

    class Meta:
        verbose_name = "Unitate administrativ teritorială"
        verbose_name_plural = "Unități administrativ teritoriale"

    def __str__(self):
        return f"{self.nume}"


class Inginer(models.Model):
    nume = models.CharField(max_length=100)
    prenume = models.CharField(max_length=100)
    judet = models.ForeignKey(
        Judet, on_delete=models.PROTECT, blank=True, null=True, related_name='ingineri',)
    localitate = models.ForeignKey(
        Localitate, on_delete=models.PROTECT, blank=True, null=True, related_name='ingineri')
    adresa = models.CharField(max_length=512, blank=True, null=True,)
    telefon = models.CharField(max_length=20)
    cnp = models.CharField(max_length=13, unique=True,
                           blank=True, null=True, validators=[cnp_validator])
    serie_ci = models.CharField(
        max_length=2, blank=True, null=True, validators=[serie_ci_validator])
    numar_ci = models.CharField(
        max_length=6, blank=True, null=True, validators=[numar_ci_validator])
    data_ci = models.DateField(blank=True, null=True,)
    cale_ci = models.CharField(max_length=512, blank=True, null=True,)
    cale_semnatura = models.CharField(max_length=512, blank=True, null=True,)

    class Meta:
        verbose_name = "Inginer"
        verbose_name_plural = "Ingineri"

    def save(self, *args, **kwargs):
        if self.serie_ci:  # Dacă este completat
            self.serie_ci = self.serie_ci.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nume} {self.prenume}"


class Lot(models.Model):
    nume = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Lot"
        verbose_name_plural = "Loturi"

    def __str__(self):
        return self.nume


class PersoanaContact(models.Model):
    nume = models.CharField(max_length=100)
    prenume = models.CharField(max_length=100)
    judet = models.ForeignKey(
        Judet, on_delete=models.PROTECT, related_name='persoane_contact', blank=True, null=True,)
    localitate = models.ForeignKey(
        Localitate, on_delete=models.PROTECT, related_name='persoane_contact', blank=True, null=True,)
    adresa = models.CharField(max_length=512, blank=True, null=True,)
    telefon = models.CharField(max_length=20)
    cnp = models.CharField(max_length=13, unique=True,
                           blank=True, null=True, validators=[cnp_validator])
    serie_ci = models.CharField(
        max_length=2, blank=True, null=True, validators=[serie_ci_validator])
    numar_ci = models.CharField(
        max_length=6, blank=True, null=True, validators=[numar_ci_validator])
    data_ci = models.DateField(blank=True, null=True,)
    cale_ci = models.CharField(max_length=512, blank=True, null=True,)
    cale_semnatura = models.CharField(max_length=512, blank=True, null=True,)

    class Meta:
        verbose_name = "Persoană de contact"
        verbose_name_plural = "Persoane de contact"

    def save(self, *args, **kwargs):
        if self.serie_ci:  # Dacă este completat
            self.serie_ci = self.serie_ci.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nume} {self.prenume}"


class FirmaProiectare(models.Model):
    nume = models.CharField(max_length=1000)
    judet = models.ForeignKey(
        Judet, on_delete=models.PROTECT, related_name='firme_proiectare')
    localitate = models.ForeignKey(
        Localitate, on_delete=models.PROTECT, related_name='firme_proiectare')
    adresa = models.CharField(max_length=512)
    cui = models.CharField(max_length=20, unique=True)
    nr_reg_com = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    telefon = models.CharField(max_length=20, blank=True, null=True,)
    reprezentant = models.ForeignKey(
        PersoanaContact, on_delete=models.PROTECT, related_name='firme_proiectare', blank=True, null=True,)
    cale_stampila = models.CharField(max_length=512, blank=True, null=True,)
    cale_certificat = models.CharField(max_length=512, blank=True, null=True,)

    class Meta:
        verbose_name = "Firmă de proiectare"
        verbose_name_plural = "Firme de proiectare"

    def __str__(self):
        return self.nume


class Beneficiar(models.Model):
    nume = models.CharField(max_length=1000)
    judet = models.ForeignKey(
        Judet, on_delete=models.PROTECT, related_name='beneficiari', blank=True, null=True,)
    localitate = models.ForeignKey(
        Localitate, on_delete=models.PROTECT, related_name='beneficiari', blank=True, null=True,)
    adresa = models.CharField(max_length=512, blank=True, null=True,)
    cui = models.CharField(max_length=20, unique=True, blank=True, null=True,)
    nr_reg_com = models.CharField(
        max_length=20, unique=True, blank=True, null=True,)
    email = models.EmailField(blank=True, null=True,)
    telefon = models.CharField(max_length=20, blank=True, null=True,)
    persoana_contact = models.ForeignKey(
        PersoanaContact, on_delete=models.PROTECT, related_name='beneficiari', blank=True, null=True,)
    cale_stampila = models.CharField(max_length=512, blank=True, null=True,)
    cale_certificat = models.CharField(max_length=512, blank=True, null=True,)

    class Meta:
        verbose_name = "Beneficiar"
        verbose_name_plural = "Beneficiari"

    def __str__(self):
        return self.nume


class Aviz(models.Model):
    nume = models.CharField(max_length=100)
    judet = models.ForeignKey(
        Judet, on_delete=models.PROTECT, related_name='avize')
    descriere = models.TextField(blank=True, null=True,)

    class Meta:
        verbose_name = "Aviz"
        verbose_name_plural = "Avize"

    def __str__(self):
        return self.nume


class Lucrare(models.Model):
    nume_intern = models.CharField(max_length=255, unique=True)
    nume = models.CharField(max_length=1000, blank=True, null=True,)
    judet = models.ForeignKey(
        Judet, on_delete=models.PROTECT, related_name='lucrari')
    localitate = models.ForeignKey(
        Localitate, on_delete=models.PROTECT, related_name='lucrari')
    adresa = models.CharField(max_length=512)
    lot = models.ForeignKey(Lot, on_delete=models.PROTECT,
                            blank=True, null=True, related_name='lucrari')
    firma_proiectare = models.ForeignKey(
        FirmaProiectare, on_delete=models.SET_NULL, null=True, default=1, related_name='lucrari')
    beneficiar = models.ForeignKey(
        Beneficiar, on_delete=models.SET_NULL, null=True, default=1, related_name='lucrari')
    persoana_contact = models.ForeignKey(
        PersoanaContact, on_delete=models.PROTECT)
    finalizata = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Lucrare"
        verbose_name_plural = "Lucrări"
        ordering = ['nume_intern']

    def clean(self):
        if self.localitate and self.judet and self.localitate.judet != self.judet:
            raise ValidationError(
                {'localitate': "Localitatea selectata nu aparține județului ales."})

    def save(self, *args, **kwargs):
        if self.pk:  # Dacă lucrarea există deja în baza de date
            lucrare_veche = Lucrare.objects.get(pk=self.pk)
            if lucrare_veche.finalizata and self.finalizata:
                raise ValidationError(
                    "Lucrarea finalizată nu poate fi modificată.")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nume_intern


class CertificatUrbanism(models.Model):
    # date despre CU
    numar = models.CharField(max_length=100)
    data = models.DateField()
    emitent = models.ForeignKey(UAT, on_delete=models.PROTECT)
    nume = models.CharField(max_length=2000, blank=True, null=True,)
    lucrare = models.OneToOneField(
        Lucrare, on_delete=models.PROTECT, related_name='certificat_urbanism')
    valabilitate = models.DateField()
    # Date obligatorii
    descrierea_proiectului = models.TextField()
    inginer_intocmit = models.ForeignKey(
        Inginer, on_delete=models.SET_NULL, default=2, null=True, related_name='certificat_urbanism_intocmit')
    inginer_verificat = models.ForeignKey(
        Inginer, on_delete=models.PROTECT, default=1, null=True, related_name='certificat_urbanism_verificat')
    # Date optionale
    suprafata_ocupata = models.IntegerField(blank=True, null=True,)
    lungime_traseu = models.IntegerField(blank=True, null=True,)
    # atasamente obligatorii
    cale_CU = models.CharField(max_length=512, blank=True, null=True,)
    cale_plan_incadrare_CU = models.CharField(
        max_length=512, blank=True, null=True,)
    cale_plan_situatie_CU = models.CharField(
        max_length=512, blank=True, null=True,)
    cale_acte_beneficiar = models.CharField(
        max_length=512, blank=True, null=True,)
    cale_acte_facturare = models.CharField(
        max_length=512, blank=True, null=True,)
    cale_chitanta_APM = models.CharField(
        max_length=512, blank=True, null=True,)
    # atasamente optionale
    cale_plan_situatie_PDF = models.CharField(
        max_length=512, blank=True, null=True,)
    cale_plan_topo_DWG = models.CharField(
        max_length=512, blank=True, null=True,)
    cale_extrase_CF = models.CharField(max_length=512, blank=True, null=True,)
    cale_aviz_GIS = models.CharField(max_length=512, blank=True, null=True,)
    cale_ATR = models.CharField(max_length=512, blank=True, null=True,)
    cale_aviz_CTE = models.CharField(max_length=512, blank=True, null=True,)
    cale_chitanta_DSP = models.CharField(
        max_length=512, blank=True, null=True,)

    class Meta:
        verbose_name = "Certificat de urbanism"
        verbose_name_plural = "Certificate de urbanism"

    def __str__(self):
        return f"CU pentru {self.lucrare.nume_intern}"


class AvizeCU(models.Model):
    certificat_urbanism = models.ForeignKey(
        CertificatUrbanism, on_delete=models.PROTECT, related_name='avize_certificat')
    nume_aviz = models.ForeignKey(
        Aviz, on_delete=models.PROTECT, related_name='certificat_avize')
    depus = models.BooleanField(default=False)
    data_depunere = models.DateField(blank=True, null=True,)
    primit = models.BooleanField(default=False)
    numar_aviz = models.CharField(max_length=100, blank=True, null=True,)
    data_aviz = models.DateField(blank=True, null=True,)
    cale_aviz = models.CharField(max_length=512, blank=True, null=True,)
    descriere_aviz = models.TextField(blank=True, null=True,)
    cost_net = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00)
    cost_tva = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00)
    cost_total = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "AvizCU"
        verbose_name_plural = "AvizeCU"
        unique_together = ('certificat_urbanism', 'nume_aviz')

    def save(self, *args, **kwargs):
        # Setează automat cost_total înainte de a salva
        self.cost_total = self.cost_net + self.cost_tva
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nume_aviz.nume} pentru {self.certificat_urbanism.lucrare.nume_intern}"
