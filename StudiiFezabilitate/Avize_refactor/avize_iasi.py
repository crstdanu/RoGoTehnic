from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult

import tempfile
import os

from .core import functii_baza as baza
from .core import functii_simple as simple


def aviz_APM_Iasi(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul APM din Iasi.
    Documentatia se depune pe email in format PDF, un singur fișier.
    Pentru Bacau, documentatia se depune in fizic, adica printata si expediata prin posta."""
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

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/00. Common/01. APM/Cerere_APM.docx"
        model_notificare = "StudiiFezabilitate/Avize/modele_cereri/00. Common/01. APM/Notificare.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/00. Common/01. APM/Model email.docx"

        # --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_APM(
            lucrare, firma, reprezentant, cu, beneficiar, contact)
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


# def aviz_APM(lucrare_id, id_aviz):
#     """
#     Aceasta functie genereaza documentatia necesara pentru avizul APM din 6 judete diferite.
#     Pentru toate judetele, cu exceptia judetului Bacau, documentatia se depune pe email in format PDF, un singur fișier.
#     Pentru Bacau, documentatia se depune in fizic, adica printata si expediata prin posta."""

#     try:
#         lucrare = Lucrare.objects.get(pk=lucrare_id)
#         avizCU = AvizeCU.objects.get(pk=id_aviz)
#         cu = avizCU.certificat_urbanism
#         firma = lucrare.firma_proiectare
#         reprezentant = firma.reprezentant
#         beneficiar = lucrare.beneficiar
#         contact = lucrare.persoana_contact

#         # Lista pentru a ține evidența fișierelor generate temporar și finale
#         temp_files = []
#         fisiere_generate = []
#         path_document_final = None

#         model_cerere = "StudiiFezabilitate/Avize/modele_cereri/00. Common/01. APM/Cerere_APM.docx"
#         model_notificare = "StudiiFezabilitate/Avize/modele_cereri/00. Common/01. APM/Notificare.docx"
#         if lucrare.judet.nume == "Bacău":
#             model_detalii = "StudiiFezabilitate/Avize/modele_cereri/00. Common/01. APM/Readme_bacau.docx"
#         else:
#             model_detalii = "StudiiFezabilitate/Avize/modele_cereri/00. Common/01. APM/Model email.docx"

#         # 1. Verificare câmpuri necesare
#         errors = utils.verifica_campuri_necesare(
#             lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
#         # Check if errors is a DocumentGenerationResult and if it's an error result
#         if errors is not None and not errors.is_success():
#             return errors

#         # Verificăm existența tuturor modelelor de documente simultan
#         for model_path, descriere in [
#             (model_cerere, "Cerere Aviz APM"),
#             (model_detalii, "Model email"),
#             (model_notificare, "Notificare APM")
#         ]:
#             if not os.path.exists(model_path):
#                 return DocumentGenerationResult.error_result(
#                     f"Nu găsesc modelul pentru {descriere}: {model_path}")

#         temp_dir = tempfile.gettempdir()

#         try:
#             # 2. Generare cerere
#             cerere_pdf_path = utils.genereaza_cerere(
#                 lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
#             temp_files.append(cerere_pdf_path)

#             # 3. Generare notificare
#             notificare_pdf_path = utils.genereaza_notificare_APM(
#                 lucrare, firma, reprezentant, cu, beneficiar, contact, model_notificare, temp_dir)
#             temp_files.append(notificare_pdf_path)

#             if lucrare.judet.nume == "Bacău":
#                 # 4. Generare document final
#                 path_document_final = common.genereaza_document_final_APM_print(
#                     lucrare, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir)
#                 fisiere_generate.append(path_document_final)

#                 # 5. Generare email
#                 email_pdf_path = utils.genereaza_readme(
#                     temp_dir, model_detalii)
#                 fisiere_generate.append(email_pdf_path)
#             else:
#                 # 4. Generare document final
#                 path_document_final = common.genereaza_document_final_APM(
#                     lucrare, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir)
#                 fisiere_generate.append(path_document_final)

#                 # 5. Generare email
#                 email_pdf_path = utils.genereaza_email(
#                     lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact, model_detalii, temp_dir)
#                 fisiere_generate.append(email_pdf_path)

#             # Toate documentele au fost generate cu succes
#             return DocumentGenerationResult.success_result(fisiere_generate)

#         except Exception as e:
#             # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
#             common.curata_fisierele_temporare(
#                 temp_files, path_document_final, fisiere_generate)
#             return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

#     except Lucrare.DoesNotExist:
#         return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

#     except AvizeCU.DoesNotExist:
#         return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

#     except Exception as e:
#         print(f"Eroare în aviz_APM: {e}")
#         return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")
