from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult

import tempfile
import os

import StudiiFezabilitate.Avize.functii as x
import StudiiFezabilitate.Avize.Common.functii as common
import StudiiFezabilitate.Avize.Bacau.functii as bacau


def aviz_RAJA(lucrare_id, id_aviz):
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

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/01. Aviz RAJA/01. Cerere RAJA.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/01. Aviz RAJA/Citeste-ma.docx"

        # 1. Verificare câmpuri necesare
        errors = bacau.verifica_campuri_necesare_RAJA(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:            # 2. Generare cerere
            cerere_pdf_path = bacau.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)
            fisiere_generate.append(cerere_pdf_path)

            # 3. Copie Certificatul de înregistrare firma de proiectare
            if firma.cale_certificat and hasattr(firma.cale_certificat, 'path'):
                certificat_inregistrare_path = x.copy_file(firma.cale_certificat.path, temp_dir,
                                                           f"02. Certificat {firma.nume}")
                temp_files.append(certificat_inregistrare_path)
                fisiere_generate.append(certificat_inregistrare_path)

            # 4. Plan de situatie la scara in format .pdf
            if cu.cale_plan_situatie_la_scara and hasattr(cu.cale_plan_situatie_la_scara, 'path'):
                plan_situatie_la_scara_path = x.copy_file(cu.cale_plan_situatie_la_scara.path, temp_dir,
                                                          "07. Plan de situatie - la scara")
                temp_files.append(plan_situatie_la_scara_path)
                fisiere_generate.append(plan_situatie_la_scara_path)

            # 5. Copie Certificatul de urbanism
            cu_path = x.copy_file(cu.cale_CU.path, temp_dir,
                                  "08. Certificat de urbanism")
            temp_files.append(cu_path)
            fisiere_generate.append(cu_path)

            # 6. Copie Memoriul tehnic
            memoriu_tehnic_path = x.copy_file(
                cu.cale_memoriu_tehnic_CU.path, temp_dir, "09. Memoriu tehnic")
            temp_files.append(memoriu_tehnic_path)
            fisiere_generate.append(memoriu_tehnic_path)

            # 7. Copie Plan de situație CU
            plan_situatie_path = x.copy_file(
                cu.cale_plan_situatie_CU.path, temp_dir, "10. Plan de situație CU")
            temp_files.append(plan_situatie_path)
            fisiere_generate.append(plan_situatie_path)

            # 8. Copie Plan incadrare CU
            plan_path = x.copy_file(
                cu.cale_plan_incadrare_CU.path, temp_dir, "11. Plan incadrare CU")
            temp_files.append(plan_path)
            fisiere_generate.append(plan_path)

            # 7. Copie Acte facturare
            acte_facturare_path = x.copy_file(
                cu.cale_acte_facturare.path, temp_dir, "06. Acte facturare")
            temp_files.append(acte_facturare_path)
            fisiere_generate.append(acte_facturare_path)

            # 5. Generare Readme
            readme_pdf_path = bacau.genereaza_readme(temp_dir, model_detalii)
            temp_files.append(readme_pdf_path)
            fisiere_generate.append(readme_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            common.curata_fisierele_temporare(
                temp_files, path_document_final, fisiere_generate)
            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în aviz_Orange: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Romprest(lucrare_id, id_aviz):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Fisierul 'Model email' contine informatii cu privire la adresa de email și continutul mesajului din email
    """
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/02. Aviz Romprest/Cerere Romprest.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/02. Aviz Romprest/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = bacau.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = bacau.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = bacau.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = bacau.genereaza_email(
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
        print(f"Eroare în aviz_Romprest: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def acord_Birou_Tehnic_Onesti(lucrare_id, id_aviz):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Fisierul 'Model email' contine informatii cu privire la adresa de email și continutul mesajului din email
    """
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/03. Acord Birou Tehnic Onesti/Cerere Acord Birou Tehnic Onesti.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/03. Acord Birou Tehnic Onesti/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = bacau.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = bacau.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = bacau.genereaza_document_final_cu_CI(
                avizCU, cerere_pdf_path, cu, beneficiar, reprezentant, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = bacau.genereaza_email(
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
        print(f"Eroare în acord_Birou_Tehnic_Onesti: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def acord_administrator_drum(lucrare_id, id_aviz):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Fisierul 'Model email' contine informatii cu privire la adresa de email și continutul mesajului din email
    """
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/04. Acord Administrator Drum/Cerere Acord - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/04. Acord Administrator Drum/Cerere Acord - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/04. Acord Administrator Drum/Cerere Acord - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/04. Acord Administrator Drum/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = bacau.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = bacau.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = bacau.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = bacau.genereaza_email(
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
        print(f"Eroare în acord_administrator_drum: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Apa_CRAB(lucrare_id, id_aviz):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Fisierul 'Model email' contine informatii cu privire la adresa de email și continutul mesajului din email
    """
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/05. Aviz CRAB/Cerere CRAB.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/05. Aviz CRAB/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = bacau.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = bacau.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = bacau.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = bacau.genereaza_email(
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
        print(f"Eroare în aviz_Apa_CRAB: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Chimcomplex(lucrare_id, id_aviz):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Fisierul 'Model email' contine informatii cu privire la adresa de email și continutul mesajului din email
    """
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/06. Aviz CHIMCOMPLEX/Cerere CHIMCOMPLEX - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/06. Aviz CHIMCOMPLEX/Cerere CHIMCOMPLEX - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/06. Aviz CHIMCOMPLEX/Cerere CHIMCOMPLEX - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/06. Aviz CHIMCOMPLEX/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = bacau.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = bacau.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = bacau.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = bacau.genereaza_email(
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
        print(f"Eroare în aviz_CHIMCOMPLEX: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Drumuri_Judetene_Bacau(lucrare_id, id_aviz):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Fisierul 'Model email' contine informatii cu privire la adresa de email și continutul mesajului din email
    """
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/07. Aviz Drumuri Judetene Bacau/Cerere Aviz drumuri judetene Bacau.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/03. bacau/07. Aviz Drumuri Judetene Bacau/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = bacau.verifica_campuri_necesare_extra(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = bacau.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = bacau.genereaza_document_final_cu_CI(
                avizCU, cerere_pdf_path, cu, beneficiar, reprezentant, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = bacau.genereaza_email(
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
        print(f"Eroare în aviz_Drumuri_Judetene_Bacau: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")
