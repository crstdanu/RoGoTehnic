from django import forms
from StudiiFezabilitate.models import Lucrare, Localitate
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
