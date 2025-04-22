from StudiiFezabilitate.models import AvizeCU, Lucrare
import StudiiFezabilitate.services.functii as x
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

        # Verificări inițiale
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
        ])
        if errors:
            return errors

        # Lista pentru a ține evidența fișierelor generate temporar
        generated_files = []

        temp_dir = tempfile.gettempdir()

        # ----- Cerere
        model_cerere = r"StudiiFezabilitate\services\modele_cereri\01. iasi\01. Aviz APM\Cerere_APM.docx"
        if not os.path.exists(model_cerere):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru cererea APM Iași")

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

        try:
            cerere_pdf_path = x.create_document(
                model_cerere, context_cerere, temp_dir,
                firma.cale_stampila.path,
                reprezentant.cale_semnatura.path,
            )
            generated_files.append(cerere_pdf_path)
        except Exception as e:
            return DocumentGenerationResult.error_result(f"Avizul nu poate fi generat - eroare: {str(e)}")

        # ----- Notificare
        model_notificare = r"StudiiFezabilitate\services\modele_cereri\01. iasi\01. Aviz APM\Notificare.docx"
        if not os.path.exists(model_notificare):
            # Curățăm fișierele generate până acum înainte de a returna eroarea
            for path in generated_files:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass
            return DocumentGenerationResult.error_result(
                "Nu găsesc șablonul pentru notificarea APM Iași")

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

        try:
            notificare_pdf_path = x.create_document(
                model_notificare, context_notificare, temp_dir,
                firma.cale_stampila.path,
                cu.inginer_intocmit.cale_semnatura.path,
                cu.inginer_verificat.cale_semnatura.path,
            )
            generated_files.append(notificare_pdf_path)
        except Exception as e:
            # Curățăm fișierele generate până acum înainte de a returna eroarea
            for path in generated_files:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass
            return DocumentGenerationResult.error_result(f"Notificarea nu a putut fi generata - eroare: {str(e)}")

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

        try:
            x.merge_pdfs(pdf_list, path_document_final)
        except Exception as e:
            # Curățăm fișierele generate până acum înainte de a returna eroarea
            for path in generated_files:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except:
                        pass
            return DocumentGenerationResult.error_result(f"Unirea PDF-urilor a eșuat - eroare: {str(e)}")

        # Cleanup temporare
        for path in generated_files:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    print(
                        f"Avertizare: Nu am putut șterge fișierul temporar {path}")

        # Returnăm un rezultat de succes cu calea către documentul final
        return DocumentGenerationResult.success_result(path_document_final)

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în aviz_APM_iasi: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")


def email_APM_iasi(lucrare_id, id_aviz):
    # verificam daca avem toate datele necesare pentru generarea emailului
    try:
        lucrare = Lucrare.objects.get(pk=lucrare_id)
        avizCU = AvizeCU.objects.get(pk=id_aviz)
        cu = avizCU.certificat_urbanism
        beneficiar = lucrare.beneficiar
        contact = lucrare.persoana_contact

        errors = x.check_required_fields([
            (cu.numar, "Nu se poate genera emailul - lipsește numărul certificatului de urbanism"),
            (cu.data, "Nu se poate genera emailul - lipsește data certificatului de urbanism"),
            (cu.emitent, "Nu se poate genera emailul - lipsește emitentul certificatului de urbanism"),
            (cu.nume, "Nu se poate genera emailul - lipsește numele lucrării"),
            (cu.adresa, "Nu se poate genera emailul - lipsește adresa lucrării"),
            (contact.nume, "Nu se poate genera emailul - lipsește numele persoanei de contact"),
            (contact.telefon, "Nu se poate genera emailul - lipsește telefonul persoanei de contact"),
            (beneficiar.nume, "Nu se poate genera emailul - lipsește numele beneficiarului"),
        ])
        # aici returnez erorile daca sunt
        if errors:
            return errors

        temp_dir = tempfile.gettempdir()

        model_email = r"StudiiFezabilitate\services\modele_cereri\01. iasi\01. Aviz APM\Model email.docx"
        if not os.path.exists(model_email):
            return DocumentGenerationResult.error_result(
                "Nu găsesc modelul pentru Emailul APM Iași")

        context = {
            'nume_beneficiar': beneficiar.nume,
            'nr_cu': cu.numar,
            'data_cu': cu.data,
            'emitent_cu': cu.emitent,
            'nume_lucrare': cu.nume,
            'adresa_lucrare': cu.adresa,
            'persoana_contact': contact.nume,
            'telefon_contact': contact.telefon,
        }

        try:
            # create_document va genera un PDF direct și va șterge DOCX-ul
            email_pdf_path = x.create_document(
                model_email, context, temp_dir,
            )

            # Verifică dacă PDF-ul există și are conținut
            if not os.path.exists(email_pdf_path) or os.path.getsize(email_pdf_path) == 0:
                return DocumentGenerationResult.error_result(
                    f"Emailul a fost generat, dar fișierul este gol: {email_pdf_path}")

            # Returnează un rezultat de succes cu calea către PDF
            return DocumentGenerationResult.success_result(email_pdf_path)

        except Exception as e:
            return DocumentGenerationResult.error_result(f"Emailul nu poate fi generat - eroare: {str(e)}")

    except Lucrare.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Lucrare cu ID {lucrare_id} nu există")

    except AvizeCU.DoesNotExist:
        return DocumentGenerationResult.error_result(f"Aviz cu ID {id_aviz} nu există")

    except Exception as e:
        print(f"Eroare în email_APM_iasi: {e}")
        return DocumentGenerationResult.error_result(f"Eroare neașteptată: {str(e)}")
