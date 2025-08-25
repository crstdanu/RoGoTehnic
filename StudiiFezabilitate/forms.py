from django import forms
from StudiiFezabilitate.models import Lucrare, CertificatUrbanism, AvizeCU, Localitate
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
                # elimină form-control dacă e setat din greșeală
                existing_classes = [
                    c for c in existing_classes if c != 'form-control']
            elif isinstance(widget, forms.CheckboxInput):
                base_class = 'form-check-input'
                # elimină form-control/select eronate
                existing_classes = [c for c in existing_classes if c not in (
                    'form-control', 'form-select')]
            else:
                base_class = 'form-control'
                # elimină form-select dacă a fost adăugat anterior
                existing_classes = [
                    c for c in existing_classes if c != 'form-select']

            if base_class not in existing_classes:
                existing_classes.append(base_class)

            # Adaugă is-invalid dacă există erori pe câmp
            if field_name in self.errors and 'is-invalid' not in existing_classes:
                existing_classes.append('is-invalid')

            widget.attrs['class'] = ' '.join(existing_classes).strip()


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

        if instance and getattr(instance, 'pk', None):
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
                  'cale_plan_situatie_DWG', 'cale_extrase_CF', 'cale_aviz_GIS', 'cale_chitanta_DSP',
                  ]

        labels = {'numar': 'Număr',
                  'data': 'Data',
                  'emitent': 'Emitent CU',
                  'nume': 'Denumire lucrare',
                  'adresa': 'Adresa lucrare',
                  'valabilitate': 'Valabilitate',
                  'descrierea_proiectului': 'Descrierea proiectului',
                  'inginer_intocmit': 'Inginer Întocmit',
                  'inginer_verificat': 'Inginer Verificat',
                  'suprafata_ocupata': 'Suprafața ocupată (m2)',
                  'lungime_traseu': 'Lungime traseu (m)',
                  'cale_CU': 'Cale Certificat de urbanism',
                  'cale_plan_incadrare_CU': 'Cale Plan de încadrare',
                  'cale_plan_situatie_CU': 'Cale Plan de situație',
                  'cale_memoriu_tehnic_CU': 'Cale Memoriu tehnic',
                  'cale_acte_beneficiar': 'Cale acte beneficiar',
                  'cale_acte_facturare': 'Cale acte facturare',
                  'cale_chitanta_APM': 'Cale chitanță APM',
                  'cale_plan_situatie_la_scara': 'Cale plan situație la scară',
                  'cale_plan_situatie_DWG': 'Cale plan situație DWG',
                  'cale_extrase_CF': 'Cale extrase CF',
                  'cale_aviz_GIS': 'Cale aviz GIS',
                  'cale_chitanta_DSP': 'Cale chitanță DSP',
                  }

        widgets = {
            'numar': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(format='%d.%m.%Y', attrs={'class': 'form-control', 'placeholder': 'zz.ll.aaaa', 'data-role': 'datepicker'}),
            'emitent': forms.Select(attrs={'class': 'form-select'}),
            'nume': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Introduceți numele lucrării din Certificatul de Urbanism'}),
            'adresa': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Introduceți adresa lucrării din Certificatul de Urbanism'}),
            'valabilitate': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 60, 'placeholder': 'luni (1-60)'}),
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

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Acceptă dd.mm.yyyy la input și (opțional) ISO ca fallback
        if 'data' in self.fields:
            self.fields['data'].input_formats = ['%d.%m.%Y', '%Y-%m-%d']


class AvizeCUForm(BaseForm):
    class Meta:
        model = AvizeCU
        fields = ['nume_aviz', 'depus', 'data_depunere', 'primit', 'numar_aviz',
                  'data_aviz', 'cale_aviz_eliberat', 'descriere_aviz', 'cost_net', 'cost_tva', 'cost_total',]
        labels = {
            'nume_aviz': 'Nume aviz',
            'depus': 'Depus',
            'data_depunere': 'Data depunerii',
            'primit': 'Primit',
            'numar_aviz': 'Număr aviz',
            'data_aviz': 'Data aviz',
            'cale_aviz_eliberat': 'Cale aviz',
            'descriere_aviz': 'Descriere aviz',
            'cost_net': 'Cost Net',
            'cost_tva': 'Cost TVA',
            'cost_total': 'Cost Total',
        }

        widgets = {
            'nume_aviz': forms.Select(attrs={'class': 'form-select'}),
            'depus': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_depunere': forms.DateInput(format='%d.%m.%Y', attrs={'class': 'form-control', 'placeholder': 'zz.ll.aaaa', 'data-role': 'datepicker'}),
            'primit': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'numar_aviz': forms.TextInput(attrs={'class': 'form-control'}),
            'data_aviz': forms.DateInput(format='%d.%m.%Y', attrs={'class': 'form-control', 'placeholder': 'zz.ll.aaaa', 'data-role': 'datepicker'}),
            'cale_aviz_eliberat': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Introduceți calea avizului'}),
            'descriere_aviz': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Introduceți descrierea avizului'}),
            'cost_net': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_tva': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cost_net'].required = False
        self.fields['cost_tva'].required = False
        self.fields['cost_total'].required = False
        # Acceptă dd.mm.yyyy și (opțional) ISO
        if 'data_depunere' in self.fields:
            self.fields['data_depunere'].input_formats = [
                '%d.%m.%Y', '%Y-%m-%d']
        if 'data_aviz' in self.fields:
            self.fields['data_aviz'].input_formats = ['%d.%m.%Y', '%Y-%m-%d']
