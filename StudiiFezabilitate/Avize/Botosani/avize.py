from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult

import tempfile
import os

import StudiiFezabilitate.Avize.functii as x
import StudiiFezabilitate.Avize.Common.functii as common
import StudiiFezabilitate.Avize.Botosani.functii as botosani


def aviz_ApaServ(lucrare_id, id_aviz):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Fisierul 'Model email' contine informatii cu privire la adresa de email și continutul mesajului din email
    La aceasta documentatie se adauga si CI-ul reprezentantului firmei de proiectare
    """
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/04. botosani/01. Aviz ApaServ/Cerere Nova Apaserv.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/04. botosani/01. Aviz ApaServ/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = botosani.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = botosani.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = botosani.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = botosani.genereaza_email(
                lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact, model_detalii, temp_dir)
            fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            common.curata_fisierele_temporare(
                temp_files, fisiere_generate)
            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în aviz_Apaserv: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")
