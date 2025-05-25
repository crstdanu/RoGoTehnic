import csv
from django.core.management.base import BaseCommand
from StudiiFezabilitate.models import Judet, Localitate, UAT
import os


class Command(BaseCommand):
    help = 'Populează tabela UAT cu date din localitati_IASI.csv'

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        csv_path = os.path.join(base_dir, 'management',
                                'localitati_BOTOSANI.csv')

        uat_adaugate = 0
        uat_existente = 0

        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                judet_nume = row['Judet'].strip()
                localitate_nume = row['Nume'].strip()
                uat_nume = row['UAT'].strip()

                # Caută sau creează județul
                judet, _ = Judet.objects.get_or_create(nume=judet_nume)

                # Caută sau creează localitatea
                localitate, _ = Localitate.objects.get_or_create(
                    nume=localitate_nume,
                    judet=judet
                )

                # Verifică dacă UAT-ul există deja
                try:
                    uat = UAT.objects.get(
                        nume=uat_nume,
                        judet=judet,
                        localitate=localitate
                    )
                    uat_existente += 1
                    self.stdout.write(
                        f"UAT-ul {uat_nume}, {localitate_nume}, {judet_nume} există deja")
                except UAT.DoesNotExist:
                    # Creează UAT-ul doar dacă nu există
                    uat = UAT.objects.create(
                        nume=uat_nume,
                        judet=judet,
                        localitate=localitate
                    )
                    uat_adaugate += 1
                    self.stdout.write(
                        f"Adăugat UAT-ul {uat_nume}, {localitate_nume}, {judet_nume}")

        self.stdout.write(
            self.style.SUCCESS(
                f'Import UAT finalizat! '
                f'Adăugate: {uat_adaugate}, '
                f'Existente deja: {uat_existente}'
            )
        )
