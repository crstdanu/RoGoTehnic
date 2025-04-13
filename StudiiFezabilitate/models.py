from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator, FileExtensionValidator

import os
import magic


# Create your models here.

extension_validator_pdf = FileExtensionValidator(
    allowed_extensions=['pdf'],
    message="Fișierul trebuie să fie în format PDF",
)
extension_validator_dwg = FileExtensionValidator(
    allowed_extensions=['dwg'],
    message="Fișierul trebuie să fie în format DWG"
)

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


def validate_file_mimetype_pdf(file):
    accept = ['application/pdf']
    # Salvăm poziția curentă
    original_position = file.tell()
    # Citim primii 1024 bytes pentru a determina tipul MIME
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    # Resetăm poziția fișierului la poziția inițială
    file.seek(original_position)

    if file_mime_type not in accept:
        raise ValidationError('Fișierul trebuie să fie în format PDF')


def validate_file_mimetype_dwg(file):
    """
    Validează dacă fișierul este în format DWG folosind MIME type și semnătura binară.
    """
    # Lista extinsă de tipuri MIME posibile pentru fișiere DWG
    accept_mime = [
        'application/dwg',
        'drawing/dwg',
        'application/acad',
        'application/x-acad',
        'application/autocad',
        'image/vnd.dwg',
        'application/x-dwg',
        'application/octet-stream'  # Mulți servere web clasifică DWG ca octet-stream
    ]

    # Citim primii bytes pentru detectarea MIME
    file_content = file.read(1024)
    file.seek(0)  # Resetăm poziția fișierului

    file_mime_type = magic.from_buffer(file_content, mime=True)

    # Verificare MIME
    if file_mime_type in accept_mime:
        return

    # Dacă MIME type nu este în lista acceptată, verificăm semnătura DWG
    # Semnăturile DWG încep cu "AC" urmat de versiunea
    file_header = file.read(6)
    file.seek(0)  # Resetăm din nou poziția

    # O listă cu semnături DWG cunoscute (primele 6 bytes)
    dwg_signatures = [
        b'AC1009',  # AutoCAD R12
        b'AC1010',  # AutoCAD R13
        b'AC1012',  # AutoCAD R14
        b'AC1014',  # AutoCAD 2000
        b'AC1015',  # AutoCAD 2000i/2002
        b'AC1018',  # AutoCAD 2004/2005/2006
        b'AC1021',  # AutoCAD 2007/2008/2009
        b'AC1024',  # AutoCAD 2010/2011/2012
        b'AC1027',  # AutoCAD 2013/2014/2015/2016/2017
        b'AC1032'   # AutoCAD 2018+
    ]

    # Verificăm dacă antetul fișierului începe cu una dintre semnăturile cunoscute
    for signature in dwg_signatures:
        if file_header.startswith(signature):
            return

    # Dacă nu am găsit o semnătură validă, ridicăm excepție
    raise ValidationError('Fișierul nu este un format DWG valid')


def cale_upload_CU(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/Certificat_de_urbanism.pdf'


def cale_upload_plan_incadrare_CU(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/Plan_de_incadrare.pdf'


def cale_upload_plan_situatie_CU(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/Plan_de_situatie.pdf'


def cale_upload_memoriu_tehnic_CU(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/Memoriu_tehnic.pdf'


def cale_upload_acte_beneficiar(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/Acte beneficiar/Acte_beneficiar.pdf'


def cale_upload_acte_facturare(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/Acte_facturare.pdf'


def cale_upload_chitanta_APM(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/Chitanta_APM.pdf'


def cale_upload_plan_situatie_la_scara(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/Plan_situatie_-_la_scara.pdf'


def cale_upload_plan_situatie_DWG(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/Plan_situatie.dwg'


def cale_upload_extrase_CF(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/Extrase_CF.pdf'


def cale_upload_aviz_GIS(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/Aviz_GIS.pdf'


def cale_upload_ATR(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/ATR.pdf'


def cale_upload_aviz_CTE(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/Aviz_CTE.pdf'


def cale_upload_chitanta_DSP(instance, filename):
    return f'SF/{instance.lucrare.nume_intern}/CU/Chitanta_DSP.pdf'


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
        return f"ing. {self.nume} {self.prenume}"


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
        Lucrare, on_delete=models.CASCADE, related_name='certificat_urbanism')
    valabilitate = models.PositiveIntegerField(
        validators=[MaxValueValidator(
            limit_value=60,
            message="Valoarea trebuie să fie mai mică sau egală cu 60.")],
        default=12,
        blank=True, null=True,)
    # Date obligatorii
    descrierea_proiectului = models.TextField()
    inginer_intocmit = models.ForeignKey(
        Inginer, on_delete=models.SET_NULL, default=2, null=True, related_name='certificat_urbanism_intocmit')
    inginer_verificat = models.ForeignKey(
        Inginer, on_delete=models.SET_NULL, default=1, null=True, related_name='certificat_urbanism_verificat')
    # Date optionale
    suprafata_ocupata = models.IntegerField(blank=True, null=True,)
    lungime_traseu = models.IntegerField(blank=True, null=True,)
    # ATASAMENTE
    cale_CU = models.FileField(
        upload_to=cale_upload_CU, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True)
    cale_plan_incadrare_CU = models.FileField(
        upload_to=cale_upload_plan_incadrare_CU, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True,)
    cale_plan_situatie_CU = models.FileField(
        upload_to=cale_upload_plan_situatie_CU, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True,)
    cale_memoriu_tehnic_CU = models.FileField(
        upload_to=cale_upload_memoriu_tehnic_CU, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True,)
    cale_acte_beneficiar = models.FileField(
        upload_to=cale_upload_acte_beneficiar, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True,)
    cale_acte_facturare = models.FileField(
        upload_to=cale_upload_acte_facturare, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True,)
    cale_chitanta_APM = models.FileField(
        upload_to=cale_upload_chitanta_APM, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True,)
    cale_plan_situatie_la_scara = models.FileField(
        upload_to=cale_upload_plan_situatie_la_scara, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True,)
    cale_plan_situatie_DWG = models.FileField(
        upload_to=cale_upload_plan_situatie_DWG, validators=[extension_validator_dwg, validate_file_mimetype_dwg], blank=True, null=True,)
    cale_extrase_CF = models.FileField(
        upload_to=cale_upload_extrase_CF, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True,)
    cale_aviz_GIS = models.FileField(
        upload_to=cale_upload_aviz_GIS, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True,)
    cale_ATR = models.FileField(
        upload_to=cale_upload_ATR, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True,)
    cale_aviz_CTE = models.FileField(
        upload_to=cale_upload_aviz_CTE, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True,)
    cale_chitanta_DSP = models.FileField(
        upload_to=cale_upload_chitanta_DSP, validators=[extension_validator_pdf, validate_file_mimetype_pdf], blank=True, null=True,)

    class Meta:
        verbose_name = "Certificat de urbanism"
        verbose_name_plural = "Certificate de urbanism"

    def clean(self):
        # Validează că UAT-ul (emitent) aparține aceluiași județ ca lucrarea
        # Verificăm mai întâi dacă avem emitent_id pentru a evita eroarea RelatedObjectDoesNotExist
        if hasattr(self, 'emitent_id') and self.emitent_id and self.lucrare_id:
            # Încărcăm explicit obiectele pentru a asigura că există
            try:
                emitent = UAT.objects.get(pk=self.emitent_id)
                lucrare = Lucrare.objects.get(pk=self.lucrare_id)

                # Verificăm județele
                if emitent.judet and lucrare.judet and emitent.judet != lucrare.judet:
                    raise ValidationError({
                        'emitent': "UAT-ul emitent trebuie să aparțină aceluiași județ ca lucrarea."
                    })
            except (UAT.DoesNotExist, Lucrare.DoesNotExist):
                # Dacă unul dintre obiecte nu există, nu validăm această regulă
                pass

        super().clean()

    def __str__(self):
        return f"CU pentru {self.lucrare.nume_intern}"

    def save(self, *args, **kwargs):
        # Apelăm metoda clean() pentru a asigura validarea înainte de salvare
        self.full_clean()

        if self.pk:  # Dacă obiectul există deja în DB
            try:
                old_instance = CertificatUrbanism.objects.get(pk=self.pk)
                if old_instance.cale_CU and self.cale_CU and self.cale_CU != old_instance.cale_CU:
                    old_file_path = old_instance.cale_CU.path
                    if os.path.isfile(old_file_path):
                        # Ștergem fișierul vechi înainte de a salva noul fișier
                        os.remove(old_file_path)
            except CertificatUrbanism.DoesNotExist:
                pass

        super().save(*args, **kwargs)


class AvizeCU(models.Model):
    certificat_urbanism = models.ForeignKey(
        CertificatUrbanism, on_delete=models.CASCADE, related_name='avize_certificat')
    nume_aviz = models.ForeignKey(
        Aviz, on_delete=models.PROTECT, related_name='certificat_avize')
    depus = models.BooleanField(default=False,)
    data_depunere = models.DateField(blank=True, null=True,)
    primit = models.BooleanField(default=False)
    numar_aviz = models.CharField(max_length=100, blank=True, null=True,)
    data_aviz = models.DateField(blank=True, null=True,)
    cale_aviz = models.CharField(max_length=512, blank=True, null=True,)
    descriere_aviz = models.TextField(blank=True, null=True,)
    cost_net = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00, blank=True, null=True,)
    cost_tva = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00, blank=True, null=True,)
    cost_total = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00, blank=True, null=True,)

    class Meta:
        verbose_name = "AvizCU"
        verbose_name_plural = "AvizeCU"
        unique_together = ('certificat_urbanism', 'nume_aviz')

    def clean(self):
        # Validează că avizul aparține aceluiași județ ca lucrarea
        if hasattr(self, 'nume_aviz_id') and self.nume_aviz_id and hasattr(self, 'certificat_urbanism_id') and self.certificat_urbanism_id:
            try:
                aviz = Aviz.objects.get(pk=self.nume_aviz_id)
                certificat = CertificatUrbanism.objects.get(
                    pk=self.certificat_urbanism_id)

                # Verificăm județele
                if aviz.judet and certificat.lucrare.judet and aviz.judet != certificat.lucrare.judet:
                    raise ValidationError({
                        'nume_aviz': "Avizul trebuie să aparțină aceluiași județ ca lucrarea."
                    })
            except (Aviz.DoesNotExist, CertificatUrbanism.DoesNotExist):
                # Dacă unul dintre obiecte nu există, nu validăm această regulă
                pass

        super().clean()

    def __str__(self):
        return f"{self.nume_aviz.nume} pentru {self.certificat_urbanism.lucrare.nume_intern}"
