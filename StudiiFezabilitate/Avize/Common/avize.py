from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult
import StudiiFezabilitate.Avize.Common.functii as y
import tempfile


def aviz_APM(lucrare_id, id_aviz):
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = y.verifica_campuri_necesare_APM(
            lucrare, firma, reprezentant, cu, beneficiar, contact)
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = y.genereaza_cerere_APM(
                lucrare, firma, reprezentant, beneficiar, contact, cu, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare notificare
            notificare_pdf_path = y.genereaza_notificare_APM(
                lucrare, firma, reprezentant, cu, beneficiar, contact, temp_dir)
            temp_files.append(notificare_pdf_path)

            if lucrare.judet.nume == "Bacău":
                # 4. Generare document final
                path_document_final = y.genereaza_document_final_APM_print(
                    lucrare, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir
                )
                fisiere_generate.append(path_document_final)

                # 5. Generare email
                email_pdf_path = y.genereaza_readme_APM_bacau(temp_dir)
                fisiere_generate.append(email_pdf_path)
            else:
                # 4. Generare document final
                path_document_final = y.genereaza_document_final_APM(
                    lucrare, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir
                )
                fisiere_generate.append(path_document_final)

                # 5. Generare email
                email_pdf_path = y.genereaza_email_APM(
                    lucrare, avizCU, beneficiar, cu, contact, temp_dir)
                fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            y.curata_fisierele_temporare(
                temp_files, path_document_final, fisiere_generate)
            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în aviz_APM: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_EE_Delgaz(lucrare_id, id_aviz):
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = y.verifica_campuri_necesare_EE_Delgaz(
            lucrare, firma, reprezentant, cu, beneficiar, contact)
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = y.genereaza_cerere_EE_Delgaz(
                lucrare, firma, reprezentant, beneficiar, contact, cu, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = y.genereaza_document_final_EE_Delgaz(
                lucrare, cerere_pdf_path, cu, beneficiar, temp_dir
            )
            fisiere_generate.append(path_document_final)

            # 5. Generare email
            email_pdf_path = y.genereaza_email_EE_Delgaz(
                lucrare, beneficiar, cu, contact, temp_dir)
            fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            y.curata_fisierele_temporare(
                temp_files, path_document_final, fisiere_generate)
            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în aviz_EE_delgaz: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")
