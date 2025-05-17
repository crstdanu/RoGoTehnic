import StudiiFezabilitate.Avize.functii as x
from StudiiFezabilitate.result import DocumentGenerationResult
import os
from datetime import datetime


def verifica_campuri_necesare(lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, model_detalii):
    """
    Verifică dacă toate câmpurile necesare pentru generarea avizului sunt prezente
    """
    errors = x.check_required_fields([
        (lucrare.judet.nume,
            "Nu se poate genera avizul - lipsește numele județului lucrării"),
        (firma.cale_stampila,
            "Nu se poate genera avizul - lipsește ștampila firmei de proiectare"),
        (reprezentant.cale_semnatura,
            "Nu se poate genera avizul - lipsește Semnatura reprezentantului firmei de proiectare"),

        # Fisiere necesare
        (cu.cale_CU,
         "Nu se poate genera avizul - lipsește Certificatul de Urbanism"),
        (cu.cale_plan_incadrare_CU,
            "Nu se poate genera avizul - lipsește Planul de incadrare in zona anexă CU"),
        (cu.cale_plan_situatie_CU,
            "Nu se poate genera avizul - lipsește Planul de situatie anexă CU"),
        (cu.cale_memoriu_tehnic_CU,
            "Nu se poate genera avizul - lipsește Memoriul tehnic anexă CU"),
        (cu.cale_acte_facturare,
            "Nu se poate genera avizul - lipsesc Acte facturare"),
        (reprezentant.cale_ci,
            "Nu se poate genera avizul - lipsește CI-ul Reprezentantului firmei de proiectare"),

        # Câmpuri necesae
        (firma.nume, "Nu se poate genera avizul - lipsește numele firmei de proiectare"),
        (firma.adresa, "Nu se poate genera avizul - lipsește Adresa firmei de proiectare"),
        (firma.localitate, "Nu se poate genera avizul - lipsește Localitatea firmei de proiectare"),
        (firma.judet, "Nu se poate genera avizul - lipsește Județul firmei de proiectare"),
        (firma.cui, "Nu se poate genera avizul - lipsește CUI-ul firmei de proiectare"),
        (firma.nr_reg_com, "Nu se poate genera avizul - lipsește numărul de înregistrare la Registrul Comerțului"),

        (reprezentant.nume,
         "Nu se poate genera avizul - lipsește Reprezentantul firmei de proiectare"),
        (reprezentant.localitate,
         "Nu se poate genera avizul - lipsește LOCALITATEA de domiciliu a reprezentantului firmei de proiectare"),
        (reprezentant.adresa,
         "Nu se poate genera avizul - lipsește ADRESA de domiciliu a reprezentantului firmei de proiectare"),
        (reprezentant.judet,
         "Nu se poate genera avizul - lipsește JUDEȚUL de domiciliu a reprezentantului firmei de proiectare"),
        (reprezentant.serie_ci,
         "Nu se poate genera avizul - lipsește SERIA CI a reprezentantului firmei de proiectare"),
        (reprezentant.numar_ci,
         "Nu se poate genera avizul - lipsește NUMĂR CI a reprezentantului firmei de proiectare"),
        (reprezentant.data_ci,
         "Nu se poate genera avizul - lipsește DATA CI a reprezentantului firmei de proiectare"),
        (reprezentant.cnp,
         "Nu se poate genera avizul - lipsește CNP-ul reprezentantului firmei de proiectare"),

        (beneficiar.nume, "Nu se poate genera avizul - lipsește numele beneficiarului"),
        (beneficiar.adresa, "Nu se poate genera avizul - lipsește Adresa beneficiarului"),
        (beneficiar.localitate,
         "Nu se poate genera avizul - lipsește Localitatea beneficiarului"),
        (beneficiar.judet, "Nu se poate genera avizul - lipsește Județul beneficiarului"),

        (contact.nume, "Nu se poate genera avizul - lipsește Persoana de contact"),
        (contact.telefon, "Nu se poate genera avizul - lipsește Telefonul persoanei de contact"),

        (firma.email, "Nu se poate genera avizul - lipsește Email-ul firmei de proiectare"),

        (cu.nume, "Nu se poate genera avizul - lipsește Numele lucrarii din Certificatul de urbanism"),
        (cu.adresa, "Nu se poate genera avizul - lipsește Adresa lucrarii din Certificatul de urbanism"),
        (cu.numar, "Nu se poate genera cererea - lipsește numărul certificatului de urbanism"),
        (cu.data, "Nu se poate genera cererea - lipsește data certificatului de urbanism"),
        (cu.emitent, "Nu se poate genera cererea - lipsește emitentul certificatului de urbanism"),
    ])

    # Verificăm existența modelelor pentru toate documentele de la început

    if not os.path.exists(model_cerere):
        return DocumentGenerationResult.error_result(
            "Nu găsesc modelul pentru Cerere")

    if not os.path.exists(model_detalii):
        return DocumentGenerationResult.error_result(
            "Nu găsesc șablonul pentru Detalii -> MODEL EMAIL sau Citeste-mă")

    return errors


def genereaza_cerere(lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir):
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
    }

    cerere_pdf_path = x.create_document(
        model_cerere, context_cerere, temp_dir,
        firma.cale_stampila.path,
        reprezentant.cale_semnatura.path,
    )
    return cerere_pdf_path


def genereaza_email(lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact, model_detalii, temp_dir):
    """
    Generează emailul pentru Aviz
    """
    data_cu_formatata = cu.data.strftime('%d.%m.%Y') if cu.data else ""
    context_email = {
        'email': avizCU.nume_aviz.email,
        'nume_beneficiar': beneficiar.nume,
        'nr_cu': cu.numar,
        'data_cu': data_cu_formatata,
        'emitent_cu': cu.emitent,
        'nume_lucrare': cu.nume,
        'adresa_lucrare': cu.adresa,
        'persoana_contact': contact.nume,
        'telefon_contact': contact.telefon,
        'firma_facturare': firma.nume,
        'cui_firma_facturare': firma.cui,
    }

    email_pdf_path = x.create_document(
        model_detalii, context_email, temp_dir,
    )
    return email_pdf_path


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


def genereaza_document_final_cu_CI(avizCU, cerere_pdf_path, cu, beneficiar, reprezentant, temp_dir):
    """
    Spre deosebire de functia genereaza_document_final, acesta functie mai adauga si CI-ul Reprezentantului la documentatie
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
        reprezentant.cale_ci.path,
    ]

    x.merge_pdfs(pdf_list, path_document_final)

    return path_document_final


def genereaza_document_final_PMI_Mediu(avizCU, cerere_pdf_path, plan_pdf_path, cu, beneficiar, temp_dir):
    """
    Combină toate fișierele și pregătește documentul final pentru a fi livrat
    """
    path_document_final = os.path.join(
        temp_dir, f"Documentatie {avizCU.nume_aviz.nume} - {beneficiar.nume}.pdf"
    )

    pdf_list = [
        cerere_pdf_path,
        plan_pdf_path,
        cu.cale_CU.path,
        cu.cale_plan_incadrare_CU.path,
        cu.cale_plan_situatie_CU.path,
        cu.cale_memoriu_tehnic_CU.path,
        cu.cale_acte_facturare.path,
    ]

    x.merge_pdfs(pdf_list, path_document_final)

    return path_document_final


def genereaza_document_final_print(avizCU, cerere_pdf_path, cu, beneficiar, temp_dir):
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
        cu.cale_plan_incadrare_CU.path,
        cu.cale_plan_situatie_CU.path,
        cu.cale_plan_situatie_CU.path,
        cu.cale_memoriu_tehnic_CU.path,
        cu.cale_acte_facturare.path,
    ]

    x.merge_pdfs_print(pdf_list, path_document_final)

    return path_document_final


def genereaza_document_Salubris_print(avizCU, cerere_pdf_path, cu, beneficiar, temp_dir):
    """
    Combină toate fișierele și pregătește documentul final pentru a fi livrat
    """
    path_document_final = os.path.join(
        temp_dir, f"Documentatie {avizCU.nume_aviz.nume} - {beneficiar.nume}.pdf"
    )

    pdf_list = [
        cerere_pdf_path,
        cu.cale_CU.path,
    ]

    x.merge_pdfs_print(pdf_list, path_document_final)

    return path_document_final


def genereaza_readme(temp_dir, model_readme):

    readme_pdf_path = x.copy_doc_to_pdf(model_readme, temp_dir)

    return readme_pdf_path


def verifica_campuri_necesare_EXTRA(cu):
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
