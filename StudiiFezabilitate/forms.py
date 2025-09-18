from django import forms
from django.forms import inlineformset_factory
from StudiiFezabilitate.models import (
    Lucrare,
    CertificatUrbanism,
    AvizeCU,
    Localitate,
    UAT,
    AvizCheltuiala,
)
from django.core.exceptions import ValidationError


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            # Bootstrap 5: select -> form-select, checkbox -> form-check-input, rest -> form-control
            existing_classes = widget.attrs.get('class', '').split()

            # Decide baza în funcție de tipul widgetului
            if isinstance(widget, (forms.Select, forms.SelectMultiple)):
                base_class = 'form-select'
                existing_classes = [
                    c for c in existing_classes if c != 'form-control']
            elif isinstance(widget, forms.CheckboxInput):
                base_class = 'form-check-input'
                existing_classes = [c for c in existing_classes if c not in (
                    'form-control', 'form-select')]
            else:
                base_class = 'form-control'
                existing_classes = [
                    c for c in existing_classes if c != 'form-select']

            if base_class not in existing_classes:
                existing_classes.append(base_class)

            widget.attrs['class'] = ' '.join(existing_classes).strip()

    def full_clean(self):
        # Rulează validarea standard
        super().full_clean()
        # Marchează câmpurile cu erori cu clasa Bootstrap 'is-invalid'
        for field_name in getattr(self, 'errors', {}):
            if field_name in self.fields:
                widget = self.fields[field_name].widget
                existing = widget.attrs.get('class', '').split()
                if 'is-invalid' not in existing:
                    existing.append('is-invalid')
                    widget.attrs['class'] = ' '.join(existing).strip()


class LucrareForm(BaseForm):
    class Meta:
        model = Lucrare
        fields = ['nume', 'nume_intern', 'judet', 'localitate', 'adresa',
                  'firma_proiectare', 'beneficiar', 'lot', 'persoana_contact', 'finalizata']
        labels = {
            'nume': 'Nume lucrare',
            'nume_intern': 'Nume intern',
            'judet': 'Județ',
            'localitate': 'Localitate',
            'adresa': 'Adresa',
            'firma_proiectare': 'Firmă de proiectare',
            'beneficiar': 'Beneficiar',
            'lot': 'Lot',
            'persoana_contact': 'Persoană de contact',
            'finalizata': 'Finalizată',
        }
        widgets = {
            'nume': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Introduceți numele complet al lucrării'}),
            'nume_intern': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduceți numele scurt al lucrării'}),
            'judet': forms.Select(attrs={'class': 'form-select'}),
            'localitate': forms.Select(attrs={'class': 'form-select'}),
            'adresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduceți adresa (fără județ sau localitate)'}),
            'firma_proiectare': forms.Select(attrs={'class': 'form-select'}),
            'beneficiar': forms.Select(attrs={'class': 'form-select'}),
            'lot': forms.Select(attrs={'class': 'form-select'}),
            'persoana_contact': forms.Select(attrs={'class': 'form-select'}),
            'finalizata': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Folosește self.instance (setată de ModelForm) după super().__init__
        instance = getattr(self, 'instance', None)

        # 1) Dacă formularul este BOUND (POST/GET cu date), folosim JUDEȚ-ul din datele trimise
        if self.is_bound:
            try:
                posted_judet = self.data.get('judet')
                if posted_judet:
                    judet_id = int(posted_judet)
                    self.fields['localitate'].queryset = Localitate.objects.filter(
                        judet_id=judet_id
                    ).order_by('nume')
            except (TypeError, ValueError):
                # Lăsăm queryset-ul neschimbat dacă judet nu e valid în date
                pass

            # Păstrăm selecția utilizatorului pentru re-randare (util pentru JS dependent)
            posted_localitate = self.data.get('localitate')
            if posted_localitate:
                self.fields['localitate'].widget.attrs['data-selected'] = str(
                    posted_localitate)

        # 2) Altfel (formular nelegat), la editare folosim JUDEȚ-ul instanței pentru a filtra localitățile
        elif instance and getattr(instance, 'pk', None):
            if instance.judet_id:
                # Filtrează opțiunile pentru câmpul localitate doar la cele care aparțin județului instanței
                self.fields['localitate'].queryset = Localitate.objects.filter(
                    judet=instance.judet)
            if getattr(instance, 'localitate_id', None):
                # Ajută JS-ul dependent să preselecteze valoarea existentă
                self.fields['localitate'].widget.attrs['data-selected'] = str(
                    instance.localitate_id)

    def clean(self):
        cleaned_data = super().clean()
        judet = cleaned_data.get("judet")
        localitate = cleaned_data.get("localitate")

        if localitate and judet and localitate.judet != judet:
            self.add_error(
                'localitate', "Localitatea selectată nu aparține județului ales.")

        return cleaned_data


class CertificatUrbanismForm(BaseForm):
    class Meta:
        model = CertificatUrbanism
        fields = ['numar', 'data', 'emitent', 'nume', 'adresa', 'valabilitate', 'descrierea_proiectului',
                  'inginer_intocmit', 'inginer_verificat', 'suprafata_ocupata', 'lungime_traseu',
                  'cale_CU', 'cale_plan_incadrare_CU', 'cale_plan_situatie_CU', 'cale_memoriu_tehnic_CU', 'cale_acte_beneficiar',
                  'cale_acte_facturare', 'cale_chitanta_APM', 'cale_plan_situatie_la_scara',
                  'cale_plan_situatie_DWG', 'cale_extrase_CF', 'cale_aviz_GIS', 'cale_chitanta_DSP', 'cale_chitanta_IPJ_Botosani',
                  ]
        labels = {
            'numar': 'Număr',
            'data': 'Data',
            'emitent': 'Emitent CU',
            'nume': 'Denumire lucrare',
            'adresa': 'Adresa lucrare',
            'valabilitate': 'Valabilitate (luni)',
            'descrierea_proiectului': 'Descrierea proiectului',
            'inginer_intocmit': 'Inginer Întocmit',
            'inginer_verificat': 'Inginer Verificat',
            'suprafata_ocupata': 'Suprafața ocupată (m2)',
            'lungime_traseu': 'Lungime traseu (m)',
            'cale_CU': 'Cale Certificat de urbanism',
            'cale_plan_incadrare_CU': 'Cale Plan de încadrare',
            'cale_plan_situatie_CU': 'Cale Plan de situație',
            'cale_memoriu_tehnic_CU': 'Cale Memoriu tehnic',
            'cale_acte_beneficiar': 'Cale Acte beneficiar',
            'cale_acte_facturare': 'Cale Acte facturare',
            'cale_chitanta_APM': 'Cale Chitanță APM',
            'cale_plan_situatie_la_scara': 'Cale Plan situație la scară',
            'cale_plan_situatie_DWG': 'Cale Plan situație DWG',
            'cale_extrase_CF': 'Cale Extrase CF',
            'cale_aviz_GIS': 'Cale Aviz GIS',
            'cale_chitanta_DSP': 'Cale Chitanță DSP',
            'cale_chitanta_IPJ_Botosani': 'Cale Chitanță IPJ Botoșani',
        }

        widgets = {
            'numar': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(format='%d.%m.%Y', attrs={'class': 'form-control', 'placeholder': 'zz.ll.aaaa', 'data-role': 'datepicker'}),
            'emitent': forms.Select(attrs={'class': 'form-select'}),
            'nume': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Introduceți Numele lucrării din Certificatul de Urbanism'}),
            'adresa': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Introduceți Adresa COMPLETĂ a lucrării din Certificatul de Urbanism'}),
            'valabilitate': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 60}),
            'descrierea_proiectului': forms.Textarea(attrs={'class': 'form-control', 'rows': 20, 'placeholder': 'Introduceți descrierea proiectului din Memoriul tehnic'}),
            'inginer_intocmit': forms.Select(attrs={'class': 'form-select'}),
            'inginer_verificat': forms.Select(attrs={'class': 'form-select'}),
            'suprafata_ocupata': forms.NumberInput(attrs={'class': 'form-control'}),
            'lungime_traseu': forms.NumberInput(attrs={'class': 'form-control'}),
            'cale_CU': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'cale_plan_incadrare_CU': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'cale_plan_situatie_CU': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'cale_memoriu_tehnic_CU': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'cale_acte_beneficiar': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'cale_acte_facturare': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'cale_chitanta_APM': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'cale_plan_situatie_la_scara': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'cale_plan_situatie_DWG': forms.FileInput(attrs={'class': 'form-control', 'accept': '.dwg'}),
            'cale_extrase_CF': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'cale_aviz_GIS': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'cale_chitanta_DSP': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'cale_chitanta_IPJ_Botosani': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),

        }

    def __init__(self, *args, **kwargs):
        # Permite trecerea explicită a lucrării pentru filtrare emitent
        lucrare = kwargs.pop('lucrare', None)
        super().__init__(*args, **kwargs)
        # Derivă lucrarea din instanță dacă nu a fost furnizată separat
        if lucrare is None and getattr(self.instance, 'lucrare_id', None):
            lucrare = self.instance.lucrare
        # Stochează pentru validare ulterioară
        self._lucrare = lucrare
        # Filtrează emitent la UAT din același județ cu lucrarea
        if lucrare and getattr(lucrare, 'judet_id', None):
            self.fields['emitent'].queryset = UAT.objects.filter(
                judet=lucrare.judet).order_by('nume')
        # Acceptă dd.mm.yyyy la input și (opțional) ISO ca fallback
        if 'data' in self.fields:
            self.fields['data'].input_formats = ['%d.%m.%Y', '%Y-%m-%d']
        # Setează 12 ca valoare implicită pentru formulare noi
        if 'valabilitate' in self.fields and not getattr(self.instance, 'pk', None):
            self.fields['valabilitate'].initial = 12

    def clean(self):
        cleaned = super().clean()
        emitent = cleaned.get('emitent')
        lucrare = self._lucrare if hasattr(self, '_lucrare') else None
        if not lucrare and getattr(self.instance, 'lucrare_id', None):
            lucrare = self.instance.lucrare
        if lucrare and emitent and getattr(emitent, 'judet_id', None) != getattr(lucrare, 'judet_id', None):
            self.add_error(
                'emitent', 'Emitentul trebuie să fie din același județ cu lucrarea.')
        return cleaned


class AvizeCUForm(BaseForm):
    class Meta:
        model = AvizeCU
        fields = ['nume_aviz', 'depus', 'data_depunere', 'primit', 'numar_aviz',
                  'data_aviz', 'cale_aviz_eliberat', 'descriere_aviz']
        labels = {
            'nume_aviz': 'Nume aviz',
            'depus': 'Depus',
            'data_depunere': 'Data depunerii',
            'primit': 'Primit',
            'numar_aviz': 'Număr aviz',
            'data_aviz': 'Data aviz',
            'cale_aviz_eliberat': 'Cale aviz',
            'descriere_aviz': 'Descriere aviz',
        }

        widgets = {
            'nume_aviz': forms.Select(attrs={'class': 'form-select'}),
            'depus': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_depunere': forms.DateInput(format='%d.%m.%Y', attrs={'class': 'form-control', 'placeholder': 'zz.ll.aaaa', 'data-role': 'datepicker'}),
            'primit': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'numar_aviz': forms.TextInput(attrs={'class': 'form-control'}),
            'data_aviz': forms.DateInput(format='%d.%m.%Y', attrs={'class': 'form-control', 'placeholder': 'zz.ll.aaaa', 'data-role': 'datepicker'}),
            # Cale aviz este un fișier încărcat (FileField) – folosim input de fișier
            'cale_aviz_eliberat': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'descriere_aviz': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Introduceți descrierea avizului'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Acceptă dd.mm.yyyy și (opțional) ISO
        if 'data_depunere' in self.fields:
            self.fields['data_depunere'].input_formats = [
                '%d.%m.%Y', '%Y-%m-%d']
        if 'data_aviz' in self.fields:
            self.fields['data_aviz'].input_formats = ['%d.%m.%Y', '%Y-%m-%d']
        # Dacă edităm o instanță existentă, filtrează nume_aviz la județul lucrării pentru UX
        try:
            instance = getattr(self, 'instance', None)
            if instance and getattr(instance, 'pk', None):
                cu = getattr(instance, 'certificat_urbanism', None)
                lucrare = getattr(cu, 'lucrare', None)
                judet = getattr(lucrare, 'judet', None)
                if judet is not None and 'nume_aviz' in self.fields:
                    from StudiiFezabilitate.models import Aviz
                    self.fields['nume_aviz'].queryset = Aviz.objects.filter(
                        judet=judet).order_by('nume')
        except Exception:
            pass

    def clean(self):
        cleaned = super().clean()
        # Previne duplicatele la editare: același (certificat_urbanism, nume_aviz)
        try:
            instance = getattr(self, 'instance', None)
            if instance and getattr(instance, 'pk', None):
                cu = getattr(instance, 'certificat_urbanism', None)
                nume_aviz = cleaned.get('nume_aviz')
                if cu and nume_aviz:
                    from StudiiFezabilitate.models import AvizeCU
                    exists = AvizeCU.objects.filter(
                        certificat_urbanism=cu,
                        nume_aviz=nume_aviz
                    ).exclude(pk=instance.pk).exists()
                    if exists:
                        self.add_error(
                            'nume_aviz', 'Acest aviz este deja adăugat pentru certificatul curent.')
        except Exception:
            # Fără blocaj dacă există probleme de context; validarea modelului/DB va prinde oricum
            pass
        return cleaned


class AvizCheltuialaForm(BaseForm):
    class Meta:
        model = AvizCheltuiala
        fields = ['tip', 'suma', 'include_tva', 'tva',
                  'document', 'dovada_plata']
        labels = {
            'tip': 'Tip',
            'suma': 'Sumă',
            'include_tva': 'Suma contine TVA',
            'tva': 'Cotă TVA',
            'document': 'Document (factură/taxă)',
            'dovada_plata': 'Dovadă plată',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pentru formularele noi/necompletate, bifa 'Suma contine TVA' să fie activă by default
        if not self.is_bound:
            try:
                if not getattr(self.instance, 'pk', None):
                    self.fields['include_tva'].initial = True
            except Exception:
                self.fields['include_tva'].initial = True


# Inline formset pentru cheltuieli asociate unui AvizeCU
AvizCheltuialaFormSet = inlineformset_factory(
    AvizeCU,
    AvizCheltuiala,
    form=AvizCheltuialaForm,
    extra=0,
    can_delete=True
)
