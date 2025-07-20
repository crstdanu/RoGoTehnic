from StudiiFezabilitate.result import DocumentGenerationResult
from . import functii_baza as baza

import os
from datetime import datetime


# ---------------------------------------    Functii de verificare

# verifica CAMPURI
def verifica_campuri_STANDARD(lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact):
    """
    Acestea sunt campurile standard necesare pentru generarea documentației
    """
    errors = baza.check_required_fields([
        (firma.nume, "Nu se poate genera avizul - lipsește numele firmei de proiectare"),
        (firma.adresa, "Nu se poate genera avizul - lipsește Adresa firmei de proiectare"),
        (firma.localitate.nume,
         "Nu se poate genera avizul - lipsește Localitatea firmei de proiectare"),
        (firma.judet.nume, "Nu se poate genera avizul - lipsește Județul firmei de proiectare"),
        (firma.email, "Nu se poate genera avizul - lipsește Email-ul firmei de proiectare"),
        (firma.cui, "Nu se poate genera avizul - lipsește CUI-ul firmei de proiectare"),
        (firma.nr_reg_com, "Nu se poate genera avizul - lipsește NR. REG. COM.-ul firmei de proiectare"),

        (reprezentant.nume,
         "Nu se poate genera avizul - lipsește Reprezentantul firmei de proiectare"),

        (beneficiar.nume, "Nu se poate genera avizul - lipsește numele beneficiarului"),
        (beneficiar.localitate.nume,
         "Nu se poate genera avizul - lipsește Localitatea beneficiarului"),
        (beneficiar.adresa, "Nu se poate genera avizul - lipsește Adresa beneficiarului"),
        (beneficiar.judet.nume,
         "Nu se poate genera avizul - lipsește Județul beneficiarului"),

        (contact.nume, "Nu se poate genera avizul - lipsește Persoana de contact"),
        (contact.telefon, "Nu se poate genera avizul - lipsește Telefonul persoanei de contact"),

        (cu.nume, "Nu se poate genera avizul - lipsește Numele lucrarii din Certificatul de urbanism"),
        (cu.adresa, "Nu se poate genera avizul - lipsește Adresa lucrarii din Certificatul de urbanism"),
        (cu.descrierea_proiectului,
         "Nu se poate genera avizul - lipsește DESCRIEREA PROIECTULUI"),
        (cu.suprafata_ocupata,
         "Nu se poate genera avizul - lipsește SUPRAFAȚA OCUPATA din Certificatul de urbanism"),
        (cu.lungime_traseu,
         "Nu se poate genera avizul - lipsește LUNGIMEA TRASEULUI din Certificatul de urbanism"),
        (cu.numar,
         "Nu se poate genera avizul - lipsește NUMARUL CERTIFICATULUI DE URBANISM"),
        (cu.data,
         "Nu se poate genera avizul - lipsește DATA CERTIFICATULUI DE URBANISM"),
        (cu.emitent.nume,
         "Nu se poate genera avizul - lipsește EMITENTUL CERTIFICATULUI DE URBANISM"),
        (cu.inginer_intocmit.nume,
         "Nu se poate genera avizul - lipsește INGINERUL INTOCMIT"),
        (cu.inginer_verificat.nume,
         "Nu se poate genera avizul - lipsește INGINERUL VERIFICATOR"),
        (avizCU.nume_aviz.email,
         "Nu se poate genera avizul - lipsește EMAIL-ul unde va fi trimisă documentația"),
    ])
    return errors


def verifica_campuri_FARA_EMAIL(lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact):
    """
    Acestea sunt campurile necesare pentru generarea documentației
    LIPSESTE verificare pentru email intrucat unele avize nu necesita email
    """
    errors = baza.check_required_fields([
        (firma.nume, "Nu se poate genera avizul - lipsește numele firmei de proiectare"),
        (firma.adresa, "Nu se poate genera avizul - lipsește Adresa firmei de proiectare"),
        (firma.localitate.nume,
         "Nu se poate genera avizul - lipsește Localitatea firmei de proiectare"),
        (firma.judet.nume, "Nu se poate genera avizul - lipsește Județul firmei de proiectare"),
        (firma.email, "Nu se poate genera avizul - lipsește Email-ul firmei de proiectare"),
        (firma.cui, "Nu se poate genera avizul - lipsește CUI-ul firmei de proiectare"),
        (firma.nr_reg_com, "Nu se poate genera avizul - lipsește NR. REG. COM.-ul firmei de proiectare"),

        (reprezentant.nume,
         "Nu se poate genera avizul - lipsește Reprezentantul firmei de proiectare"),

        (beneficiar.nume, "Nu se poate genera avizul - lipsește numele beneficiarului"),
        (beneficiar.localitate.nume,
         "Nu se poate genera avizul - lipsește Localitatea beneficiarului"),
        (beneficiar.adresa, "Nu se poate genera avizul - lipsește Adresa beneficiarului"),
        (beneficiar.judet.nume,
         "Nu se poate genera avizul - lipsește Județul beneficiarului"),

        (contact.nume, "Nu se poate genera avizul - lipsește Persoana de contact"),
        (contact.telefon, "Nu se poate genera avizul - lipsește Telefonul persoanei de contact"),

        (cu.nume, "Nu se poate genera avizul - lipsește Numele lucrarii din Certificatul de urbanism"),
        (cu.adresa, "Nu se poate genera avizul - lipsește Adresa lucrarii din Certificatul de urbanism"),
        (cu.descrierea_proiectului,
         "Nu se poate genera avizul - lipsește DESCRIEREA PROIECTULUI"),
        (cu.suprafata_ocupata,
         "Nu se poate genera avizul - lipsește SUPRAFAȚA OCUPATA din Certificatul de urbanism"),
        (cu.lungime_traseu,
         "Nu se poate genera avizul - lipsește LUNGIMEA TRASEULUI din Certificatul de urbanism"),
        (cu.numar,
         "Nu se poate genera avizul - lipsește NUMARUL CERTIFICATULUI DE URBANISM"),
        (cu.data,
         "Nu se poate genera avizul - lipsește DATA CERTIFICATULUI DE URBANISM"),
        (cu.emitent.nume,
         "Nu se poate genera avizul - lipsește EMITENTUL CERTIFICATULUI DE URBANISM"),
        (cu.inginer_intocmit.nume,
         "Nu se poate genera avizul - lipsește INGINERUL INTOCMIT"),
        (cu.inginer_verificat.nume,
         "Nu se poate genera avizul - lipsește INGINERUL VERIFICATOR"),
    ])
    return errors


# verifica FISIERE
def verifica_fisiere_incarcate_APM(cu, firma, reprezentant):
    errors = baza.check_required_fields([
        # Fisiere necesare intocmire documentatie
        (firma.cale_stampila,
         "Nu se poate genera avizul - lipsește ștampila firmei de proiectare"),
        (reprezentant.cale_semnatura,
            "Nu se poate genera avizul - lipsește Semnatura reprezentantului firmei de proiectare"),
        (cu.inginer_intocmit.cale_semnatura,
            "Nu se poate genera avizul - lipsește Semnatura inginerului intocmit"),
        (cu.inginer_verificat.cale_semnatura,
            "Nu se poate genera avizul - lipsește Semnatura inginerului verificator"),

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
        (cu.cale_chitanta_APM,
            "Nu se poate genera avizul - lipseste CHITANTA APM"),
    ])
    return errors


def verifica_fisiere_incarcate_STANDARD(cu, firma, reprezentant):
    errors = baza.check_required_fields([
        # Fisiere necesare intocmire documentatie
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
    ])
    return errors


# ------------------------------------------------------------    din cate stiu se foloseste OBLIGATORIU doar la avizul RAJA
def verifica_fisiere_incarcate_CU_PLAN_SITUATIE_PDF(cu, firma, reprezentant):
    errors = baza.check_required_fields([
        # Fisiere necesare intocmire documentatie
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
        # deocamdata folosesc asta doar la avizul RAJA
        (cu.cale_plan_situatie_la_scara,
            "Nu se poate genera avizul - lipsește Planul de situatie la scara (nu anexa CU ci cel original)"),
    ])
    return errors


# verifica MODELE
def verifica_existenta_modele(model_cerere, model_detalii, model_notificare=None):
    if not os.path.exists(model_cerere):
        return DocumentGenerationResult.error_result(
            "Nu găsesc modelul pentru Cerere")

    if model_notificare and not os.path.exists(model_notificare):
        return DocumentGenerationResult.error_result(
            "Nu găsesc modelul pentru Notificare")

    if not os.path.exists(model_detalii):
        return DocumentGenerationResult.error_result(
            "Nu găsesc șablonul pentru Detalii -> MODEL EMAIL sau Citeste-mă")

    return None  # No errors found


# --------------------------------------      Functii de generare documente


def genereaza_cerere_minimala(lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir):
    """
    Generează cererea pentru Aviz folosind date minimale
    și returnează calea către documentul generat.
    """

    context_cerere = {
        'nume_firma': firma.nume,
        'localitate_firma': (firma.localitate.tip + ' ' + firma.localitate.nume).strip() if firma.localitate.tip else firma.localitate.nume,
        'adresa_firma': firma.adresa,
        'judet_firma': firma.judet.nume,
        'email_firma': firma.email,
        'cui_firma': firma.cui,
        'nr_reg_com': firma.nr_reg_com,
        'reprezentant_firma': reprezentant.nume,

        'nume_beneficiar': beneficiar.nume,

        'telefon_contact': contact.telefon,
        'persoana_contact': contact.nume,

        'nume_lucrare_CU': cu.nume,
        'adresa_lucrare_CU': cu.adresa,

        'data': datetime.now().strftime("%d.%m.%Y"), }

    # Generăm documentul și verificăm rezultatul
    cerere_pdf_path = baza.create_document(
        model_cerere,
        context_cerere,
        temp_dir,
        firma.cale_stampila.path,
        reprezentant.cale_semnatura.path,)

    return cerere_pdf_path


def genereaza_cerere_STANDARD(lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir):
    """
    Generează cererea pentru Aviz folosind date minimale
    și returnează calea către documentul generat.
    """
    data_cu_formatata = cu.data.strftime('%d.%m.%Y') if cu.data else ""

    context_cerere = {
        'nume_firma': firma.nume,
        'localitate_firma': (firma.localitate.tip + ' ' + firma.localitate.nume).strip() if firma.localitate.tip else firma.localitate.nume,
        'adresa_firma': firma.adresa,
        'judet_firma': firma.judet.nume,
        'email_firma': firma.email,
        'cui_firma': firma.cui,
        'nr_reg_com': firma.nr_reg_com,

        'reprezentant_firma': reprezentant.nume,

        'nume_beneficiar': beneficiar.nume,

        'telefon_contact': contact.telefon,
        'persoana_contact': contact.nume,

        'nume_lucrare_CU': cu.nume,
        'adresa_lucrare_CU': cu.adresa,
        'nr_cu': cu.numar,
        'data_cu': data_cu_formatata,
        'emitent_cu': cu.emitent.nume,

        'suprafata_mp': cu.suprafata_ocupata,
        'lungime_traseu': cu.lungime_traseu,  # folosit la HCL

        'firma_facturare': firma.nume,
        'cui_firma_facturare': firma.cui,

        'data': datetime.now().strftime("%d.%m.%Y"), }

    # Generăm documentul și verificăm rezultatul
    cerere_pdf_path = baza.create_document(
        model_cerere,
        context_cerere,
        temp_dir,
        firma.cale_stampila.path,
        reprezentant.cale_semnatura.path,)

    return cerere_pdf_path


def genereaza_cerere_CULTURA(lucrare, firma, reprezentant, cu, beneficiar, contact, model_cerere, temp_dir):
    """
    Generează cererea pentru Aviz folosind date minimale
    și returnează calea către documentul generat.
    """
    data_cu_formatata = cu.data.strftime('%d.%m.%Y') if cu.data else ""

    context_cerere = {
        'nume_firma': firma.nume,
        'localitate_firma': (firma.localitate.tip + ' ' + firma.localitate.nume).strip() if firma.localitate.tip else firma.localitate.nume,
        'adresa_firma': firma.adresa,
        'judet_firma': firma.judet.nume,
        'email_firma': firma.email,
        'cui_firma': firma.cui,
        'nr_reg_com': firma.nr_reg_com,

        'reprezentant_firma': reprezentant.nume,

        'nume_beneficiar': beneficiar.nume,

        'telefon_contact': contact.telefon,
        'persoana_contact': contact.nume,

        'nume_lucrare_CU': cu.nume,
        'adresa_lucrare_CU': cu.adresa,
        'nr_cu': cu.numar,
        'data_cu': data_cu_formatata,
        'emitent_cu': cu.emitent.nume,

        'suprafata_mp': cu.suprafata_ocupata,  # asta e la Cultura
        # asta e doar la CULTURA
        'total_aviz': baza.multiply_by_3(cu.suprafata_ocupata),

        'data': datetime.now().strftime("%d.%m.%Y"), }

    # Generăm documentul și verificăm rezultatul
    cerere_pdf_path = baza.create_document(
        model_cerere,
        context_cerere,
        temp_dir,
        firma.cale_stampila.path,
        reprezentant.cale_semnatura.path,)

    return cerere_pdf_path


def genereaza_notificare_APM(lucrare, firma, reprezentant, cu, beneficiar, contact, model_notificare, temp_dir):
    """
    Generează notificarea pentru APM folosind datele furnizate
    și returnează calea către documentul generat.
    """

    context_notificare = {
        'nume_firma': firma.nume,
        'localitate_firma': (firma.localitate.tip + ' ' + firma.localitate.nume).strip() if firma.localitate.tip else firma.localitate.nume,
        'adresa_firma': firma.adresa,
        'judet_firma': firma.judet.nume,
        'email_firma': firma.email,
        'cui_firma': firma.cui,

        'reprezentant_firma': reprezentant.nume,


        'nume_lucrare_CU': cu.nume,
        'adresa_lucrare_CU': cu.adresa,

        'nume_beneficiar': beneficiar.nume,
        'localitate_beneficiar': (beneficiar.localitate.tip + ' ' + beneficiar.localitate.nume).strip() if beneficiar.localitate.tip else beneficiar.localitate.nume,
        'adresa_beneficiar': beneficiar.adresa,
        'judet_beneficiar': beneficiar.judet.nume,

        'suprafata_mp': cu.suprafata_ocupata,
        'telefon_contact': contact.telefon,

        'descrierea_proiectului': cu.descrierea_proiectului,

        'inginer_intocmit': cu.inginer_intocmit.nume,
        'inginer_verificat': cu.inginer_verificat.nume,
    }

    notificare_pdf_path = baza.create_document(
        model_notificare, context_notificare, temp_dir,
        firma.cale_stampila.path,
        cu.inginer_intocmit.cale_semnatura.path,
        cu.inginer_verificat.cale_semnatura.path,
    )
    return notificare_pdf_path


# --------------------------------------      Aici se genereaza documentele finale

def genereaza_document_final_APM(lucrare, avizCU, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir, print=False):
    """
    Combină toate fișierele și pregătește documentul final pentru a fi livrat
    """
    path_document_final = os.path.join(
        temp_dir, f"Documentatie {avizCU.nume_aviz.nume} - pentru {beneficiar.nume}.pdf"
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

    if print:
        baza.merge_pdfs_print(pdf_list, path_document_final)
    else:
        baza.merge_pdfs(pdf_list, path_document_final)

    return path_document_final


def genereaza_document_final_PMI_MEDIU(lucrare, avizCU, cerere_pdf_path, notificare_pdf_path, cu, beneficiar, temp_dir, print=False):
    """
    Combină toate fișierele și pregătește documentul final pentru a fi livrat
    """
    path_document_final = os.path.join(
        temp_dir, f"Documentatie {avizCU.nume_aviz.nume} - pentru {beneficiar.nume}.pdf"
    )

    pdf_list = [
        cerere_pdf_path,
        notificare_pdf_path,
        cu.cale_CU.path,
        cu.cale_plan_incadrare_CU.path,
        cu.cale_plan_situatie_CU.path,
        cu.cale_acte_facturare.path,
    ]

    baza.merge_pdfs(pdf_list, path_document_final)

    return path_document_final


def genereaza_document_final_STANDARD(lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir, print=False):
    """
    Combină toate fișierele și pregătește documentul final pentru a fi livrat
    """
    if print:
        path_document_final = os.path.join(
            temp_dir, f"Documentatie {avizCU.nume_aviz.nume} - DE PRINTAT.pdf"
        )
    else:
        path_document_final = os.path.join(
            temp_dir, f"Documentatie {avizCU.nume_aviz.nume} - pentru {beneficiar.nume}.pdf"
        )

    pdf_list = [
        cerere_pdf_path,
        cu.cale_CU.path,
        cu.cale_plan_incadrare_CU.path,
        cu.cale_plan_situatie_CU.path,
        cu.cale_memoriu_tehnic_CU.path,
        cu.cale_acte_facturare.path,
    ]

    if print:
        baza.merge_pdfs_print(pdf_list, path_document_final)
    else:
        baza.merge_pdfs(pdf_list, path_document_final)

    return path_document_final


def genereaza_document_final_Salubris(lucrare, avizCU, cerere_pdf_path, cu, beneficiar, temp_dir):
    """
    Combină toate fișierele și pregătește documentul final pentru a fi livrat
    """

    path_document_final = os.path.join(
        temp_dir, f"Documentatie {avizCU.nume_aviz.nume} - DE PRINTAT.pdf"
    )
    pdf_list = [
        cerere_pdf_path,
        cu.cale_CU.path,
    ]
    baza.merge_pdfs_print(pdf_list, path_document_final)

    return path_document_final


# --------------------------------------       Aici se genereaza email si readme

# am observat ca modelele de email au aceleasi campuri, deci pot pastra doar o singura functie aici
def genereaza_email(lucrare, avizCU, firma, reprezentant, cu, beneficiar, contact, model_detalii, temp_dir):
    """
    Generează emailul și îl pregătește pentru a fi livrat
    """
    data_cu_formatata = cu.data.strftime('%d.%m.%Y') if cu.data else ""

    context_email = {
        'email_aviz': avizCU.nume_aviz.email,
        'nume_beneficiar': beneficiar.nume,
        'nr_cu': cu.numar,
        'data_cu': data_cu_formatata,
        'emitent_cu': cu.emitent,
        'nume_lucrare_CU': cu.nume,
        'adresa_lucrare_CU': cu.adresa,
        'persoana_contact': contact.nume,
        'telefon_contact': contact.telefon,
        'firma_facturare': firma.nume,
        'cui_firma_facturare': firma.cui,
    }

    email_pdf_path = baza.create_document(
        model_detalii, context_email, temp_dir,
    )

    # Verifică dacă PDF-ul emailului există și are conținut
    if not os.path.exists(email_pdf_path) or os.path.getsize(email_pdf_path) == 0:
        raise Exception(
            f"Emailul a fost generat, dar fișierul este gol: {email_pdf_path}")

    return email_pdf_path


def genereaza_readme(model_readme, temp_dir):
    readme_pdf_path = baza.copy_doc_to_pdf(model_readme, temp_dir)

    return readme_pdf_path
