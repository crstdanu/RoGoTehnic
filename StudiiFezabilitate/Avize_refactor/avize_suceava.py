from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult

import tempfile
import os

from .core import functii_baza as baza
from .core import functii_simple as simple


def aviz_APM_Suceava(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul APM din Suceava.
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/01. Aviz APM - Suceava/Cerere_APM_Suceava.docx"
        model_notificare = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/01. Aviz APM - Suceava/Notificare_APM_Suceava.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/01. Aviz APM - Suceava/Model_email_APM_Suceava.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_STANDARD(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_APM(cu, firma, reprezentant, beneficiar)
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
                lucrare, avizCU, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir)
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
        print(f"Eroare neașteptată în {avizCU.nume_aviz.nume}: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_EE_Delgaz_Suceava(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul EE DELGAZ.
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/02. Aviz EE Delgaz - Suceava/Cerere EE Delgaz - Suceava.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/02. Aviz EE Delgaz - Suceava/Model email - EE Delgaz - Suceava.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_STANDARD(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_STANDARD(
            cu, firma, reprezentant, beneficiar)
        if result is not None and not result.is_success():
            return result

        # 1.3 Verificare existența modelelor
        result = simple.verifica_existenta_modele(
            model_cerere, model_detalii, model_notificare=None)
        if result is not None and not result.is_success():
            return result

        temp_dir = tempfile.gettempdir()
        # -------------------------------                                     --- 2. Generare Documente --- #
        try:
            # --- 2. Generare Cerere --- #
            cerere_pdf_path = simple.genereaza_cerere_STANDARD(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # --- 4. Generare Document Final --- #
            path_document_final = simple.genereaza_document_final_STANDARD(
                lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
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
        print(f"Eroare neașteptată în {avizCU.nume_aviz.nume}: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_GN_Delgaz_Suceava(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul GN DELGAZ.
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/03. Aviz GN Delgaz - Suceava/Cerere GN Delgaz - Suceava.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/03. Aviz GN Delgaz - Suceava/Model email - GN Delgaz Suceava.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_STANDARD(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_STANDARD(
            cu, firma, reprezentant, beneficiar)
        if result is not None and not result.is_success():
            return result

        # 1.3 Verificare existența modelelor
        result = simple.verifica_existenta_modele(
            model_cerere, model_detalii, model_notificare=None)
        if result is not None and not result.is_success():
            return result

        temp_dir = tempfile.gettempdir()
        # -------------------------------                                     --- 2. Generare Documente --- #
        try:
            # --- 2. Generare Cerere --- #
            cerere_pdf_path = simple.genereaza_cerere_STANDARD(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # --- 4. Generare Document Final --- #
            path_document_final = simple.genereaza_document_final_STANDARD(
                lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
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
        print(f"Eroare neașteptată în {avizCU.nume_aviz.nume}: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Orange_Suceava(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul Orange.
    Documentația se depune pe portalul Orange.
    Fisierele se depun separat, nu într-un singur fișier PDF. 
    Se depune: Cererea gnerată, Certificatul de urbanism, Planul de incadrare, Planul de situație, Memoriul tehnic și Actele de facturare.
    Fisierul README contine informatii cu privire la pasii de urmat pentru depunerea documentației pe portalul Orange."""
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/04. Aviz Orange - Suceava/01. Cerere Orange - Suceava.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/04. Aviz Orange - Suceava/Citeste-ma.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_FARA_EMAIL(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_STANDARD(
            cu, firma, reprezentant, beneficiar)
        if result is not None and not result.is_success():
            return result

        # 1.3 Verificare existența modelelor
        result = simple.verifica_existenta_modele(
            model_cerere, model_detalii, model_notificare=None)
        if result is not None and not result.is_success():
            return result

        temp_dir = tempfile.gettempdir()
        # -------------------------------                                     --- 2. Generare Documente --- #
        try:
            # --- 2.1 Generare Cerere --- #
            cerere_pdf_path = simple.genereaza_cerere_STANDARD(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)
            fisiere_generate.append(cerere_pdf_path)

            # 2.2 Copie Certificatul de urbanism
            cu_path = baza.copy_file(
                cu.cale_CU.path, temp_dir, "02. Certificat de urbanism")
            temp_files.append(cu_path)
            fisiere_generate.append(cu_path)

            # 2.3. Copie Plan incadrare CU
            plan_path = baza.copy_file(
                cu.cale_plan_incadrare_CU.path, temp_dir, "03. Plan incadrare CU")
            temp_files.append(plan_path)
            fisiere_generate.append(plan_path)

            # 2.4 Copie Plan de situație CU
            plan_situatie_path = baza.copy_file(
                cu.cale_plan_situatie_CU.path, temp_dir, "04. Plan de situație CU")
            temp_files.append(plan_situatie_path)
            fisiere_generate.append(plan_situatie_path)

            # 2.5. Copie Memoriul tehnic
            memoriu_tehnic_path = baza.copy_file(
                cu.cale_memoriu_tehnic_CU.path, temp_dir, "05. Memoriu tehnic")
            temp_files.append(memoriu_tehnic_path)
            fisiere_generate.append(memoriu_tehnic_path)

            # 2.6 Copie Acte facturare
            acte_facturare_path = baza.copy_file(
                cu.cale_acte_facturare.path, temp_dir, "06. Acte facturare")
            temp_files.append(acte_facturare_path)
            fisiere_generate.append(acte_facturare_path)

            # 2.7. Generare Readme
            readme_pdf_path = simple.genereaza_readme(model_detalii, temp_dir)
            temp_files.append(readme_pdf_path)
            fisiere_generate.append(readme_pdf_path)

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
        print(f"Eroare neașteptată în {avizCU.nume_aviz.nume}: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Cultura_Suceava(lucrare_id: int, id_aviz: int):
    pass


def aviz_HCL_Suceava(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul EE DELGAZ.
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

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. suceava/06. Aviz HCL - Suceava/Cerere HCL - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. suceava/06. Aviz HCL - Suceava/Cerere HCL - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. suceava/06. Aviz HCL - Suceava/Cerere HCL - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. suceava/06. Aviz HCL - Suceava/Citeste-ma.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_FARA_EMAIL(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_STANDARD(
            cu, firma, reprezentant, beneficiar)
        if result is not None and not result.is_success():
            return result

        # 1.3 Verificare existența modelelor
        result = simple.verifica_existenta_modele(
            model_cerere, model_detalii, model_notificare=None)
        if result is not None and not result.is_success():
            return result

        temp_dir = tempfile.gettempdir()
        # -------------------------------                                     --- 2. Generare Documente --- #
        try:
            # --- 2. Generare Cerere --- #
            cerere_pdf_path = simple.genereaza_cerere_STANDARD(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # --- 4. Generare Document Final --- #
            path_document_final = simple.genereaza_document_final_STANDARD(
                lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # --- 5. Generare Email --- #
            email_pdf_path = simple.genereaza_readme(model_detalii, temp_dir)
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
        print(f"Eroare neașteptată în {avizCU.nume_aviz.nume}: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_ACET(lucrare_id: int, id_aviz: int):
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

        temp_files = []
        fisiere_generate = []
        path_document_final = None

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/07. Aviz ACET/Cerere ACET.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/07. Aviz ACET/Model email.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_FARA_EMAIL(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_STANDARD(
            cu, firma, reprezentant, beneficiar)
        if result is not None and not result.is_success():
            return result

        # 1.3 Verificare existența modelelor
        result = simple.verifica_existenta_modele(
            model_cerere, model_detalii, model_notificare=None)
        if result is not None and not result.is_success():
            return result

        temp_dir = tempfile.gettempdir()
        # -------------------------------                                     --- 2. Generare Documente --- #
        try:
            # --- 2. Generare Cerere --- #
            cerere_pdf_path = simple.genereaza_cerere_STANDARD(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # --- 4. Generare Document Final --- #
            path_document_final = simple.genereaza_document_final_STANDARD(
                lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
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
        print(f"Eroare neașteptată în {avizCU.nume_aviz.nume}: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_GN_NeoGas(lucrare_id: int, id_aviz: int):
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

        temp_files = []
        fisiere_generate = []
        path_document_final = None

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/08. Aviz NeoGas/Cerere NeoGas.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/08. Aviz NeoGas/Model email.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_FARA_EMAIL(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_STANDARD(
            cu, firma, reprezentant, beneficiar)
        if result is not None and not result.is_success():
            return result

        # 1.3 Verificare existența modelelor
        result = simple.verifica_existenta_modele(
            model_cerere, model_detalii, model_notificare=None)
        if result is not None and not result.is_success():
            return result

        temp_dir = tempfile.gettempdir()
        # -------------------------------                                     --- 2. Generare Documente --- #
        try:
            # --- 2. Generare Cerere --- #
            cerere_pdf_path = simple.genereaza_cerere_STANDARD(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # --- 4. Generare Document Final --- #
            path_document_final = simple.genereaza_document_final_STANDARD(
                lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
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
        print(f"Eroare neașteptată în {avizCU.nume_aviz.nume}: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_DIGI_Suceava(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul Digi.
    Documentația se depune pe portalul Digi.
    Fisierele se depun separat, nu într-un singur fișier PDF. 
    Se depune: Acte facturare, Acte beneficiar, Certificatul de urbanism, și Memoriul tehnic.
    Fisierul README contine informatii cu privire la pasii de urmat pentru depunerea documentației pe portalul Digi."""
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/09. Aviz DIGI - Suceava/Citeste-ma.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/05. suceava/09. Aviz DIGI - Suceava/Citeste-ma.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_FARA_EMAIL(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_ACTE_BENEFICIAR(
            cu, firma, reprezentant, beneficiar)
        if result is not None and not result.is_success():
            return result

        # 1.3 Verificare existența modelelor
        result = simple.verifica_existenta_modele(
            model_cerere, model_detalii, model_notificare=None)
        if result is not None and not result.is_success():
            return result

        temp_dir = tempfile.gettempdir()
        # -------------------------------                                     --- 2. Generare Documente --- #
        try:

            # 2.1 Copie Acte facturare
            acte_facturare_path = baza.copy_file(
                cu.cale_acte_facturare.path, temp_dir, "02. Acte facturare")
            temp_files.append(acte_facturare_path)
            fisiere_generate.append(acte_facturare_path)

            # 2.2 Copie Acte beneficiar
            acte_beneficiar_path = baza.copy_file(
                cu.cale_acte_beneficiar.path, temp_dir, "03. Imputernicire")
            temp_files.append(acte_beneficiar_path)
            fisiere_generate.append(acte_beneficiar_path)

            # 2.3 Copie Certificatul de urbanism
            cu_path = baza.copy_file(
                cu.cale_CU.path, temp_dir, "04. Certificat de urbanism")
            temp_files.append(cu_path)
            fisiere_generate.append(cu_path)
        
            # 2.4 Copie Memoriul tehnic
            memoriu_tehnic_path = baza.copy_file(
                cu.cale_memoriu_tehnic_CU.path, temp_dir, "05. Memoriu tehnic")
            temp_files.append(memoriu_tehnic_path)
            fisiere_generate.append(memoriu_tehnic_path)


            # 2.5 Copie Plan de incadrare CU
            plan_incadrare_path = baza.copy_file(
                cu.cale_plan_incadrare_CU.path, temp_dir, "06. Plan de incadrare CU")
            temp_files.append(plan_incadrare_path)
            fisiere_generate.append(plan_incadrare_path)

            # 2.6 Copie Plan de situație CU
            plan_situatie_path = baza.copy_file(
                cu.cale_plan_situatie_CU.path, temp_dir, "07. Plan de situație CU")
            temp_files.append(plan_situatie_path)
            fisiere_generate.append(plan_situatie_path)


            # 2.7. Generare Readme
            readme_pdf_path = simple.genereaza_readme_DIGI(lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact, model_detalii, temp_dir)
            temp_files.append(readme_pdf_path)
            fisiere_generate.append(readme_pdf_path)

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
        print(f"Eroare neașteptată în {avizCU.nume_aviz.nume}: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")