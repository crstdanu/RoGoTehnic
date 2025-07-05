from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult

import tempfile
import os

from .core import functii_baza as baza
from .core import functii_simple as simple


def aviz_APM_Iasi(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul APM din Iasi.
    Documentatia se depune pe email in format PDF, un singur fișier."""
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        temp_files = []
        fisiere_generate = []
        path_document_final = None

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/01. Aviz APM - Iasi/Cerere_APM_Iasi.docx"
        model_notificare = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/01. Aviz APM - Iasi/Notificare_APM_Iasi.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/01. Aviz APM - Iasi/Model_email_APM_Iasi.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_STANDARD(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_APM(cu, firma, reprezentant)
        if result is not None and not result.is_success():
            return result

        # 1.3 Verificare existența modelelor
        result = simple.verifica_existenta_modele(
            model_cerere, model_detalii, model_notificare)
        if result is not None and not result.is_success():
            return result

        temp_dir = tempfile.gettempdir()
        # -------------------------------                                     --- 2. Generare Documente --- #
        try:
            # --- 2. Generare Cerere --- #
            cerere_pdf_path = simple.genereaza_cerere_minimala(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # --- 3. Generare Notificare --- #
            notificare_pdf_path = simple.genereaza_notificare_APM(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_notificare, temp_dir)
            temp_files.append(notificare_pdf_path)

            # --- 4. Generare Document Final --- #
            path_document_final = simple.genereaza_document_final_APM(
                lucrare, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # --- 5. Generare Email --- #
            email_pdf_path = simple.genereaza_email(
                lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact, model_detalii, temp_dir)
            fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)
        # -------------------------------------------- -------------------                    --- 3. Tratare erori --- #
        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            baza.curata_fisierele_temporare(
                temp_files, path_document_final, fisiere_generate)
            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        # Prindem orice altă excepție neașteptată (ex: probleme de conectare la DB)
        print(f"Eroare neașteptată în aviz_APM_Iasi: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")
