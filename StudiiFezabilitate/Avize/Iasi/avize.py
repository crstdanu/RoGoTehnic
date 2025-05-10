from StudiiFezabilitate.models import AvizeCU, Lucrare
from StudiiFezabilitate.result import DocumentGenerationResult

import tempfile

import StudiiFezabilitate.Avize.functii as x
import StudiiFezabilitate.Avize.Common.functii as common
import StudiiFezabilitate.Avize.Iasi.functii as iasi


def aviz_Apavital(lucrare_id, id_aviz):
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
        if errors:
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
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        try:
            # 2. Generare cerere
            cerere_pdf_path = iasi.genereaza_cerere(
                lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir)
            temp_files.append(cerere_pdf_path)
            # Nu adăugăm cerere_pdf_path în fisiere_generate deoarece va fi parte din documentul final

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
    pass


def aviz_CTP(lucrare_id, id_aviz):
    pass


def aviz_Salubris(lucrare_id, id_aviz):
    pass


def aviz_PMI_Mediu(lucrare_id, id_aviz):
    pass


def aviz_PMI_BSM(lucrare_id, id_aviz):
    pass


def aviz_PMI_SUP(lucrare_id, id_aviz):
    pass


def aviz_PMI_Spatii_Verzi(lucrare_id, id_aviz):
    pass


def aviz_PMI_Trafic_Urban(lucrare_id, id_aviz):
    pass


def aviz_PMI_GIS_Cadastru(lucrare_id, id_aviz):
    pass


def aviz_PMI_Nomenclatura_Urbana(lucrare_id, id_aviz):
    pass


def aviz_Evidenta_Patrimoniu(lucrare_id, id_aviz):
    pass
