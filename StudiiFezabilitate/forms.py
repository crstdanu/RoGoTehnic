from django import forms
from StudiiFezabilitate.models import Lucrare, CertificatUrbanism, UAT
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

    def __init__(self, *args, **kwargs):
        super(CertificatUrbanismForm, self).__init__(*args, **kwargs)
        if 'lucrare' in self.data:
            try:
                lucrare_id = int(self.data.get('lucrare'))
                lucrare = Lucrare.objects.get(id=lucrare_id)
                self.fields['emitent'].queryset = UAT.objects.filter(
                    judet=lucrare.judet)
            except (ValueError, Lucrare.DoesNotExist):
                self.fields['emitent'].queryset = UAT.objects.none()
        elif self.instance.pk:
            self.fields['emitent'].queryset = UAT.objects.filter(
                judet=self.instance.lucrare.judet)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     nume = cleaned_data.get("nume")
    #     lucrare = cleaned_data.get("lucrare")

    #     if nume and lucrare and nume.lucrare != lucrare:
    #         self.add_error(
    #             'nume', "Numele lucrării nu corespunde cu lucrarea selectată.")

    #     return cleaned_data
