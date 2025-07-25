from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult

import tempfile
import os

import StudiiFezabilitate.Avize.functii as x
import StudiiFezabilitate.Avize.Common.functii as common
import StudiiFezabilitate.Avize.Iasi.functii as iasi


def aviz_Apavital(lucrare_id, id_aviz):
    """
    Acest aviz se depune online pe platforma Apavital
    De aceea este nevoie sa generam fisierele separate
    Fisierul 'Citeste-ma' contine informatii cu privire la modul de depunere a documentatiei
    """
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/01. Aviz Apavital/01.Cerere Apavital.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/01. Aviz Apavital/Citeste-ma.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # În cazul avizului Apavital, fișierele sunt copiate direct în temp_dir și adăugate
            # atât în temp_files (pentru curățarea în caz de eroare) cât și în fisiere_generate
            # (pentru a fi returnate utilizatorului)

            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)
            fisiere_generate.append(cerere_pdf_path)

            # 3. Copiere documente necesare pentru aviz
            # Definim documentele ce trebuie copiate într-o structură mai ușor de gestionat
            documente_de_copiat = [
                (cu.cale_CU.path, "02. Certificat de urbanism"),
                (cu.cale_plan_incadrare_CU.path, "03. Plan incadrare CU"),
                (cu.cale_plan_situatie_CU.path, "04. Plan de situație CU"),
                (cu.cale_memoriu_tehnic_CU.path, "05. Memoriu tehnic"),
                (cu.cale_acte_facturare.path, "06. Acte facturare")
            ]

            # Parcurgem lista și copiem fiecare document
            for sursa, nume_destinatie in documente_de_copiat:
                document_path = x.copy_file(sursa, temp_dir, nume_destinatie)
                temp_files.append(document_path)
                fisiere_generate.append(document_path)

            # 4. Generare Readme
            readme_pdf_path = iasi.genereaza_readme(temp_dir, model_detalii)
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
        print(f"Eroare în aviz_Apavital: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_GN_Gazmir(lucrare_id, id_aviz):
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

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/02. Aviz GN Gazmir/Cerere aviz Gazmir.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/02. Aviz GN Gazmir/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = iasi.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = iasi.genereaza_email(
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
        print(f"Eroare în aviz_GN_Gazmir: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Termoficare(lucrare_id, id_aviz):
    """
    Avizul Termoficare se depune fizic la adresa institutiei astfel ca documentatia va trebui printata. 
    De aceea folosesc o functie care introduce pagini goale precum si documente in doua exemplare acolo unde e cazul
    Fisierul 'Citeste-ma' contine informatii cu privire la adresa de depunere a documentatiei si programul de lucru al institutiei.
    """
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/03. Aviz Termoficare/Cerere Termoficare.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/03. Aviz Termoficare/Citeste-ma.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = iasi.genereaza_document_final_print(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            # Adăugăm în temp_files pentru curățare în caz de eroare
            temp_files.append(path_document_final)
            fisiere_generate.append(path_document_final)

            # 4. Generare Readme
            readme_pdf_path = iasi.genereaza_readme(temp_dir, model_detalii)
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
        print(f"Eroare în aviz_Termoficare: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_CTP(lucrare_id, id_aviz):
    """
    Avizul CTP (Compania de Transport Public) se depune fizic la adresa institutiei astfel ca documentatia va trebui printata. 
    De aceea folosesc o functie care introduce pagini goale precum si documente in doua exemplare acolo unde e cazul.
    Fisierul 'Citeste-ma' contine informatii cu privire la adresa de depunere a documentatiei si programul de lucru al institutiei.
    """
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/04. Aviz CTP/Cerere CTP.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/04. Aviz CTP/Citeste-ma.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = iasi.genereaza_document_final_print(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            # Adăugăm în temp_files pentru curățare în caz de eroare
            temp_files.append(path_document_final)
            fisiere_generate.append(path_document_final)

            # 4. Generare Readme
            readme_pdf_path = iasi.genereaza_readme(temp_dir, model_detalii)
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
        print(f"Eroare în aviz_CTP: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Salubris(lucrare_id, id_aviz):
    """
    Avizul Salubris se depune fizic la adresa institutiei astfel ca documentatia va trebui printata. 
    De aceea folosesc o functie care introduce pagini goale precum si documente in doua exemplare acolo unde e cazul.
    Spre deosebire de restul avizelor de pana acum documentatia pentru acest aviz este diferita (sunt mai putine documente de depus) asa ca voi folosi o functie separata pentru generarea documentatiei
    Fisierul 'Citeste-ma' contine informatii cu privire la adresa de depunere a documentatiei si programul de lucru al institutiei.
    """
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        firma = lucrare.firma_proiectare
        reprezentant = firma.reprezentant
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/05. Aviz Salubris/Cerere Salubris.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/05. Aviz Salubris/Citeste-ma.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = iasi.genereaza_document_Salubris_print(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            # Adăugăm în temp_files pentru curățare în caz de eroare
            temp_files.append(path_document_final)
            fisiere_generate.append(path_document_final)

            # 4. Generare Readme
            readme_pdf_path = iasi.genereaza_readme(temp_dir, model_detalii)
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
        print(f"Eroare în aviz_Salubris: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_PMI_Mediu(lucrare_id, id_aviz):
    """
    Acest aviz se depune pe email astefel ca documentatia este in format pdf pentru a fi atasata emailului
    Spre deosebire de celelalte functii de generare a documentatiei pentru avize, aceasta mai adauga un Plan Mediu PMI
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

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/06. Aviz PMI-Mediu/Cerere Aviz Mediu PMI.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/06. Aviz PMI-Mediu/Model email.docx"
        model_anexa = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/06. Aviz PMI-Mediu/Plan Mediu PMI.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        # Verificăm existența tuturor modelelor de documente simultan
        for model_path, descriere in [
            (model_cerere, "Cerere Aviz Mediu PMI"),
            (model_detalii, "Model email"),
            (model_anexa, "Plan Mediu PMI")
        ]:
            if not os.path.exists(model_path):
                return DocumentGenerationResult.error_result(
                    f"Nu găsesc modelul pentru {descriere}: {model_path}")

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Genereaza Plan Mediu PMI
            plan_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_anexa, temp_dir)
            temp_files.append(plan_pdf_path)

            # 4. Generare document final
            path_document_final = iasi.genereaza_document_final_PMI_Mediu(
                avizCU, cerere_pdf_path, plan_pdf_path, cu, beneficiar, temp_dir)
            # Adăugăm în temp_files pentru curățare în caz de eroare
            temp_files.append(path_document_final)
            fisiere_generate.append(path_document_final)

            # 5. Generare email
            email_pdf_path = iasi.genereaza_email(
                lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact, model_detalii, temp_dir)
            # Adăugăm și în temp_files pentru curățare
            temp_files.append(email_pdf_path)
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
        print(f"Eroare în aviz_PMI_Mediu: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_PMI_BSM(lucrare_id, id_aviz):
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

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/07. Aviz PMI BSM/Model aviz PMI BSM - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/07. Aviz PMI BSM/Model aviz PMI BSM - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/07. Aviz PMI BSM/Model aviz PMI BSM - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/07. Aviz PMI BSM/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = iasi.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = iasi.genereaza_email(
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
        print(f"Eroare în aviz_PMI_BSM: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_PMI_SUP(lucrare_id, id_aviz):
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

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/08. Aviz PMI SUP/Model aviz PMI SUP - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/08. Aviz PMI SUP/Model aviz PMI SUP - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/08. Aviz PMI SUP/Model aviz PMI SUP - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/08. Aviz PMI SUP/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = iasi.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = iasi.genereaza_email(
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
        print(f"Eroare în aviz_PMI_SUP: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_PMI_Spatii_verzi(lucrare_id, id_aviz):
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

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/09. Aviz PMI - Spatii verzi/Model aviz PMI Spatii Verzi - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/09. Aviz PMI - Spatii verzi/Model aviz PMI Spatii Verzi - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/09. Aviz PMI - Spatii verzi/Model aviz PMI Spatii Verzi - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/09. Aviz PMI - Spatii verzi/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = iasi.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = iasi.genereaza_email(
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
        print(f"Eroare în aviz_PMI_Spatii_verzi: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_PMI_Trafic_urban(lucrare_id, id_aviz):
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

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/10. Aviz PMI - Trafic urban/Model aviz PMI - Trafic urban - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/10. Aviz PMI - Trafic urban/Model aviz PMI - Trafic urban - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/10. Aviz PMI - Trafic urban/Model aviz PMI - Trafic urban - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/10. Aviz PMI - Trafic urban/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = iasi.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = iasi.genereaza_email(
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
        print(f"Eroare în aviz_PMI_Trafic_urban: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_PMI_GIS_Cadastru(lucrare_id, id_aviz):
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

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/11. Aviz PMI - GIS Cadastru/Cerere Aviz GiS.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/11. Aviz PMI - GIS Cadastru/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = iasi.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = iasi.genereaza_email(
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
        print(f"Eroare în aviz_PMI_GIS_Cadastru: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_PMI_Nomenclatura_urbana(lucrare_id, id_aviz):
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

        model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/12. Aviz PMI - Nomenclatura urbana/Cerere PMI - Nomenclatura urbana.docx"
        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/12. Aviz PMI - Nomenclatura urbana/Model email.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 3. Generare document final
            path_document_final = iasi.genereaza_document_final(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            fisiere_generate.append(path_document_final)

            # 4. Generare email
            email_pdf_path = iasi.genereaza_email(
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
        print(f"Eroare în aviz_PMI_Nomenclatura_urbana: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_Evidenta_patrimoniu(lucrare_id, id_aviz):
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

        if firma.nume == "S.C. ROGOTEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/13. Aviz Evidenta patrimoniu/Cerere Evidenta Patrimoniu - ROGOTEHNIC.docx"
        elif firma.nume == "S.C. GENERAL TEHNIC S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/13. Aviz Evidenta patrimoniu/Cerere Evidenta Patrimoniu - GENERAL TEHNIC.docx"
        elif firma.nume == "S.C. PROING SERV S.R.L.":
            model_cerere = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/13. Aviz Evidenta patrimoniu/Cerere Evidenta Patrimoniu - PROING SERV.docx"
        else:
            return DocumentGenerationResult.error_result(
                "Nu am gasit modelul de cerere pentru firma de proiectare selectata")

        model_detalii = "StudiiFezabilitate/Avize/modele_cereri/01. iasi/13. Aviz Evidenta patrimoniu/Citeste-ma.docx"

        # Lista pentru a ține evidența fișierelor generate temporar și finale
        temp_files = []
        fisiere_generate = []
        path_document_final = None

        # 1. Verificare câmpuri necesare
        errors = iasi.verifica_campuri_necesare(
            lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii)
        # Check if errors is a DocumentGenerationResult and if it's an error result
        if errors is not None and not errors.is_success():
            return errors        # 2. Verificare câmpuri necesare pentru Evidenta patrimoniu
        # Acest aviz are câmpuri necesare diferite față de celelalte avize
        extra_errors = iasi.verifica_campuri_necesare_evidenta_patrimoniu(cu)
        # Check if extra_errors is a DocumentGenerationResult and if it's an error result
        if extra_errors is not None and not extra_errors.is_success():
            return extra_errors

        temp_dir = tempfile.gettempdir()

        try:
            # 3. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)

            # 4. Generare document final
            path_document_final = iasi.genereaza_document_final_print(
                avizCU, cerere_pdf_path, cu, beneficiar, temp_dir)
            temp_files.append(path_document_final)
            fisiere_generate.append(path_document_final)

            # 5. Generare Readme
            readme_pdf_path = iasi.genereaza_readme(temp_dir, model_detalii)
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
        print(f"Eroare în aviz_Evidenta_patrimoniu: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")
