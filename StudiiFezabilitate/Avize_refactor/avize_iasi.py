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


def aviz_EE_Delgaz_Iasi(lucrare_id: int, id_aviz: int):
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/02. Aviz EE Delgaz - Iasi/Cerere EE Delgaz - Iasi.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/02. Aviz EE Delgaz - Iasi/Model email - EE Delgaz - Iasi.docx"

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


def aviz_GN_Delgaz_Iasi(lucrare_id: int, id_aviz: int):
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/03. Aviz GN Delgaz - Iasi/Cerere GN Delgaz - Iasi.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/03. Aviz GN Delgaz - Iasi/Model email - GN Delgaz Iasi.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_STANDARD(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_STANDARD_cu_DWG(
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

            # --- 6. Generare DWG-ul --- #
            plan_situatie_DWG_path = simple.genereaza_plan_situatie_DWG(
                lucrare, avizCU, cu, temp_dir)
            fisiere_generate.append(plan_situatie_DWG_path)

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


def aviz_Orange_Iasi(lucrare_id: int, id_aviz: int):
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/04. Aviz Orange - Iasi/01. Cerere Orange - Iasi.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/04. Aviz Orange - Iasi/Citeste-ma.docx"

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


def aviz_Cultura_Iasi(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul Directiei de Cultura.
    Documentatia se depune pe email in format PDF, un singur fișier. precum și fizic: se trimite documentatia printata, prin posta"""
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/05. Aviz Cultura - Iasi/Cerere Cultura - Iasi.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/05. Aviz Cultura - Iasi/Model email - Iasi.docx"

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
            cerere_pdf_path = simple.genereaza_cerere_CULTURA(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # --- 4. Generare Document Final --- #
            path_document_final = simple.genereaza_document_final_STANDARD(
                lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # --- 4. Generare Document Final --- #
            path_document_final_print = simple.genereaza_document_final_STANDARD(
                lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir, print=True)
            fisiere_generate.append(path_document_final_print)

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


def aviz_HCL_Iasi(lucrare_id: int, id_aviz: int):
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
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/06. Aviz HCL - Iasi/Cerere HCL - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/06. Aviz HCL - Iasi/Cerere HCL - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/06. Aviz HCL - Iasi/Cerere HCL - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/06. Aviz HCL - Iasi/Citeste-ma.docx"

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


def aviz_principiu_Politia_Rutiera(lucrare_id, id_aviz):
    pass


def studiu_Geotehnic_Polsa(lucrare_id, id_aviz):
    pass


def aviz_MAI(lucrare_id, id_aviz):
    pass


def aviz_CFR(lucrare_id, id_aviz):
    pass


def aviz_ISU(lucrare_id, id_aviz):
    pass


def punct_de_vedere_ISU(lucrare_id, id_aviz):
    pass


def aviz_DSP(lucrare_id, id_aviz):
    pass


def punct_de_vedere_DSP(lucrare_id, id_aviz):
    pass


def punct_de_vedere_OAR(lucrare_id, id_aviz):
    pass


def aviz_Apavital(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul Apavital.
    Documentatia se depune pe platforma Apavital si contine fisierele separate."""
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/07. Aviz Apavital/01. Cerere Apavital.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/07. Aviz Apavital/Citeste-ma.docx"

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
            fisiere_generate.append(cerere_pdf_path)

            # Aici copiem documentele necesaare pentru avizul Apavital

            documente_de_copiat = [
                (cu.cale_CU.path, "02. Certificat de urbanism"),
                (cu.cale_plan_incadrare_CU.path, "03. Plan incadrare CU"),
                (cu.cale_plan_situatie_CU.path, "04. Plan de situație CU"),
                (cu.cale_memoriu_tehnic_CU.path, "05. Memoriu tehnic"),
                (cu.cale_acte_facturare.path, "06. Acte facturare")
            ]

            # Parcurgem lista și copiem fiecare document
            for sursa, nume_destinatie in documente_de_copiat:
                document_path = baza.copy_file(
                    sursa, temp_dir, nume_destinatie)
                temp_files.append(document_path)
                fisiere_generate.append(document_path)

            # --- 5. Generare README --- #
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


def aviz_GN_Gazmir(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul GN Gazmir.
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/08. Aviz GN Gazmir/Cerere Gazmir.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/08. Aviz GN Gazmir/Model email.docx"

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
            cerere_pdf_path = simple.genereaza_cerere_minimala(
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


def aviz_Termoficare(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul Termoficare.
    Documentatia se depune fizic"""
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/09. Aviz Termoficare/Cerere Termoficare.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/09. Aviz Termoficare/Citeste-ma.docx"

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
                lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir, print=True)
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


def aviz_CTP(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul CTP.
    Documentatia se depune fizic la sediul CTP"""
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/10. Aviz CTP/Cerere CTP.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/10. Aviz CTP/Citeste-ma.docx"

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
                lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir, print=True)
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


def aviz_Salubris(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul Salubris.
    Documentatia se depune fizic.
    Diferenta fata de restul avizelor este ca la cerere se adauga doar Certificatul de urbanism, nimic altceva"""
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/11. Aviz Salubris/Cerere Salubris.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/11. Aviz Salubris/Citeste-ma.docx"

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
            path_document_final = simple.genereaza_document_final_Salubris(
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


def aviz_PMI_Mediu(lucrare_id: int, id_aviz: int):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Spre deosebire de celelalte functii de generare a documentatiei pentru avize, aceasta mai adauga un Plan Mediu PMI, la fel ca la APM
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/12. Aviz PMI-Mediu/Cerere Aviz Mediu PMI.docx"
        model_notificare = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/12. Aviz PMI-Mediu/Plan Mediu PMI.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/12. Aviz PMI-Mediu/Model email.docx"

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
            notificare_pdf_path = simple.genereaza_cerere_STANDARD(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_notificare, temp_dir)
            temp_files.append(notificare_pdf_path)

            # --- 4. Generare Document Final --- #
            path_document_final = simple.genereaza_document_final_PMI_MEDIU(
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


def aviz_PMI_BSM(lucrare_id: int, id_aviz: int):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Fisierul 'Model email' contine informatii cu privire la adresa de email și continutul mesajului din email
    Spre deosebire de celelelte functii de generare a documentatiei pentru avize, modelul de cerere pentru acest aviz difera in functie de firma de proiectare
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

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/13. Aviz PMI - BSM/Model aviz PMI BSM - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/13. Aviz PMI - BSM/Model aviz PMI BSM - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/13. Aviz PMI - BSM/Model aviz PMI BSM - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/13. Aviz PMI - BSM/Model email.docx"

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
            cerere_pdf_path = simple.genereaza_cerere_minimala(
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


def aviz_PMI_SUP(lucrare_id: int, id_aviz: int):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Fisierul 'Model email' contine informatii cu privire la adresa de email și continutul mesajului din email
    Spre deosebire de celelelte functii de generare a documentatiei pentru avize, modelul de cerere pentru acest aviz difera in functie de firma de proiectare
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

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/14. Aviz PMI - SUP/Model aviz PMI SUP - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/14. Aviz PMI - SUP/Model aviz PMI SUP - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/14. Aviz PMI - SUP/Model aviz PMI SUP - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/14. Aviz PMI - SUP/Model email.docx"

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
            cerere_pdf_path = simple.genereaza_cerere_minimala(
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


def aviz_PMI_Spatii_Verzi(lucrare_id: int, id_aviz: int):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Fisierul 'Model email' contine informatii cu privire la adresa de email și continutul mesajului din email
    Spre deosebire de celelelte functii de generare a documentatiei pentru avize, modelul de cerere pentru acest aviz difera in functie de firma de proiectare
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

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/15. Aviz PMI - Spatii verzi/Model aviz PMI Spatii Verzi - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/15. Aviz PMI - Spatii verzi/Model aviz PMI Spatii Verzi - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/15. Aviz PMI - Spatii verzi/Model aviz PMI Spatii Verzi - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/15. Aviz PMI - Spatii verzi/Model email.docx"

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
            cerere_pdf_path = simple.genereaza_cerere_minimala(
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


def aviz_PMI_Trafic_Urban(lucrare_id: int, id_aviz: int):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Fisierul 'Model email' contine informatii cu privire la adresa de email și continutul mesajului din email
    Spre deosebire de celelelte functii de generare a documentatiei pentru avize, modelul de cerere pentru acest aviz difera in functie de firma de proiectare
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

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/16. Aviz PMI - Trafic urban/Model aviz PMI - Trafic urban - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/16. Aviz PMI - Trafic urban/Model aviz PMI - Trafic urban - GENERAL TEHNIC.docxx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/16. Aviz PMI - Trafic urban/Model aviz PMI - Trafic urban - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/16. Aviz PMI - Trafic urban/Model email.docx"

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
            cerere_pdf_path = simple.genereaza_cerere_minimala(
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


def aviz_PMI_GIS(lucrare_id: int, id_aviz: int):
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/17. Aviz PMI - GiS Cadastru/Cerere Aviz GiS.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/17. Aviz PMI - GiS Cadastru/Model email.docx"

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


def aviz_PMI_Nomenclatura_urbana(lucrare_id: int, id_aviz: int):
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/18. Aviz PMI - Nomenclatura urbana/Cerere PMI - Nomenclatura urbana.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/18. Aviz PMI - Nomenclatura urbana/Model email.docx"

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


def aviz_PMI_Evidenta_Patrimoniiu(lucrare_id: int, id_aviz: int):
    """
    Avizul Evidență patrimoniu se depune fizic la adresa institutiei astfel ca documentatia va trebui printata. 
    De aceea folosesc o functie care introduce pagini goale precum si documente in doua exemplare acolo unde e cazul.
    Fisierul 'Citeste-ma' contine informatii cu privire la adresa de depunere a documentatiei si programul de lucru al institutiei.
    Spre deosebire de celelelte functii de generare a documentatiei pentru avize, modelul de cerere pentru acest aviz difera in functie de firma de proiectare
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
        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/19. Aviz Evidenta patrimoniu/Cerere Evidenta Patrimoniu - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/19. Aviz Evidenta patrimoniu/Cerere Evidenta Patrimoniu - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/19. Aviz Evidenta patrimoniu/Cerere Evidenta Patrimoniu - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/19. Aviz Evidenta patrimoniu/Citeste-ma.docx"

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
                lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir, print=True)
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


def aviz_DIGI_Iasi(lucrare_id: int, id_aviz: int):
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/20. Aviz DIGI - Iasi/Citeste-ma.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/20. Aviz DIGI - Iasi/Citeste-ma.docx"

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


def aviz_MApN_Iasi(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul MApN Iasi.
    Documentatia se depune prin poștă astfel ca documentatia va trebui printata."""
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/21. Aviz MApN - Iasi/Cerere MApN.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/21. Aviz MApN - Iasi/Citeste-ma.docx"

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
                lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir, print=True)
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


def aviz_TransElectrica_Iasi(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul TransElectrica.
    Documentatia se depune fizic, prin posta
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/23 . Aviz TransElectrica - Iasi/Cerere Transelectrica.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/23 . Aviz TransElectrica - Iasi/Citeste-ma.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_FARA_EMAIL(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_COMPLET(
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
            cerere_pdf_path = simple.genereaza_cerere_cu_CI(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # --- 4. Generare Document Final --- #
            path_document_final = simple.genereaza_document_final_COMPLET(
                lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir, print=True)
            fisiere_generate.append(path_document_final)

            # --- 5. Generare Email --- #
            email_pdf_path = simple.genereaza_readme(model_detalii, temp_dir)
            fisiere_generate.append(email_pdf_path)

            # --- 6. Generare DWG-ul --- #
            plan_situatie_DWG_path = simple.genereaza_plan_situatie_DWG(
                lucrare, avizCU, cu, temp_dir)
            fisiere_generate.append(plan_situatie_DWG_path)

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


def aviz_TransGaz_Iasi(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul TransGaz.
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/22. Aviz TransGaz - Iasi/Cerere TransGaz.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/22. Aviz TransGaz - Iasi/Model email.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_STANDARD(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_STANDARD_cu_DWG(
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

            # --- 6. Generare DWG-ul --- #
            plan_situatie_DWG_path = simple.genereaza_plan_situatie_DWG(
                lucrare, avizCU, cu, temp_dir)
            fisiere_generate.append(plan_situatie_DWG_path)

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


def aviz_ANIF_Iasi(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul ANIF Iași.
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/24. Aviz ANIF - Iasi/Cerere ANIF.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/24. Aviz ANIF - Iasi/Model email - ANIF - Iasi.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_STANDARD(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_COMPLET_fara_DWG(
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
            path_document_final = simple.genereaza_document_final_COMPLET(
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


def studiu_geotehnic_Iasi(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru studiu geotehnic.
    Documentația se trimite pe mail.
    Fisierele se depun separat, nu într-un singur fișier PDF. """
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/25. Studiu geotehnic/Model email.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. iasi/25. Studiu geotehnic/Model email.docx"

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

            # 2.1 Copie Certificatul de urbanism
            cu_path = baza.copy_file(
                cu.cale_CU.path, temp_dir, "02. Certificat de urbanism")
            temp_files.append(cu_path)
            fisiere_generate.append(cu_path)

            # 2.2 Copie Plan incadrare CU
            plan_path = baza.copy_file(
                cu.cale_plan_incadrare_CU.path, temp_dir, "03. Plan incadrare CU")
            temp_files.append(plan_path)
            fisiere_generate.append(plan_path)

            # 2.3 Copie Plan de situație CU
            plan_situatie_path = baza.copy_file(
                cu.cale_plan_situatie_CU.path, temp_dir, "04. Plan de situație CU")
            temp_files.append(plan_situatie_path)
            fisiere_generate.append(plan_situatie_path)

            # 2.4 Copie Memoriul tehnic
            memoriu_tehnic_path = baza.copy_file(
                cu.cale_memoriu_tehnic_CU.path, temp_dir, "05. Memoriu tehnic")
            temp_files.append(memoriu_tehnic_path)
            fisiere_generate.append(memoriu_tehnic_path)

            # 2.5 Copie Acte facturare
            acte_facturare_path = baza.copy_file(
                cu.cale_acte_facturare.path, temp_dir, "06. Acte facturare")
            temp_files.append(acte_facturare_path)
            fisiere_generate.append(acte_facturare_path)

            # 2.6 Generare model email
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

