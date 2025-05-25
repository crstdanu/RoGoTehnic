from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult
import StudiiFezabilitate.Avize.Common.functii as common
import StudiiFezabilitate.Avize.functii as x
import StudiiFezabilitate.Avize.utils as utils
import tempfile
import os


def aviz_APM(lucrare_id, id_aviz):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul APM din 6 judete diferite.
    Pentru toate judetele, cu exceptia judetului Bacau, documentatia se depune pe email in format PDF, un singur fișier.
    Pentru Bacau, documentatia se depune in fizic, adica printata si expediata prin posta."""

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

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/00. Common/01. APM/Cerere_APM.docx"
        model_notificare = "StudiiFezabilitate/Avize/modele_cereri/00. Common/01. APM/Notificare.docx"
        if lucrare.judet.nume == "Bacău":
            model_detalii = "StudiiFezabilitate/Avize/modele_cereri/00. Common/01. APM/Readme_bacau.docx"
        else:
            model_detalii = "StudiiFezabilitate/Avize/modele_cereri/00. Common/01. APM/Model email.docx"

        # 1. Verificare câmpuri necesare
        errors = utils.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        # Verificăm existența tuturor modelelor de documente simultan
        for model_path, descriere in [
            (model_cerere, "Cerere Aviz APM"),
            (model_detalii, "Model email"),
            (model_notificare, "Notificare APM")
        ]:
            if not os.path.exists(model_path):
                return DocumentGenerationResult.error_result(
                    f"Nu găsesc modelul pentru {descriere}: {model_path}")

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = utils.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare notificare
            notificare_pdf_path = utils.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(notificare_pdf_path)

            if lucrare.judet.nume == "Bacău":
                # 4. Generare document final
                path_document_final = common.genereaza_document_final_APM_print(
                    lucrare, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir)
                fisiere_generate.append(path_document_final)

                # 5. Generare email
                email_pdf_path = utils.genereaza_readme(
                    temp_dir, model_detalii)
                fisiere_generate.append(email_pdf_path)
            else:
                # 4. Generare document final
                path_document_final = common.genereaza_document_final_APM(
                    lucrare, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir)
                fisiere_generate.append(path_document_final)

                # 5. Generare email
                email_pdf_path = utils.genereaza_email(
                    lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact, model_detalii, temp_dir)
                fisiere_generate.append(email_pdf_path)

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
        print(f"Eroare în aviz_APM: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_EE_Delgaz(lucrare_id, id_aviz):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul EE Delgaz din 6 judete diferite:
    Iasi, Bacau, Suceava, Botosani, Vaslui si Neamt.
    Modelul de cerere este același pentru toate cele 6 județe.
    Documentația generata este inaiantata pe email in format PDF, un singur fișier.
    Fișierul "Model email" conține informațiile necesare cu privire la conținutul emailului și adresa de email la care trebuie înaintată documentația.
    Adresade email este specifică fiecărui județ în parte, iar modelul de email este același pentru toate cele 6 județe.
    """
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

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/00. Common/02. EE Delgaz/Cerere EE Delgaz.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/00. Common/02. EE Delgaz/Model email - EE Delgaz.docx"

        # 1. Verificare câmpuri necesare
        errors = utils.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = utils.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = utils.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir
            )
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = utils.genereaza_email(
                lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact, model_detalii, temp_dir)
            fisiere_generate.append(email_pdf_path)

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
        print(f"Eroare în aviz_EE_delgaz: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_GN_Delgaz(lucrare_id, id_aviz):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul GN Delgaz din 6 judete diferite:
    Iasi, Bacau, Suceava, Botosani, Vaslui si Neamt.
    Modelul de cerere este același pentru toate cele 6 județe.
    Documentația generata este inaiantata pe email in format PDF, un singur fișier.
    Fișierul "Model email" conține informațiile necesare cu privire la conținutul emailului și adresa de email la care trebuie înaintată documentația.
    Adresade email este specifică fiecărui județ în parte, iar modelul de email este același pentru toate cele 6 județe.
    """
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

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/00. Common/03. GN Delgaz/Cerere GN Delgaz.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/00. Common/03. GN Delgaz/Model email - GN Delgaz.docx"

        # 1. Verificare câmpuri necesare
        errors = utils.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = utils.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            # 3. Generare document final
            temp_files.append(cerere_pdf_path)
            path_document_final = utils.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir
            )
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = utils.genereaza_email(
                lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact, model_detalii, temp_dir)
            fisiere_generate.append(email_pdf_path)

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
        print(f"Eroare în aviz_GN_Delgaz: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Orange(lucrare_id, id_aviz):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul Orange.
    Modelul de cerere este același pentru toate județele.
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

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/00. Common/04. Aviz Orange/01. Cerere Orange.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/00. Common/04. Aviz Orange/Citeste-ma.docx"

        # 1. Verificare câmpuri necesare
        errors = utils.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # În cazul avizului Orange, fișierele sunt copiate direct în temp_dir și adăugate
            # atât în temp_files (pentru curățarea în caz de eroare) cât și în fisiere_generate
            # (pentru a fi returnate utilizatorului)

            # 2. Generare cerere
            cerere_pdf_path = utils.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)
            fisiere_generate.append(cerere_pdf_path)

            # 3. Copie Certificatul de urbanism
            cu_path = x.copy_file(cu.cale_CU.path, temp_dir,
                                  "02. Certificat de urbanism")
            temp_files.append(cu_path)
            fisiere_generate.append(cu_path)

            # 4. Copie Plan incadrare CU
            plan_path = x.copy_file(
                cu.cale_plan_incadrare_CU.path, temp_dir, "03. Plan incadrare CU")
            temp_files.append(plan_path)
            fisiere_generate.append(plan_path)

            # 5. Copie Plan de situație CU
            plan_situatie_path = x.copy_file(
                cu.cale_plan_situatie_CU.path, temp_dir, "04. Plan de situație CU")
            temp_files.append(plan_situatie_path)
            fisiere_generate.append(plan_situatie_path)

            # 6. Copie Memoriul tehnic
            memoriu_tehnic_path = x.copy_file(
                cu.cale_memoriu_tehnic_CU.path, temp_dir, "05. Memoriu tehnic")
            temp_files.append(memoriu_tehnic_path)
            fisiere_generate.append(memoriu_tehnic_path)

            # 7. Copie Acte facturare
            acte_facturare_path = x.copy_file(
                cu.cale_acte_facturare.path, temp_dir, "06. Acte facturare")
            temp_files.append(acte_facturare_path)
            fisiere_generate.append(acte_facturare_path)

            # 8. Generare Readme
            readme_pdf_path = utils.genereaza_readme(temp_dir, model_detalii)
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


def aviz_Cultura(lucrare_id, id_aviz):
    """
    Aceasta functie genereaza documentatia necesara pentru avizul Cultura.
    Aceasta functie se deosebeste prin faptul ca, pentru fiecare judet in parte, avem un model diferit de cerere.
    Totodata, la unele judete documentatia se depune doar in fizic, adica printata si expediata prin posta, iar la altele se depune atat fizic cat si pe email"""
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

        if lucrare.judet.nume == "Iași":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/00. Common/05. Aviz Cultura/Cerere Cultura - Iasi.docx"
        elif lucrare.judet.nume == "Neamț":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/00. Common/05. Aviz Cultura/Cerere Cultura - Neamt.docx"
        elif lucrare.judet.nume == "Botoșani":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/00. Common/05. Aviz Cultura/Cerere Cultura - Botosani.docx"
        else:
            return DocumentGenerationResult.error_result("Nu găsesc modelul pentru Cerere Cultura")

        if lucrare.judet.nume == "Iași":
            model_detalii = "StudiiFezabilitate/Avize/modele_cereri/00. Common/05. Aviz Cultura/Model email - Iasi.docx"
        elif lucrare.judet.nume == "Neamț":
            model_detalii = "StudiiFezabilitate/Avize/modele_cereri/00. Common/05. Aviz Cultura/Model email - Neamt.docx"
        elif lucrare.judet.nume == "Botoșani":
            model_detalii = "StudiiFezabilitate/Avize/modele_cereri/00. Common/05. Aviz Cultura/Model email - Botosani.docx"
        else:
            return DocumentGenerationResult.error_result("Nu găsesc modelul pentru Emailul catre Cultura")

        # 1. Verificare câmpuri necesare
        errors = utils.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        # 1. Verificare câmpuri necesare speciale pentru avizul Cultura
        errors_cultura = common.verifica_campuri_necesare_EXTRA(cu, avizCU)
        # Check if errors_cultura is a DocumentGenerationResult and if it's an error result
        if errors_cultura is not None and not errors_cultura.is_success():
            return errors_cultura

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = common.genereaza_cerere_CULTURA(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = utils.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir
            )
            fisiere_generate.append(path_document_final)

            if lucrare.judet.nume == "Iași" or lucrare.judet.nume == "Neamț":
                cerere_printabila_pdf_path = utils.genereaza_document_final_print(
                    avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
                fisiere_generate.append(cerere_printabila_pdf_path)

            # 4. Generare email
            email_pdf_path = utils.genereaza_email(
                lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact, model_detalii, temp_dir)
            fisiere_generate.append(email_pdf_path)

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
        print(f"Eroare în aviz_Cultura: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_HCL(lucrare_id, id_aviz):
    """
    Documentația pentru Avizul HCL se depune la instituția aferenta. In functie de fiecare UAT în parte aceasta se depune fizic sau online.
    Sunt foarte multe UAT-uri și nu stiu procedura de depunere la fiecare în parte astfel ca voi genera o documentație pentru depus online si una pentru depus fizic (cu pagini goale pentru a facilita printarea)
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

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/00. Common/06. Aviz HCL/Cerere HCL - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/00. Common/06. Aviz HCL/Cerere HCL - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/00. Common/06. Aviz HCL/Cerere HCL - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/00. Common/06. Aviz HCL/Citeste-ma.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = utils.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors        # 2. Verificare câmpuri necesare pentru Evidenta patrimoniu
        # Acest aviz are câmpuri necesare diferite față de celelalte avize
        extra_errors = common.verifica_campuri_necesare_HCL(cu)
        # Check if extra_errors is a DocumentGenerationResult and if it's an error result
        if extra_errors is not None and not extra_errors.is_success():
            return extra_errors

        temp_dir = tempfile.gettempdir()

        try:
            # 3. Generare cerere
            cerere_pdf_path = utils.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 4. Generare document final - de printat
            path_document_final = utils.genereaza_document_final_print(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            temp_files.append(path_document_final)
            fisiere_generate.append(path_document_final)

            # 4. Generare document final - de trimis fizic
            path_document_final = utils.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            temp_files.append(path_document_final)
            fisiere_generate.append(path_document_final)

            # 5. Generare Readme
            readme_pdf_path = utils.genereaza_readme(temp_dir, model_detalii)
            temp_files.append(readme_pdf_path)
            fisiere_generate.append(readme_pdf_path)

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
        print(f"Eroare în aviz_HCL: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Politia_Rutiera(lucrare_id, id_aviz):
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
