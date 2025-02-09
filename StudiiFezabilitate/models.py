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

    def __str__(self):
        return self.nume


class Localitate(models.Model):
    nume = models.CharField(max_length=100)
    judet = models.ForeignKey(
        Judet, on_delete=models.PROTECT, related_name='localitati')

    class Meta:
        unique_together = ('nume', 'judet')
        verbose_name = "Localitate"
        verbose_name_plural = "Localități"

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
        max_length=10, blank=True, null=True, validators=[numar_ci_validator])
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
        max_length=10, blank=True, null=True, validators=[numar_ci_validator])
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


class Lucrare(models.Model):
    nume = models.CharField(max_length=1000)
    nume_intern = models.CharField(max_length=255, unique=True)
    judet = models.ForeignKey(
        Judet, on_delete=models.PROTECT, related_name='lucrari')
    localitate = models.ForeignKey(
        Localitate, on_delete=models.PROTECT, related_name='lucrari')
    adresa = models.CharField(max_length=512)
    lot = models.ForeignKey(Lot, on_delete=models.PROTECT,
                            blank=True, null=True, related_name='lucrari')
    firma_proiectare = models.ForeignKey(
        FirmaProiectare, on_delete=models.PROTECT)
    beneficiar = models.ForeignKey(
        Beneficiar, on_delete=models.PROTECT)
    persoana_contact = models.ForeignKey(
        PersoanaContact, on_delete=models.PROTECT)
    finalizata = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Lucrare"
        verbose_name_plural = "Lucrări"

    def clean(self):
        validate_localitate(self)

    def __str__(self):
        return self.nume_intern
