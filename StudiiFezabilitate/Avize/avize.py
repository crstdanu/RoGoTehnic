from StudiiFezabilitate.models import AvizeCU, Lucrare
import StudiiFezabilitate.Avize.functii as x
from StudiiFezabilitate.result import DocumentGenerationResult
from docxtpl import DocxTemplate
import os
from datetime import datetime
import tempfile


def aviz_APM_iasi(lucrare_id, id_aviz):
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

        # 1. Generare documentație aviz
        # Verificări inițiale pentru documentația principală
        errors = x.check_required_fields([
            (firma.cale_stampila,
             "Nu se poate genera avizul - lipsește ștampila firmei de proiectare"),
            (reprezentant.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura reprezentantului firmei de proiectare"),
            (cu.inginer_intocmit.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura Inginerului intocmit"),
            (cu.inginer_verificat.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura Inginerului verificat"),
            (cu.cale_CU.path, "Nu se poate genera avizul - lipsește Certificatul de Urbanism"),
            (cu.cale_plan_incadrare_CU.path,
             "Nu se poate genera avizul - lipsește Planul de incadrare in zona"),
            (cu.cale_plan_situatie_CU.path,
             "Nu se poate genera avizul - lipsește Planul de situatie"),
            (cu.cale_chitanta_APM.path,
             "Nu se poate genera avizul - lipsește Chitanța APM"),
            (cu.cale_acte_facturare.path,
             "Nu se poate genera avizul - lipsesc Acte facturare"),
            (firma.nume, "Nu se poate genera avizul - lipsește Firma de proiectare"),
            (firma.adresa, "Nu se poate genera avizul - lipsește Adresa firmei de proiectare"),
            (firma.localitate, "Nu se poate genera avizul - lipsește Localitatea firmei de proiectare"),
            (firma.judet, "Nu se poate genera avizul - lipsește Județul firmei de proiectare"),
            (reprezentant.nume,
             "Nu se poate genera avizul - lipsește Reprezentantul firmei de proiectare"),
            (beneficiar.nume, "Nu se poate genera avizul - lipsește Beneficiarul"),
            (beneficiar.adresa, "Nu se poate genera avizul - lipsește Adresa beneficiarului"),
            (beneficiar.localitate,
             "Nu se poate genera avizul - lipsește Localitatea beneficiarului"),
            (beneficiar.judet, "Nu se poate genera avizul - lipsește Județul beneficiarului"),
            (contact.nume, "Nu se poate genera avizul - lipsește Persoana de contact"),
            (contact.telefon, "Nu se poate genera avizul - lipsește Telefonul persoanei de contact"),
            (firma.email, "Nu se poate genera avizul - lipsește Email-ul firmei de proiectare"),
            (cu.nume, "Nu se poate genera avizul - lipsește Numele lucrarii din Certificatul de urbanism"),
            (cu.adresa, "Nu se poate genera avizul - lipsește Adresa lucrarii din Certificatul de urbanism"),
            # Verificări pentru generarea emailului
            (cu.numar, "Nu se poate genera emailul - lipsește numărul certificatului de urbanism"),
            (cu.data, "Nu se poate genera emailul - lipsește data certificatului de urbanism"),
            (cu.emitent, "Nu se poate genera emailul - lipsește emitentul certificatului de urbanism"),
        ])
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        # Verificăm existența modelelor pentru ambele documente de la început
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\01. iasi\01. Aviz APM\Cerere_APM.docx"
        model_notificare = r"StudiiFezabilitate\services\modele_cereri\01. iasi\01. Aviz APM\Notificare.docx"
        model_email = r"StudiiFezabilitate\services\modele_cereri\01. iasi\01. Aviz APM\Model email.docx"

        if not os.path.exists(model_cerere):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru cererea APM Iași")

        if not os.path.exists(model_notificare):
            return DocumentGenerationResult.error_result(
                "Nu găsesc șablonul pentru notificarea APM Iași")

        if not os.path.exists(model_email):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru Emailul APM Iași")

        try:
            # ----- Cerere
            context_cerere = {
                'nume_firma_proiectare': firma.nume,
                'localitate_firma_proiectare': firma.localitate.nume,
                'adresa_firma_proiectare': firma.adresa,
                'judet_firma_proiectare': firma.judet.nume,
                'nume_beneficiar': beneficiar.nume,
                'email_firma_proiectare': firma.email,
                'persoana_contact': contact.nume,
                'telefon_contact': contact.telefon,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'data': datetime.now().strftime("%d.%m.%Y"),
            }

            cerere_pdf_path = x.create_document(
                model_cerere, context_cerere, temp_dir,
                firma.cale_stampila.path,
                reprezentant.cale_semnatura.path,
            )
            temp_files.append(cerere_pdf_path)

            # ----- Notificare
            context_notificare = {
                'nume_firma_proiectare': firma.nume,
                'localitate_firma_proiectare': firma.localitate.nume,
                'adresa_firma_proiectare': firma.adresa,
                'judet_firma_proiectare': firma.judet.nume,
                'reprezentant_firma_proiectare': reprezentant.nume,
                'nume_beneficiar': beneficiar.nume,
                'localitate_beneficiar': beneficiar.localitate.nume,
                'adresa_beneficiar': beneficiar.adresa,
                'judet_beneficiar': beneficiar.judet.nume,
                'email_firma_proiectare': firma.email,
                'descrierea_proiectului': cu.descrierea_proiectului,
                'telefon_contact': contact.telefon,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'inginer_intocmit': cu.inginer_intocmit.nume,
                'inginer_verificat': cu.inginer_verificat.nume,
            }

            notificare_pdf_path = x.create_document(
                model_notificare, context_notificare, temp_dir,
                firma.cale_stampila.path,
                cu.inginer_intocmit.cale_semnatura.path,
                cu.inginer_verificat.cale_semnatura.path,
            )
            temp_files.append(notificare_pdf_path)

            # ----- Document final
            path_document_final = os.path.join(
                temp_dir, f"Documentatie aviz APM Iași - {beneficiar.nume}.pdf"
            )

            pdf_list = [
                cerere_pdf_path,
                cu.cale_chitanta_APM.path,
                cu.cale_CU.path,
                cu.cale_plan_incadrare_CU.path,
                cu.cale_plan_situatie_CU.path,
                notificare_pdf_path,
                cu.cale_acte_facturare.path,
            ]

            x.merge_pdfs(pdf_list, path_document_final)
            fisiere_generate.append(path_document_final)

            # 2. Generare email APM
            context_email = {
                'nume_beneficiar': beneficiar.nume,
                'nr_cu': cu.numar,
                'data_cu': cu.data,
                'emitent_cu': cu.emitent,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'persoana_contact': contact.nume,
                'telefon_contact': contact.telefon,
            }

            email_pdf_path = x.create_document(
                model_email, context_email, temp_dir,
            )

            # Verifică dacă PDF-ul emailului există și are conținut
            if not os.path.exists(email_pdf_path) or os.path.getsize(email_pdf_path) == 0:
                raise Exception(
                    f"Emailul a fost generat, dar fișierul este gol: {email_pdf_path}")

            fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            for path in temp_files:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            if path_document_final and os.path.exists(path_document_final):
                try:
                    os.remove(path_document_final)
                except:
                    pass

            for path in fisiere_generate:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în generate_documents_APM_iasi: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_APM_neamt(lucrare_id, id_aviz):
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

        # 1. Generare documentație aviz
        # Verificări inițiale pentru documentația principală
        errors = x.check_required_fields([
            (firma.cale_stampila,
             "Nu se poate genera avizul - lipsește ștampila firmei de proiectare"),
            (reprezentant.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura reprezentantului firmei de proiectare"),
            (cu.inginer_intocmit.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura Inginerului intocmit"),
            (cu.inginer_verificat.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura Inginerului verificat"),
            (cu.cale_CU.path, "Nu se poate genera avizul - lipsește Certificatul de Urbanism"),
            (cu.cale_plan_incadrare_CU.path,
             "Nu se poate genera avizul - lipsește Planul de incadrare in zona"),
            (cu.cale_plan_situatie_CU.path,
             "Nu se poate genera avizul - lipsește Planul de situatie"),
            (cu.cale_chitanta_APM.path,
             "Nu se poate genera avizul - lipsește Chitanța APM"),
            (cu.cale_acte_facturare.path,
             "Nu se poate genera avizul - lipsesc Acte facturare"),
            (firma.nume, "Nu se poate genera avizul - lipsește Firma de proiectare"),
            (firma.adresa, "Nu se poate genera avizul - lipsește Adresa firmei de proiectare"),
            (firma.localitate, "Nu se poate genera avizul - lipsește Localitatea firmei de proiectare"),
            (firma.judet, "Nu se poate genera avizul - lipsește Județul firmei de proiectare"),
            (reprezentant.nume,
             "Nu se poate genera avizul - lipsește Reprezentantul firmei de proiectare"),
            (beneficiar.nume, "Nu se poate genera avizul - lipsește Beneficiarul"),
            (beneficiar.adresa, "Nu se poate genera avizul - lipsește Adresa beneficiarului"),
            (beneficiar.localitate,
             "Nu se poate genera avizul - lipsește Localitatea beneficiarului"),
            (beneficiar.judet, "Nu se poate genera avizul - lipsește Județul beneficiarului"),
            (contact.nume, "Nu se poate genera avizul - lipsește Persoana de contact"),
            (contact.telefon, "Nu se poate genera avizul - lipsește Telefonul persoanei de contact"),
            (firma.email, "Nu se poate genera avizul - lipsește Email-ul firmei de proiectare"),
            (cu.nume, "Nu se poate genera avizul - lipsește Numele lucrarii din Certificatul de urbanism"),
            (cu.adresa, "Nu se poate genera avizul - lipsește Adresa lucrarii din Certificatul de urbanism"),
            # Verificări pentru generarea emailului - le adăugăm aici pentru a verifica totul de la început
            (cu.numar, "Nu se poate genera emailul - lipsește numărul certificatului de urbanism"),
            (cu.data, "Nu se poate genera emailul - lipsește data certificatului de urbanism"),
            (cu.emitent, "Nu se poate genera emailul - lipsește emitentul certificatului de urbanism"),
        ])
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        # Verificăm existența modelelor pentru ambele documente de la început
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\02. neamt\01. Aviz APM\Cerere_APM.docx"
        model_notificare = r"StudiiFezabilitate\services\modele_cereri\02. neamt\01. Aviz APM\Notificare.docx"
        model_email = r"StudiiFezabilitate\services\modele_cereri\02. neamt\01. Aviz APM\Model email.docx"

        if not os.path.exists(model_cerere):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru cererea APM Neamț")

        if not os.path.exists(model_notificare):
            return DocumentGenerationResult.error_result(
                "Nu găsesc șablonul pentru notificarea APM Neamț")

        if not os.path.exists(model_email):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru Emailul APM Neamț")

        try:
            # ----- Cerere
            context_cerere = {
                'nume_firma_proiectare': firma.nume,
                'localitate_firma_proiectare': firma.localitate.nume,
                'adresa_firma_proiectare': firma.adresa,
                'judet_firma_proiectare': firma.judet.nume,
                'nume_beneficiar': beneficiar.nume,
                'email_firma_proiectare': firma.email,
                'persoana_contact': contact.nume,
                'telefon_contact': contact.telefon,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'data': datetime.now().strftime("%d.%m.%Y"),
            }

            cerere_pdf_path = x.create_document(
                model_cerere, context_cerere, temp_dir,
                firma.cale_stampila.path,
                reprezentant.cale_semnatura.path,
            )
            temp_files.append(cerere_pdf_path)

            # ----- Notificare
            context_notificare = {
                'nume_firma_proiectare': firma.nume,
                'localitate_firma_proiectare': firma.localitate.nume,
                'adresa_firma_proiectare': firma.adresa,
                'judet_firma_proiectare': firma.judet.nume,
                'reprezentant_firma_proiectare': reprezentant.nume,
                'nume_beneficiar': beneficiar.nume,
                'localitate_beneficiar': beneficiar.localitate.nume,
                'adresa_beneficiar': beneficiar.adresa,
                'judet_beneficiar': beneficiar.judet.nume,
                'email_firma_proiectare': firma.email,
                'descrierea_proiectului': cu.descrierea_proiectului,
                'telefon_contact': contact.telefon,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'inginer_intocmit': cu.inginer_intocmit.nume,
                'inginer_verificat': cu.inginer_verificat.nume,
            }

            notificare_pdf_path = x.create_document(
                model_notificare, context_notificare, temp_dir,
                firma.cale_stampila.path,
                cu.inginer_intocmit.cale_semnatura.path,
                cu.inginer_verificat.cale_semnatura.path,
            )
            temp_files.append(notificare_pdf_path)

            # ----- Document final
            path_document_final = os.path.join(
                temp_dir, f"Documentatie aviz APM Neamț - {beneficiar.nume}.pdf"
            )

            pdf_list = [
                cerere_pdf_path,
                cu.cale_chitanta_APM.path,
                cu.cale_CU.path,
                cu.cale_plan_incadrare_CU.path,
                cu.cale_plan_situatie_CU.path,
                notificare_pdf_path,
                cu.cale_acte_facturare.path,
            ]

            x.merge_pdfs(pdf_list, path_document_final)
            fisiere_generate.append(path_document_final)

            # 2. Generare email APM
            context_email = {
                'nume_beneficiar': beneficiar.nume,
                'nr_cu': cu.numar,
                'data_cu': cu.data,
                'emitent_cu': cu.emitent,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'persoana_contact': contact.nume,
                'telefon_contact': contact.telefon,
            }

            email_pdf_path = x.create_document(
                model_email, context_email, temp_dir,
            )

            # Verifică dacă PDF-ul emailului există și are conținut
            if not os.path.exists(email_pdf_path) or os.path.getsize(email_pdf_path) == 0:
                raise Exception(
                    f"Emailul a fost generat, dar fișierul este gol: {email_pdf_path}")

            fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            for path in temp_files:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            if path_document_final and os.path.exists(path_document_final):
                try:
                    os.remove(path_document_final)
                except:
                    pass

            for path in fisiere_generate:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în generate_documents_APM_neamt: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_APM_bacau(lucrare_id, id_aviz):
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

        # 1. Generare documentație aviz
        # Verificări inițiale pentru documentația principală
        errors = x.check_required_fields([
            (firma.cale_stampila,
             "Nu se poate genera avizul - lipsește ștampila firmei de proiectare"),
            (reprezentant.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura reprezentantului firmei de proiectare"),
            (cu.inginer_intocmit.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura Inginerului intocmit"),
            (cu.inginer_verificat.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura Inginerului verificat"),
            (cu.cale_CU.path, "Nu se poate genera avizul - lipsește Certificatul de Urbanism"),
            (cu.cale_plan_incadrare_CU.path,
             "Nu se poate genera avizul - lipsește Planul de incadrare in zona"),
            (cu.cale_plan_situatie_CU.path,
             "Nu se poate genera avizul - lipsește Planul de situatie"),
            (cu.cale_chitanta_APM.path,
             "Nu se poate genera avizul - lipsește Chitanța APM"),
            (cu.cale_acte_facturare.path,
             "Nu se poate genera avizul - lipsesc Acte facturare"),
            (firma.nume, "Nu se poate genera avizul - lipsește Firma de proiectare"),
            (firma.adresa, "Nu se poate genera avizul - lipsește Adresa firmei de proiectare"),
            (firma.localitate, "Nu se poate genera avizul - lipsește Localitatea firmei de proiectare"),
            (firma.judet, "Nu se poate genera avizul - lipsește Județul firmei de proiectare"),
            (reprezentant.nume,
             "Nu se poate genera avizul - lipsește Reprezentantul firmei de proiectare"),
            (beneficiar.nume, "Nu se poate genera avizul - lipsește Beneficiarul"),
            (beneficiar.adresa, "Nu se poate genera avizul - lipsește Adresa beneficiarului"),
            (beneficiar.localitate,
             "Nu se poate genera avizul - lipsește Localitatea beneficiarului"),
            (beneficiar.judet, "Nu se poate genera avizul - lipsește Județul beneficiarului"),
            (contact.nume, "Nu se poate genera avizul - lipsește Persoana de contact"),
            (contact.telefon, "Nu se poate genera avizul - lipsește Telefonul persoanei de contact"),
            (firma.email, "Nu se poate genera avizul - lipsește Email-ul firmei de proiectare"),
            (cu.nume, "Nu se poate genera avizul - lipsește Numele lucrarii din Certificatul de urbanism"),
            (cu.adresa, "Nu se poate genera avizul - lipsește Adresa lucrarii din Certificatul de urbanism"),
            (cu.numar, "Nu se poate genera avizul - lipsește numărul certificatului de urbanism"),
            (cu.data, "Nu se poate genera avizul - lipsește data certificatului de urbanism"),
            (cu.emitent, "Nu se poate genera avizul - lipsește emitentul certificatului de urbanism"),
        ])
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        # Verificăm existența modelelor pentru toate documentele de la început
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\03. bacau\01. Aviz APM\Cerere_APM.docx"
        model_notificare = r"StudiiFezabilitate\services\modele_cereri\03. bacau\01. Aviz APM\Notificare.docx"
        model_citeste_ma = r"StudiiFezabilitate\services\modele_cereri\03. bacau\01. Aviz APM\Citeste-ma.docx"

        if not os.path.exists(model_cerere):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru cererea APM Bacău")

        if not os.path.exists(model_notificare):
            return DocumentGenerationResult.error_result(
                "Nu găsesc șablonul pentru notificarea APM Bacău")

        if not os.path.exists(model_citeste_ma):
            return DocumentGenerationResult.error_result(
                "Nu găsesc fișierul Citeste-ma pentru APM Bacău")

        try:
            # ----- Cerere
            context_cerere = {
                'nume_firma_proiectare': firma.nume,
                'localitate_firma_proiectare': firma.localitate.nume,
                'adresa_firma_proiectare': firma.adresa,
                'judet_firma_proiectare': firma.judet.nume,
                'nume_beneficiar': beneficiar.nume,
                'email_firma_proiectare': firma.email,
                'persoana_contact': contact.nume,
                'telefon_contact': contact.telefon,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'data': datetime.now().strftime("%d.%m.%Y"),
            }

            cerere_pdf_path = x.create_document(
                model_cerere, context_cerere, temp_dir,
                firma.cale_stampila.path,
                reprezentant.cale_semnatura.path,
            )
            temp_files.append(cerere_pdf_path)

            # ----- Notificare
            context_notificare = {
                'nume_firma_proiectare': firma.nume,
                'localitate_firma_proiectare': firma.localitate.nume,
                'adresa_firma_proiectare': firma.adresa,
                'judet_firma_proiectare': firma.judet.nume,
                'reprezentant_firma_proiectare': reprezentant.nume,
                'nume_beneficiar': beneficiar.nume,
                'localitate_beneficiar': beneficiar.localitate.nume,
                'adresa_beneficiar': beneficiar.adresa,
                'judet_beneficiar': beneficiar.judet.nume,
                'email_firma_proiectare': firma.email,
                'descrierea_proiectului': cu.descrierea_proiectului,
                'telefon_contact': contact.telefon,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'inginer_intocmit': cu.inginer_intocmit.nume,
                'inginer_verificat': cu.inginer_verificat.nume,
            }

            notificare_pdf_path = x.create_document(
                model_notificare, context_notificare, temp_dir,
                firma.cale_stampila.path,
                cu.inginer_intocmit.cale_semnatura.path,
                cu.inginer_verificat.cale_semnatura.path,
            )
            temp_files.append(notificare_pdf_path)

            # ----- Document final
            path_document_final = os.path.join(
                temp_dir, f"Documentatie aviz APM Bacău - {beneficiar.nume}.pdf"
            )

            pdf_list = [
                cerere_pdf_path,
                cu.cale_chitanta_APM.path,
                cu.cale_CU.path,
                cu.cale_plan_incadrare_CU.path,
                cu.cale_plan_situatie_CU.path,
                notificare_pdf_path,
                cu.cale_acte_facturare.path,
            ]

            x.merge_pdfs(pdf_list, path_document_final)
            fisiere_generate.append(path_document_final)

            # 2. Generare Citeste-ma pentru APM Bacău cu validări adecvate
            try:
                # Copierea fișierului în directorul temporar
                new_file_path = x.copy_file(model_citeste_ma, temp_dir)
                if not new_file_path or not os.path.exists(new_file_path):
                    raise Exception(
                        f"Nu s-a putut copia fișierul Citeste-ma în {temp_dir}")

                temp_files.append(new_file_path)

                # Convertirea în PDF
                citeste_ma_pdf_path = x.convert_to_pdf(new_file_path)
                if not citeste_ma_pdf_path or not os.path.exists(citeste_ma_pdf_path):
                    raise Exception(
                        f"Nu s-a putut converti fișierul Citeste-ma în PDF")

                # Verifică dacă PDF-ul are conținut
                if os.path.getsize(citeste_ma_pdf_path) == 0:
                    raise Exception(
                        f"Fișierul PDF Citeste-ma generat este gol: {citeste_ma_pdf_path}")

                fisiere_generate.append(citeste_ma_pdf_path)
            except Exception as e:
                raise Exception(
                    f"Eroare la procesarea fișierului Citeste-ma: {str(e)}")

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            for path in temp_files:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            if path_document_final and os.path.exists(path_document_final):
                try:
                    os.remove(path_document_final)
                except:
                    pass

            for path in fisiere_generate:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în aviz_APM_bacau: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_APM_botosani(lucrare_id, id_aviz):
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

        # 1. Generare documentație aviz
        # Verificări inițiale pentru documentația principală
        errors = x.check_required_fields([
            (firma.cale_stampila,
             "Nu se poate genera avizul - lipsește ștampila firmei de proiectare"),
            (reprezentant.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura reprezentantului firmei de proiectare"),
            (cu.inginer_intocmit.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura Inginerului intocmit"),
            (cu.inginer_verificat.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura Inginerului verificat"),
            (cu.cale_CU.path, "Nu se poate genera avizul - lipsește Certificatul de Urbanism"),
            (cu.cale_plan_incadrare_CU.path,
             "Nu se poate genera avizul - lipsește Planul de incadrare in zona"),
            (cu.cale_plan_situatie_CU.path,
             "Nu se poate genera avizul - lipsește Planul de situatie"),
            (cu.cale_chitanta_APM.path,
             "Nu se poate genera avizul - lipsește Chitanța APM"),
            (cu.cale_acte_facturare.path,
             "Nu se poate genera avizul - lipsesc Acte facturare"),
            (firma.nume, "Nu se poate genera avizul - lipsește Firma de proiectare"),
            (firma.adresa, "Nu se poate genera avizul - lipsește Adresa firmei de proiectare"),
            (firma.localitate, "Nu se poate genera avizul - lipsește Localitatea firmei de proiectare"),
            (firma.judet, "Nu se poate genera avizul - lipsește Județul firmei de proiectare"),
            (reprezentant.nume,
             "Nu se poate genera avizul - lipsește Reprezentantul firmei de proiectare"),
            (beneficiar.nume, "Nu se poate genera avizul - lipsește Beneficiarul"),
            (beneficiar.adresa, "Nu se poate genera avizul - lipsește Adresa beneficiarului"),
            (beneficiar.localitate,
             "Nu se poate genera avizul - lipsește Localitatea beneficiarului"),
            (beneficiar.judet, "Nu se poate genera avizul - lipsește Județul beneficiarului"),
            (contact.nume, "Nu se poate genera avizul - lipsește Persoana de contact"),
            (contact.telefon, "Nu se poate genera avizul - lipsește Telefonul persoanei de contact"),
            (firma.email, "Nu se poate genera avizul - lipsește Email-ul firmei de proiectare"),
            (cu.nume, "Nu se poate genera avizul - lipsește Numele lucrarii din Certificatul de urbanism"),
            (cu.adresa, "Nu se poate genera avizul - lipsește Adresa lucrarii din Certificatul de urbanism"),
            # Verificări pentru generarea emailului - le adăugăm aici pentru a verifica totul de la început
            (cu.numar, "Nu se poate genera emailul - lipsește numărul certificatului de urbanism"),
            (cu.data, "Nu se poate genera emailul - lipsește data certificatului de urbanism"),
            (cu.emitent, "Nu se poate genera emailul - lipsește emitentul certificatului de urbanism"),
        ])
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        # Verificăm existența modelelor pentru ambele documente de la început
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\04. botosani\01. Aviz APM\Cerere_APM.docx"
        model_notificare = r"StudiiFezabilitate\services\modele_cereri\04. botosani\01. Aviz APM\Notificare.docx"
        model_email = r"StudiiFezabilitate\services\modele_cereri\04. botosani\01. Aviz APM\Model email.docx"

        if not os.path.exists(model_cerere):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru cererea APM Botoșani")

        if not os.path.exists(model_notificare):
            return DocumentGenerationResult.error_result(
                "Nu găsesc șablonul pentru notificarea APM Botoșani")

        if not os.path.exists(model_email):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru Emailul APM Botoșani")

        try:
            # ----- Cerere
            context_cerere = {
                'nume_firma_proiectare': firma.nume,
                'localitate_firma_proiectare': firma.localitate.nume,
                'adresa_firma_proiectare': firma.adresa,
                'judet_firma_proiectare': firma.judet.nume,
                'nume_beneficiar': beneficiar.nume,
                'email_firma_proiectare': firma.email,
                'persoana_contact': contact.nume,
                'telefon_contact': contact.telefon,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'data': datetime.now().strftime("%d.%m.%Y"),
            }

            cerere_pdf_path = x.create_document(
                model_cerere, context_cerere, temp_dir,
                firma.cale_stampila.path,
                reprezentant.cale_semnatura.path,
            )
            temp_files.append(cerere_pdf_path)

            # ----- Notificare
            context_notificare = {
                'nume_firma_proiectare': firma.nume,
                'localitate_firma_proiectare': firma.localitate.nume,
                'adresa_firma_proiectare': firma.adresa,
                'judet_firma_proiectare': firma.judet.nume,
                'reprezentant_firma_proiectare': reprezentant.nume,
                'nume_beneficiar': beneficiar.nume,
                'localitate_beneficiar': beneficiar.localitate.nume,
                'adresa_beneficiar': beneficiar.adresa,
                'judet_beneficiar': beneficiar.judet.nume,
                'email_firma_proiectare': firma.email,
                'descrierea_proiectului': cu.descrierea_proiectului,
                'telefon_contact': contact.telefon,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'inginer_intocmit': cu.inginer_intocmit.nume,
                'inginer_verificat': cu.inginer_verificat.nume,
            }

            notificare_pdf_path = x.create_document(
                model_notificare, context_notificare, temp_dir,
                firma.cale_stampila.path,
                cu.inginer_intocmit.cale_semnatura.path,
                cu.inginer_verificat.cale_semnatura.path,
            )
            temp_files.append(notificare_pdf_path)

            # ----- Document final
            path_document_final = os.path.join(
                temp_dir, f"Documentatie aviz APM Botoșani - {beneficiar.nume}.pdf"
            )

            pdf_list = [
                cerere_pdf_path,
                cu.cale_chitanta_APM.path,
                cu.cale_CU.path,
                cu.cale_plan_incadrare_CU.path,
                cu.cale_plan_situatie_CU.path,
                notificare_pdf_path,
                cu.cale_acte_facturare.path,
            ]

            x.merge_pdfs(pdf_list, path_document_final)
            fisiere_generate.append(path_document_final)

            # 2. Generare email APM
            context_email = {
                'nume_beneficiar': beneficiar.nume,
                'nr_cu': cu.numar,
                'data_cu': cu.data,
                'emitent_cu': cu.emitent,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'persoana_contact': contact.nume,
                'telefon_contact': contact.telefon,
            }

            email_pdf_path = x.create_document(
                model_email, context_email, temp_dir,
            )

            # Verifică dacă PDF-ul emailului există și are conținut
            if not os.path.exists(email_pdf_path) or os.path.getsize(email_pdf_path) == 0:
                raise Exception(
                    f"Emailul a fost generat, dar fișierul este gol: {email_pdf_path}")

            fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            for path in temp_files:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            if path_document_final and os.path.exists(path_document_final):
                try:
                    os.remove(path_document_final)
                except:
                    pass

            for path in fisiere_generate:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în generate_documents_APM_botosani: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_APM_suceava(lucrare_id, id_aviz):
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

        # 1. Generare documentație aviz
        # Verificări inițiale pentru documentația principală
        errors = x.check_required_fields([
            (firma.cale_stampila,
             "Nu se poate genera avizul - lipsește ștampila firmei de proiectare"),
            (reprezentant.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura reprezentantului firmei de proiectare"),
            (cu.inginer_intocmit.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura Inginerului intocmit"),
            (cu.inginer_verificat.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura Inginerului verificat"),
            (cu.cale_CU.path, "Nu se poate genera avizul - lipsește Certificatul de Urbanism"),
            (cu.cale_plan_incadrare_CU.path,
             "Nu se poate genera avizul - lipsește Planul de incadrare in zona"),
            (cu.cale_plan_situatie_CU.path,
             "Nu se poate genera avizul - lipsește Planul de situatie"),
            (cu.cale_chitanta_APM.path,
             "Nu se poate genera avizul - lipsește Chitanța APM"),
            (cu.cale_acte_facturare.path,
             "Nu se poate genera avizul - lipsesc Acte facturare"),
            (firma.nume, "Nu se poate genera avizul - lipsește Firma de proiectare"),
            (firma.adresa, "Nu se poate genera avizul - lipsește Adresa firmei de proiectare"),
            (firma.localitate, "Nu se poate genera avizul - lipsește Localitatea firmei de proiectare"),
            (firma.judet, "Nu se poate genera avizul - lipsește Județul firmei de proiectare"),
            (reprezentant.nume,
             "Nu se poate genera avizul - lipsește Reprezentantul firmei de proiectare"),
            (beneficiar.nume, "Nu se poate genera avizul - lipsește Beneficiarul"),
            (beneficiar.adresa, "Nu se poate genera avizul - lipsește Adresa beneficiarului"),
            (beneficiar.localitate,
             "Nu se poate genera avizul - lipsește Localitatea beneficiarului"),
            (beneficiar.judet, "Nu se poate genera avizul - lipsește Județul beneficiarului"),
            (contact.nume, "Nu se poate genera avizul - lipsește Persoana de contact"),
            (contact.telefon, "Nu se poate genera avizul - lipsește Telefonul persoanei de contact"),
            (firma.email, "Nu se poate genera avizul - lipsește Email-ul firmei de proiectare"),
            (cu.nume, "Nu se poate genera avizul - lipsește Numele lucrarii din Certificatul de urbanism"),
            (cu.adresa, "Nu se poate genera avizul - lipsește Adresa lucrarii din Certificatul de urbanism"),
            # Verificări pentru generarea emailului - le adăugăm aici pentru a verifica totul de la început
            (cu.numar, "Nu se poate genera emailul - lipsește numărul certificatului de urbanism"),
            (cu.data, "Nu se poate genera emailul - lipsește data certificatului de urbanism"),
            (cu.emitent, "Nu se poate genera emailul - lipsește emitentul certificatului de urbanism"),
        ])
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        # Verificăm existența modelelor pentru ambele documente de la început
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\05. suceava\01. Aviz APM\Cerere_APM.docx"
        model_notificare = r"StudiiFezabilitate\services\modele_cereri\05. suceava\01. Aviz APM\Notificare.docx"
        model_email = r"StudiiFezabilitate\services\modele_cereri\05. suceava\01. Aviz APM\Model email.docx"

        if not os.path.exists(model_cerere):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru cererea APM Suceava")

        if not os.path.exists(model_notificare):
            return DocumentGenerationResult.error_result(
                "Nu găsesc șablonul pentru notificarea APM Suceava")

        if not os.path.exists(model_email):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru Emailul APM Suceava")

        try:
            # ----- Cerere
            context_cerere = {
                'nume_firma_proiectare': firma.nume,
                'localitate_firma_proiectare': firma.localitate.nume,
                'adresa_firma_proiectare': firma.adresa,
                'judet_firma_proiectare': firma.judet.nume,
                'nume_beneficiar': beneficiar.nume,
                'email_firma_proiectare': firma.email,
                'persoana_contact': contact.nume,
                'telefon_contact': contact.telefon,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'data': datetime.now().strftime("%d.%m.%Y"),
            }

            cerere_pdf_path = x.create_document(
                model_cerere, context_cerere, temp_dir,
                firma.cale_stampila.path,
                reprezentant.cale_semnatura.path,
            )
            temp_files.append(cerere_pdf_path)

            # ----- Notificare
            context_notificare = {
                'nume_firma_proiectare': firma.nume,
                'localitate_firma_proiectare': firma.localitate.nume,
                'adresa_firma_proiectare': firma.adresa,
                'judet_firma_proiectare': firma.judet.nume,
                'reprezentant_firma_proiectare': reprezentant.nume,
                'nume_beneficiar': beneficiar.nume,
                'localitate_beneficiar': beneficiar.localitate.nume,
                'adresa_beneficiar': beneficiar.adresa,
                'judet_beneficiar': beneficiar.judet.nume,
                'email_firma_proiectare': firma.email,
                'descrierea_proiectului': cu.descrierea_proiectului,
                'telefon_contact': contact.telefon,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'inginer_intocmit': cu.inginer_intocmit.nume,
                'inginer_verificat': cu.inginer_verificat.nume,
            }

            notificare_pdf_path = x.create_document(
                model_notificare, context_notificare, temp_dir,
                firma.cale_stampila.path,
                cu.inginer_intocmit.cale_semnatura.path,
                cu.inginer_verificat.cale_semnatura.path,
            )
            temp_files.append(notificare_pdf_path)

            # ----- Document final
            path_document_final = os.path.join(
                temp_dir, f"Documentatie aviz APM Suceava - {beneficiar.nume}.pdf"
            )

            pdf_list = [
                cerere_pdf_path,
                cu.cale_chitanta_APM.path,
                cu.cale_CU.path,
                cu.cale_plan_incadrare_CU.path,
                cu.cale_plan_situatie_CU.path,
                notificare_pdf_path,
                cu.cale_acte_facturare.path,
            ]

            x.merge_pdfs(pdf_list, path_document_final)
            fisiere_generate.append(path_document_final)

            # 2. Generare email APM
            context_email = {
                'nume_beneficiar': beneficiar.nume,
                'nr_cu': cu.numar,
                'data_cu': cu.data,
                'emitent_cu': cu.emitent,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'persoana_contact': contact.nume,
                'telefon_contact': contact.telefon,
            }

            email_pdf_path = x.create_document(
                model_email, context_email, temp_dir,
            )

            # Verifică dacă PDF-ul emailului există și are conținut
            if not os.path.exists(email_pdf_path) or os.path.getsize(email_pdf_path) == 0:
                raise Exception(
                    f"Emailul a fost generat, dar fișierul este gol: {email_pdf_path}")

            fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            for path in temp_files:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            if path_document_final and os.path.exists(path_document_final):
                try:
                    os.remove(path_document_final)
                except:
                    pass

            for path in fisiere_generate:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în generate_documents_APM_suceava: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def aviz_APM_vaslui(lucrare_id, id_aviz):
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

        # 1. Generare documentație aviz
        # Verificări inițiale pentru documentația principală
        errors = x.check_required_fields([
            (firma.cale_stampila,
             "Nu se poate genera avizul - lipsește ștampila firmei de proiectare"),
            (reprezentant.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura reprezentantului firmei de proiectare"),
            (cu.inginer_intocmit.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura Inginerului intocmit"),
            (cu.inginer_verificat.cale_semnatura.path,
             "Nu se poate genera avizul - lipsește Semnatura Inginerului verificat"),
            (cu.cale_CU.path, "Nu se poate genera avizul - lipsește Certificatul de Urbanism"),
            (cu.cale_plan_incadrare_CU.path,
             "Nu se poate genera avizul - lipsește Planul de incadrare in zona"),
            (cu.cale_plan_situatie_CU.path,
             "Nu se poate genera avizul - lipsește Planul de situatie"),
            (cu.cale_chitanta_APM.path,
             "Nu se poate genera avizul - lipsește Chitanța APM"),
            (cu.cale_acte_facturare.path,
             "Nu se poate genera avizul - lipsesc Acte facturare"),
            (firma.nume, "Nu se poate genera avizul - lipsește Firma de proiectare"),
            (firma.adresa, "Nu se poate genera avizul - lipsește Adresa firmei de proiectare"),
            (firma.localitate, "Nu se poate genera avizul - lipsește Localitatea firmei de proiectare"),
            (firma.judet, "Nu se poate genera avizul - lipsește Județul firmei de proiectare"),
            (reprezentant.nume,
             "Nu se poate genera avizul - lipsește Reprezentantul firmei de proiectare"),
            (beneficiar.nume, "Nu se poate genera avizul - lipsește Beneficiarul"),
            (beneficiar.adresa, "Nu se poate genera avizul - lipsește Adresa beneficiarului"),
            (beneficiar.localitate,
             "Nu se poate genera avizul - lipsește Localitatea beneficiarului"),
            (beneficiar.judet, "Nu se poate genera avizul - lipsește Județul beneficiarului"),
            (contact.nume, "Nu se poate genera avizul - lipsește Persoana de contact"),
            (contact.telefon, "Nu se poate genera avizul - lipsește Telefonul persoanei de contact"),
            (firma.email, "Nu se poate genera avizul - lipsește Email-ul firmei de proiectare"),
            (cu.nume, "Nu se poate genera avizul - lipsește Numele lucrarii din Certificatul de urbanism"),
            (cu.adresa, "Nu se poate genera avizul - lipsește Adresa lucrarii din Certificatul de urbanism"),
            # Verificări pentru generarea emailului - le adăugăm aici pentru a verifica totul de la început
            (cu.numar, "Nu se poate genera emailul - lipsește numărul certificatului de urbanism"),
            (cu.data, "Nu se poate genera emailul - lipsește data certificatului de urbanism"),
            (cu.emitent, "Nu se poate genera emailul - lipsește emitentul certificatului de urbanism"),
        ])
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        # Verificăm existența modelelor pentru ambele documente de la început
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\06. vaslui\01. Aviz APM\Cerere_APM.docx"
        model_notificare = r"StudiiFezabilitate\services\modele_cereri\06. vaslui\01. Aviz APM\Notificare.docx"
        model_email = r"StudiiFezabilitate\services\modele_cereri\06. vaslui\01. Aviz APM\Model email.docx"

        if not os.path.exists(model_cerere):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru cererea APM Vaslui")

        if not os.path.exists(model_notificare):
            return DocumentGenerationResult.error_result(
                "Nu găsesc șablonul pentru notificarea APM Vaslui")

        if not os.path.exists(model_email):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru Emailul APM Vaslui")

        try:
            # ----- Cerere
            context_cerere = {
                'nume_firma_proiectare': firma.nume,
                'localitate_firma_proiectare': firma.localitate.nume,
                'adresa_firma_proiectare': firma.adresa,
                'judet_firma_proiectare': firma.judet.nume,
                'nume_beneficiar': beneficiar.nume,
                'email_firma_proiectare': firma.email,
                'persoana_contact': contact.nume,
                'telefon_contact': contact.telefon,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'data': datetime.now().strftime("%d.%m.%Y"),
            }

            cerere_pdf_path = x.create_document(
                model_cerere, context_cerere, temp_dir,
                firma.cale_stampila.path,
                reprezentant.cale_semnatura.path,
            )
            temp_files.append(cerere_pdf_path)

            # ----- Notificare
            context_notificare = {
                'nume_firma_proiectare': firma.nume,
                'localitate_firma_proiectare': firma.localitate.nume,
                'adresa_firma_proiectare': firma.adresa,
                'judet_firma_proiectare': firma.judet.nume,
                'reprezentant_firma_proiectare': reprezentant.nume,
                'nume_beneficiar': beneficiar.nume,
                'localitate_beneficiar': beneficiar.localitate.nume,
                'adresa_beneficiar': beneficiar.adresa,
                'judet_beneficiar': beneficiar.judet.nume,
                'email_firma_proiectare': firma.email,
                'descrierea_proiectului': cu.descrierea_proiectului,
                'telefon_contact': contact.telefon,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'inginer_intocmit': cu.inginer_intocmit.nume,
                'inginer_verificat': cu.inginer_verificat.nume,
            }

            notificare_pdf_path = x.create_document(
                model_notificare, context_notificare, temp_dir,
                firma.cale_stampila.path,
                cu.inginer_intocmit.cale_semnatura.path,
                cu.inginer_verificat.cale_semnatura.path,
            )
            temp_files.append(notificare_pdf_path)

            # ----- Document final
            path_document_final = os.path.join(
                temp_dir, f"Documentatie aviz APM Vaslui - {beneficiar.nume}.pdf"
            )

            pdf_list = [
                cerere_pdf_path,
                cu.cale_chitanta_APM.path,
                cu.cale_CU.path,
                cu.cale_plan_incadrare_CU.path,
                cu.cale_plan_situatie_CU.path,
                notificare_pdf_path,
                cu.cale_acte_facturare.path,
            ]

            x.merge_pdfs(pdf_list, path_document_final)
            fisiere_generate.append(path_document_final)

            # 2. Generare email APM
            context_email = {
                'nume_beneficiar': beneficiar.nume,
                'nr_cu': cu.numar,
                'data_cu': cu.data,
                'emitent_cu': cu.emitent,
                'nume_lucrare': cu.nume,
                'adresa_lucrare': cu.adresa,
                'persoana_contact': contact.nume,
                'telefon_contact': contact.telefon,
            }

            email_pdf_path = x.create_document(
                model_email, context_email, temp_dir,
            )

            # Verifică dacă PDF-ul emailului există și are conținut
            if not os.path.exists(email_pdf_path) or os.path.getsize(email_pdf_path) == 0:
                raise Exception(
                    f"Emailul a fost generat, dar fișierul este gol: {email_pdf_path}")

            fisiere_generate.append(email_pdf_path)

            # Toate documentele au fost generate cu succes
            return DocumentGenerationResult.success_result(fisiere_generate)

        except Exception as e:
            # Dacă apare orice eroare, curățăm toate fișierele generate și returnăm eroarea
            for path in temp_files:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            if path_document_final and os.path.exists(path_document_final):
                try:
                    os.remove(path_document_final)
                except:
                    pass

            for path in fisiere_generate:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass

            return DocumentGenerationResult.error_result(f"Eroare la generarea documentelor: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în generate_documents_APM_vaslui: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")
