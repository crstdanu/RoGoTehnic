from django import forms
from StudiiFezabilitate.models import Lucrare, CertificatUrbanism, AvizeCU
from django.core.exceptions import ValidationError


class LucrareForm(forms.ModelForm):
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
            'nume_intern': forms.TextInput(attrs={'class': 'form-control'}),
            'judet': forms.Select(attrs={'class': 'form-control'}),
            'localitate': forms.Select(attrs={'class': 'form-control'}),
            'adresa': forms.TextInput(attrs={'class': 'form-control'}),
            'firma_proiectare': forms.Select(attrs={'class': 'form-control'}),
            'beneficiar': forms.Select(attrs={'class': 'form-control'}),
            'lot': forms.Select(attrs={'class': 'form-control'}),
            'persoana_contact': forms.Select(attrs={'class': 'form-control'}),
            'finalizata': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            judet = cleaned_data.get("judet")
            localitate = cleaned_data.get("localitate")

            if localitate and judet and localitate.judet != judet:
                self.add_error(
                    'localitate', "Localitatea selectată nu aparține județului ales.")

            return cleaned_data


class CertificatUrbanismForm(forms.ModelForm):
    class Meta:
        model = CertificatUrbanism
        fields = ['numar', 'data', 'emitent', 'nume', 'valabilitate', 'descrierea_proiectului',
                  'inginer_intocmit', 'inginer_verificat', 'suprafata_ocupata', 'lungime_traseu', 'cale_CU']

        labels = {'numar': 'Număr',
                  'data': 'Data',
                  'emitent': 'Emitent CU',
                  'nume': 'Denumire lucrare',
                  'valabilitate': 'Data valabilitate',
                  'descrierea_proiectului': 'Descrierea proiectului',
                  'inginer_intocmit': 'Inginer Întocmit',
                  'inginer_verificat': 'Inginer Verificat',
                  'suprafata_ocupata': 'Suprafața ocupată (m2)',
                  'lungime_traseu': 'Lungime traseu (m)',
                  'cale_CU': 'Cale Certificat de urbanism',
                  }

        widgets = {
            'numar': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'emitent': forms.Select(attrs={'class': 'form-control'}),
            'nume': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Introduceți numele lucrării din Certificatul de Urbanism'}),
            'valabilitate': forms.DateInput(attrs={'class': 'form-control'}),
            'descrierea_proiectului': forms.Textarea(attrs={'class': 'form-control', 'rows': 20, 'placeholder': 'Introduceți descrierea proiectului din Memoriul tehnic'}),
            'inginer_intocmit': forms.Select(attrs={'class': 'form-control'}),
            'inginer_verificat': forms.Select(attrs={'class': 'form-control'}),
            'suprafata_ocupata': forms.NumberInput(attrs={'class': 'form-control'}),
            'lungime_traseu': forms.NumberInput(attrs={'class': 'form-control'}),
            'cale_CU': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Introduceți calea Certificatului de Urbanism'}),

        }


class AvizeCUForm(forms.ModelForm):
    class Meta:
        model = AvizeCU
        fields = ['nume_aviz', 'depus', 'data_depunere', 'primit', 'numar_aviz',
                  'data_aviz', 'cale_aviz', 'descriere_aviz', 'cost_net', 'cost_tva', 'cost_total']
        labels = {
            'nume_aviz': 'Nume aviz',
            'depus': 'Depus',
            'data_depunere': 'Data depunerii',
            'primit': 'Primit',
            'numar_aviz': 'Număr aviz',
            'data_aviz': 'Data aviz',
            'cale_aviz': 'Cale aviz',
            'descriere_aviz': 'Descriere aviz',
            'cost_net': 'Cost Net',
            'cost_tva': 'Cost TVA',
            'cost_total': 'Cost Total',
        }

        widgets = {
            'nume_aviz': forms.Select(attrs={'class': 'form-control'}),
            'depus': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_depunere': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'primit': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'numar_aviz': forms.TextInput(attrs={'class': 'form-control'}),
            'data_aviz': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cale_aviz': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Introduceți calea avizului'}),
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
