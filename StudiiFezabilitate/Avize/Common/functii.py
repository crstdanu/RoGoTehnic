import StudiiFezabilitate.Avize.functii as x
from StudiiFezabilitate.result import DocumentGenerationResult
import os
from datetime import datetime


# Doar astea
def genereaza_document_final_APM(lucrare, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir):
    """
    Combină toate fișierele și pregătește documentul final pentru a fi livrat
    """
    path_document_final = os.path.join(
        temp_dir, f"Documentatie Aviz APM {lucrare.judet.nume} - {beneficiar.nume}.pdf"
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

    return path_document_final


def genereaza_document_final_APM_print(lucrare, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir):
    """
    Combină toate fișierele și pregătește documentul final pentru a fi livrat
    """
    path_document_final = os.path.join(
        temp_dir, f"Documentatie Aviz APM {lucrare.judet.nume} - {beneficiar.nume}.pdf"
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

    x.merge_pdfs_print(pdf_list, path_document_final)

    return path_document_final


def verifica_campuri_necesare_EXTRA(cu, avizCU):
    """
    Verifică dacă toate câmpurile necesare pentru generarea avizului sunt prezente
    """
    errors = x.check_required_fields([
        (cu.suprafata_ocupata,
         "Nu se poate genera cererea - lipsește SPRAFATA OCUPATA de rețea"),
        (cu.lungime_traseu,
         "Nu se poate genera cererea - lipsește LUNGIMEA TRASEULUI de retea"),
        (avizCU.nume_aviz.email,
         "Nu se poate genera cererea - lipsește Adresa de email de la avizul CULTURA de retea"),
    ])
    return errors


def verifica_campuri_necesare_HCL(cu):
    """
    Verifică dacă toate câmpurile necesare pentru generarea avizului sunt prezente
    """
    errors = x.check_required_fields([
        (cu.suprafata_ocupata,
         "Nu se poate genera cererea - lipsește SPRAFATA OCUPATA de rețea"),
        (cu.lungime_traseu,
         "Nu se poate genera cererea - lipsește LUNGIMEA TRASEULUI de retea"),
    ])
    return errors


def genereaza_cerere_CULTURA(lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir):
    """
    Generează cererea pentru Aviz
    """
    data_cu_formatata = cu.data.strftime('%d.%m.%Y') if cu.data else ""

    context_cerere = {
        'nume_firma_proiectare': firma.nume,
        'localitate_firma_proiectare': (firma.localitate.tip + ' ' + firma.localitate.nume).strip() if firma.localitate.tip else firma.localitate.nume,
        'adresa_firma_proiectare': firma.adresa,
        'judet_firma_proiectare': firma.judet.nume,
        'email_firma_proiectare': firma.email,
        # la ApaServ se cer multe date despre REPREZENTANT in Cerere
        'reprezentant_firma_proiectare': reprezentant.nume,
        'localitate_repr': reprezentant.localitate,
        'adresa_repr': reprezentant.adresa,
        'judet_repr': reprezentant.judet,
        'cnp_repr': reprezentant.cnp,
        'seria_CI': reprezentant.serie_ci,
        'nr_CI': reprezentant.numar_ci,
        'data_CI': reprezentant.data_ci.strftime('%d.%m.%Y') if reprezentant.data_ci else "",

        'nume_beneficiar': beneficiar.nume,
        'cui_firma_proiectare': firma.cui,
        'nr_reg_com': firma.nr_reg_com,
        'telefon_contact': contact.telefon,
        'persoana_contact': contact.nume,
        'nume_lucrare': cu.nume,
        'adresa_lucrare': cu.adresa,
        'nr_cu': cu.numar,
        'data_cu': data_cu_formatata,
        'emitent_cu': cu.emitent.nume,
        'suprafata_ocupata': cu.suprafata_ocupata,
        'lungime_traseu': cu.lungime_traseu,
        'data': datetime.now().strftime("%d.%m.%Y"),
        'total_aviz': x.multiply_by_3(cu.suprafata_ocupata),

    }

    cerere_pdf_path = x.create_document(
        model_cerere, context_cerere, temp_dir,
        firma.cale_stampila.path,
        reprezentant.cale_semnatura.path,
    )
    return cerere_pdf_path


# Functii comune

def curata_fisierele_temporare(temp_files, path_document_final=None, fisiere_generate=None):
    """
    Curăță fișierele temporare generate în timpul procesului
    """
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

    if fisiere_generate:
        for path in fisiere_generate:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass


def genereaza_document_final(avizCU, cerere_pdf_path, cu, beneficiar, temp_dir):
    """
    Combină toate fișierele și pregătește documentul final pentru a fi livrat
    """
    path_document_final = os.path.join(
        temp_dir, f"Documentatie {avizCU.nume_aviz.nume} - {beneficiar.nume}.pdf"
    )

    pdf_list = [
        cerere_pdf_path,
        cu.cale_CU.path,
        cu.cale_plan_incadrare_CU.path,
        cu.cale_plan_situatie_CU.path,
        cu.cale_memoriu_tehnic_CU.path,
        cu.cale_acte_facturare.path,
    ]

    x.merge_pdfs(pdf_list, path_document_final)

    return path_document_final


def genereaza_document_final_print(avizCU, cerere_pdf_path, cu, temp_dir):
    """
    Combină toate fișierele și pregătește documentul final pentru a fi livrat
    """
    path_document_final = os.path.join(
        temp_dir, f"Documentatie aviz {avizCU.nume_aviz.nume} - de printat.pdf"
    )

    pdf_list = [
        cerere_pdf_path,
        cu.cale_chitanta_APM.path,
        cu.cale_CU.path,
        cu.cale_plan_incadrare_CU.path,
        cu.cale_plan_situatie_CU.path,
        cu.cale_acte_facturare.path,
    ]

    x.merge_pdfs_print(pdf_list, path_document_final)

    return path_document_final


# -----------------------------------------------                            Aviz APM


def verifica_campuri_necesare_APM(lucrare, firma, reprezentant, cu, beneficiar, contact):
    """
    Verifică dacă toate câmpurile necesare pentru generarea avizului APM sunt prezente
    """
    errors = x.check_required_fields([
        (lucrare.judet.nume,
            "Nu se poate genera avizul - lipsește numele județului lucrării"),
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
        (cu.emitent.nume, "Nu se poate genera emailul - lipsește numele emitentului certificatului de urbanism"),
    ])

    # Verificăm existența modelelor pentru toate documentele de la început
    model_cerere = r"StudiiFezabilitate\Avize\modele_cereri\00. Common\01. APM\Cerere_APM.docx"
    model_notificare = r"StudiiFezabilitate\Avize\modele_cereri\00. Common\01. APM\Notificare.docx"

    if lucrare.judet.nume == "Bacău":
        model_detalii = r"StudiiFezabilitate\Avize\modele_cereri\00. Common\01. APM\Readme_bacau.docx"
    else:
        model_detalii = r"StudiiFezabilitate\Avize\modele_cereri\00. Common\01. APM\Model email.docx"

    if not os.path.exists(model_cerere):
        return DocumentGenerationResult.error_result(
            "Nu găsesc modelul pentru Cererea APM")

    if not os.path.exists(model_notificare):
        return DocumentGenerationResult.error_result(
            "Nu găsesc șablonul pentru Notificarea APM")

    if not os.path.exists(model_detalii):
        return DocumentGenerationResult.error_result(
            "Nu găsesc modelul pentru Detalii APM")

    return errors


def genereaza_cerere_APM(lucrare, firma, reprezentant, beneficiar, contact, cu, temp_dir):
    """
    Generează cererea pentru APM
    """
    model_cerere = r"StudiiFezabilitate\Avize\modele_cereri\00. Common\01. APM\Cerere_APM.docx"

    context_cerere = {
        'judet_lucrare': lucrare.judet.nume,
        'nume_firma_proiectare': firma.nume,
        'localitate_firma_proiectare': (firma.localitate.tip + ' ' + firma.localitate.nume).strip() if firma.localitate.tip else
        firma.localitate.nume,
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

    return cerere_pdf_path


def genereaza_notificare_APM(lucrare, firma, reprezentant, cu, beneficiar, contact, temp_dir):
    """
    Generează notificarea pentru APM
    """
    model_notificare = r"StudiiFezabilitate\Avize\modele_cereri\00. Common\01. APM\Notificare.docx"

    context_notificare = {
        'nume_firma_proiectare': firma.nume,
        'localitate_firma_proiectare': (firma.localitate.tip + ' ' + firma.localitate.nume).strip() if firma.localitate.tip else firma.localitate.nume,
        'adresa_firma_proiectare': firma.adresa,
        'judet_firma_proiectare': firma.judet.nume,
        'reprezentant_firma_proiectare': reprezentant.nume,
        'nume_beneficiar': beneficiar.nume,
        'localitate_beneficiar': (beneficiar.localitate.tip + ' ' + beneficiar.localitate.nume).strip() if beneficiar.localitate.tip else beneficiar.localitate.nume,
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

    return notificare_pdf_path


def genereaza_document_final_APM_print(cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir):
    """
    Combină toate fișierele și pregătește documentul final pentru a fi livrat
    """
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

    x.merge_pdfs_print(pdf_list, path_document_final)

    return path_document_final


def genereaza_email_APM(lucrare, avizCU, beneficiar, cu, contact, temp_dir):
    """
    Generează emailul pentru APM și îl pregătește pentru a fi livrat
    """
    model_email = r"StudiiFezabilitate\Avize\modele_cereri\00. Common\01. APM\Model email.docx"

    context_email = {
        'email_apm': avizCU.nume_aviz.email,
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

    return email_pdf_path


def genereaza_readme_APM_bacau(temp_dir):

    model_readme = r"StudiiFezabilitate\Avize\modele_cereri\00. Common\01. APM\Readme_bacau.docx"

    readme_pdf_path = x.copy_doc_to_pdf(model_readme, temp_dir)

    return readme_pdf_path
