import csv
from django.core.management.base import BaseCommand
from StudiiFezabilitate.models import Judet, Localitate
import os


class Command(BaseCommand):
    help = 'Populează tabela Localitate cu date din localitati_IASI.csv'

    def handle(self, *args, **options):
        # Calea absolută către fișierul CSV
        base_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        csv_path = os.path.join(
            base_dir, 'management', 'localitati_BOTOSANI.csv')

        localitati_adaugate = 0
        localitati_existente = 0

        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                judet_nume = row['Judet'].strip()
                localitate_nume = row['Nume'].strip()
                tip = row['Tip'].strip()

                # Caută sau creează județul
                judet, _ = Judet.objects.get_or_create(nume=judet_nume)

                # Verifică dacă localitatea există deja
                try:
                    localitate = Localitate.objects.get(
                        nume=localitate_nume,
                        judet=judet
                    )
                    localitati_existente += 1
                    self.stdout.write(
                        f"Localitatea {localitate_nume}, {judet_nume} există deja")
                except Localitate.DoesNotExist:
                    # Creează localitatea doar dacă nu există
                    localitate = Localitate.objects.create(
                        nume=localitate_nume,
                        judet=judet,
                        tip=tip
                    )
                    localitati_adaugate += 1
                    self.stdout.write(
                        f"Adăugată localitatea {localitate_nume}, {judet_nume}")

        self.stdout.write(
            self.style.SUCCESS(
                f'Import localități finalizat! '
                f'Adăugate: {localitati_adaugate}, '
                f'Existente deja: {localitati_existente}'
            )
        )
