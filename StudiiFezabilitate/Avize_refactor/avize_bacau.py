from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult

import tempfile
import os

from .core import functii_baza as baza
from .core import functii_simple as simple


def aviz_APM_Bacau(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul APM din Bacău.
    Documentatia se depune in fizic, adica printata si expediata prin posta."""
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/03. bacau/01. Aviz APM - Bacau/Cerere_APM_Bacau.docx"
        model_notificare = "StudiiFezabilitate/Avize_refactor/modele_cereri/03. bacau/01. Aviz APM - Bacau/Notificare_APM_Bacau.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/03. bacau/01. Aviz APM - Bacau/Readme_APM_Bacau.docx"

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
                lucrare, avizCU, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir, print=True)
            fisiere_generate.append(path_document_final)

            # --- 5. Generare README --- #
            readme_pdf_path = simple.genereaza_readme(model_detalii, temp_dir)
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


def aviz_EE_Delgaz_Bacau(lucrare_id: int, id_aviz: int):
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/03. bacau/02. Aviz EE Delgaz - Bacau/Cerere EE Delgaz - Bacau.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/03. bacau/02. Aviz EE Delgaz - Bacau/Model email - EE Delgaz - Bacau.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_STANDARD(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_STANDARD(
            cu, firma, reprezentant)
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


def aviz_GN_Delgaz_Bacau(lucrare_id: int, id_aviz: int):
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/03. bacau/03. Aviz GN Delgaz - Bacau/Cerere GN Delgaz - Bacau.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/03. bacau/03. Aviz GN Delgaz - Bacau/Model email - GN Delgaz Bacau.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_STANDARD(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_STANDARD(
            cu, firma, reprezentant)
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


def aviz_Orange_Bacau(lucrare_id: int, id_aviz: int):
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/03. bacau/04. Aviz Orange - Bacau/01. Cerere Orange - Bacau.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/03. bacau/04. Aviz Orange - Bacau/Citeste-ma.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_FARA_EMAIL(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_STANDARD(
            cu, firma, reprezentant)
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


def aviz_Cultura_Bacau(lucrare_id: int, id_aviz: int):
    pass


def aviz_HCL_Bacau(lucrare_id: int, id_aviz: int):
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
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. bacau/06. Aviz HCL - Bacau/Cerere HCL - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. bacau/06. Aviz HCL - Bacau/Cerere HCL - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. bacau/06. Aviz HCL - Bacau/Cerere HCL - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/01. bacau/06. Aviz HCL - Bacau/Citeste-ma.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_FARA_EMAIL(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_STANDARD(
            cu, firma, reprezentant)
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


def aviz_Romprest(lucrare_id: int, id_aviz: int):
    pass


def acord_Birou_Tehnic_Onesti(lucrare_id: int, id_aviz: int):
    pass


def acord_administrator_drum(lucrare_id: int, id_aviz: int):
    pass


def aviz_Apa_CRAB(lucrare_id: int, id_aviz: int):
    pass


def aviz_Chimcomplex(lucrare_id: int, id_aviz: int):
    pass


def aviz_Drumuri_Judetene_Bacau(lucrare_id: int, id_aviz: int):
    pass


def aviz_RAJA(lucrare_id: int, id_aviz: int):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul RAJA.
    Documentația se depune pe portalul RAJA.
    Fisierele se depun separat, nu într-un singur fișier PDF. 
    Se depune: Cererea gnerată, Certificatul de urbanism, Planul de incadrare, Planul de situație, Memoriul tehnic și Actele de facturare.
    Fisierul README contine informatii cu privire la pasii de urmat pentru depunerea documentației pe portalul RAJA."""
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

        model_cerere = "StudiiFezabilitate/Avize_refactor/modele_cereri/03. bacau/07. Aviz RAJA/01. Cerere RAJA.docx"
        model_detalii = "StudiiFezabilitate/Avize_refactor/modele_cereri/03. bacau/07. Aviz RAJA/Citeste-ma.docx"

        # -------------------------------                                     --- 1. Validări --- #
        # 1.1 Verificare câmpuri necesare
        result = simple.verifica_campuri_FARA_EMAIL(
            lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact)
        if result is not None and not result.is_success():
            return result

        # 1.2 Verificare fișiere încărcate
        result = simple.verifica_fisiere_incarcate_CU_PLAN_SITUATIE_PDF(
            cu, firma, reprezentant)
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
            cerere_pdf_path = simple.genereaza_cerere_minimala(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)
            fisiere_generate.append(cerere_pdf_path)

            # 2.2 Copie Certificatul de înregistrare
            acte_facturare_path = baza.copy_file(
                cu.cale_acte_facturare.path, temp_dir, "02. Acte facturare")
            temp_files.append(acte_facturare_path)
            fisiere_generate.append(acte_facturare_path)

            # 2.3 Copie Plan de situație la scara
            plan_situatie_path = baza.copy_file(
                cu.cale_plan_situatie_la_scara.path, temp_dir, "07. Plan de situație la scara")
            temp_files.append(plan_situatie_path)
            fisiere_generate.append(plan_situatie_path)

            # 2.4 Copie Certificatul de urbanism
            cu_path = baza.copy_file(
                cu.cale_CU.path, temp_dir, "08. Certificat de urbanism")
            temp_files.append(cu_path)
            fisiere_generate.append(cu_path)

            # 2.5. Copie Memoriul tehnic
            memoriu_tehnic_path = baza.copy_file(
                cu.cale_memoriu_tehnic_CU.path, temp_dir, "09. Memoriu tehnic")
            temp_files.append(memoriu_tehnic_path)
            fisiere_generate.append(memoriu_tehnic_path)

            # 2.6 Copie Plan de situație CU
            plan_situatie_path = baza.copy_file(
                cu.cale_plan_situatie_CU.path, temp_dir, "10. Plan de situație CU")
            temp_files.append(plan_situatie_path)
            fisiere_generate.append(plan_situatie_path)

            # 2.7. Copie Plan incadrare CU
            plan_path = baza.copy_file(
                cu.cale_plan_incadrare_CU.path, temp_dir, "11. Plan incadrare CU")
            temp_files.append(plan_path)
            fisiere_generate.append(plan_path)

            # 2.8 Copie Memoriul tehnic
            memoriu_tehnic_path = baza.copy_file(
                cu.cale_memoriu_tehnic_CU.path, temp_dir, "12. Memoriu tehnic")
            temp_files.append(memoriu_tehnic_path)
            fisiere_generate.append(memoriu_tehnic_path)

            # 2.9 Generare Readme
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
